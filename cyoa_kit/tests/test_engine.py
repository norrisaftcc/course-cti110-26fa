# CTI 110
# CYOA KIT - Test runner
# norris
# 10/15/26

# Checks of the engine's rules. Each test is a plain function that uses
# assert. run_tests.py calls every function whose name starts with test_.
# You can also run this file by itself:  python3 tests/test_engine.py

import copy
import json
import os
import sys
import tempfile
import types

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)
import engine                                   # noqa: E402  (needs the path above)

TOY = os.path.join(KIT, "stories", "toy.json")

def fixed_dice(face):
    """A stand-in for random.Random: every die shows this face."""
    return types.SimpleNamespace(randint=lambda low, high: face)

def roll_story(resolver, dice, bonus, vs):
    """A one-scene story whose only option rolls the dice."""
    roll = {"dice": dice, "add": "skill", "vs": vs,
            "results": {"fail": {"effects": [{"flag": "lost"}]},
                        "success": {"effects": [{"flag": "won"}]}}}
    return {"id": "dice", "title": "Dice", "start": "s1", "resolver": resolver,
            "fields": [],
            "meters": [{"id": "skill", "label": "Skill", "min": 0, "max": 9, "start": bonus}],
            "scenes": [{"id": "s1", "title": "One", "beats": [{"text": "Roll."}],
                        "choices": [{"key": "g", "ask": "Roll?", "gate": "exec",
                                     "options": [{"key": "go", "label": "Go", "roll": roll}]}],
                        "ending": "end"}],
            "endings": {"end": {"title": "End", "beats": [{"text": "Done."}]}}}

def play_toy(keys):
    """Play the toy story with these option keys. Return the last state."""
    story = engine.load_story(TOY)
    state = engine.new_state(story)
    for key in keys:
        while engine.current_group(story, state) is None:
            state = engine.leave_scene(story, state)
        state, beats, report = engine.choose(story, state, key, None)
    return story, state

def test_ose_meets_vs_succeeds():
    story = roll_story("ose", "1d6", 2, 5)
    state = engine.new_state(story)
    new, beats, report = engine.choose(story, state, "go", fixed_dice(3))
    assert report["total"] == 5 and report["result"] == "success", report
    assert new["flags"] == ["won"]

def test_ose_one_below_vs_fails():
    story = roll_story("ose", "1d6", 2, 5)
    new, beats, report = engine.choose(story, engine.new_state(story), "go", fixed_dice(2))
    assert report["total"] == 4 and report["result"] == "fail", report
    assert new["flags"] == ["lost"]

def test_fate_tie_fails():
    story = roll_story("fate4df", "4dF", 2, 2)
    new, beats, report = engine.choose(story, engine.new_state(story), "go", fixed_dice(0))
    assert report["faces"] == [0, 0, 0, 0] and report["total"] == 2, report
    assert report["result"] == "fail"

def test_fate_beats_vs_succeeds():
    story = roll_story("fate4df", "4dF", 2, 2)
    new, beats, report = engine.choose(story, engine.new_state(story), "go", fixed_dice(1))
    assert report["total"] == 6 and report["result"] == "success", report

def test_seeded_dice_repeat():
    first = engine.roll_dice("4dF", engine.make_rng(7))
    second = engine.roll_dice("4dF", engine.make_rng(7))
    assert first == second and len(first) == 4

def test_choose_does_not_change_its_input():
    story, state = play_toy(["wizard"])
    before = copy.deepcopy(state)
    engine.choose(story, state, "lamp", None)
    assert state == before

def test_state_survives_json():
    story, state = play_toy(["fighter", "lamp"])
    assert json.loads(json.dumps(state)) == state
    path = os.path.join(tempfile.mkdtemp(), "save.json")
    engine.save_game(state, path)
    assert engine.load_game(story, path) == state

def test_hidden_option_raises():
    story, state = play_toy(["wizard", "lamp"])
    state = engine.leave_scene(story, state)            # walk into the yard
    for key in ("lift", "nope"):
        try:
            engine.choose(story, state, key, None)
        except ValueError:
            continue
        raise AssertionError(f"choose accepted the option '{key}'")

def test_meter_clamps_at_max_and_min():
    story = roll_story("ose", "1d6", 2, 5)
    group = story["scenes"][0]["choices"][0]
    group["options"] = [{"key": "up", "label": "Up", "effects": [{"meter": "skill", "add": 50}]},
                        {"key": "down", "label": "Down", "effects": [{"meter": "skill", "add": -50}]}]
    state = engine.new_state(story)
    assert engine.choose(story, state, "up", None)[0]["meters"]["skill"] == 9
    assert engine.choose(story, state, "down", None)[0]["meters"]["skill"] == 0

def test_group_with_no_visible_option_is_skipped():
    story = roll_story("ose", "1d6", 2, 5)
    hidden = {"key": "secret", "ask": "Hidden?", "gate": "plan",
              "options": [{"key": "x", "label": "X", "when": {"flag": "never"}}]}
    story["scenes"][0]["choices"].insert(0, hidden)
    state = engine.new_state(story)
    assert engine.current_group(story, state)["key"] == "g"
    new, beats, report = engine.choose(story, state, "go", fixed_dice(6))
    assert new["group"] == 2 and engine.current_group(story, new) is None

def test_trail_and_ending():
    story, state = play_toy(["fighter", "lamp", "lift"])
    assert state["trail"] == ["gate", "yard", "treasure"]
    assert engine.is_over(story, state)
    assert engine.get_ending(story, state)["title"] == "Down the Well"

def test_then_beats_see_the_new_state():
    story = engine.load_story(TOY)
    state = engine.new_state(story)
    state, beats, report = engine.choose(story, state, "wizard", None)
    state, beats, report = engine.choose(story, state, "lamp", None)
    assert [beat["text"] for beat in beats] == ["The lamp is warm. Someone lit it today."]
    assert report is None and state["flags"] == ["lamp"]

def test_bad_json_names_line_and_column():
    path = os.path.join(KIT, "tests", "broken", "bad_json.json")
    try:
        engine.load_story(path)
    except ValueError as error:
        assert "line 12, column 7" in str(error), str(error)
        return
    raise AssertionError("bad JSON loaded")

def test_load_game_rejects_another_story():
    story, state = play_toy(["fighter"])
    state["story"] = "fort"
    path = os.path.join(tempfile.mkdtemp(), "save.json")
    engine.save_game(state, path)
    try:
        engine.load_game(story, path)
    except ValueError as error:
        assert "fort" in str(error)
        return
    raise AssertionError("a save from another story loaded")

def all_tests():
    """Every test function in this file, in the order written."""
    found = []
    for name, value in list(globals().items()):
        if name.startswith("test_") and callable(value):
            found.append((name, value))
    return found

if __name__ == "__main__":
    for test_name, test in all_tests():
        test()
        print("PASS", test_name)
