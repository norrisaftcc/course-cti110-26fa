# CTI 110
# CYOA KIT - Engine
# norris
# 10/15/26

# The engine holds the RULES of every story. It never prints and never
# asks for input. Every function takes plain dicts and lists and gives
# back new ones. The words of the game live in the story file, not here.
#
# Do not change this file. The checker tells you if it has changed.

import copy
import json
import random

STATE_KEYS = ["story", "scene", "group", "fields", "meters", "flags", "trail"]   # no others

# Each kind of dice: (how many dice, lowest face, highest face).
DICE = {"1d6": (1, 1, 6), "2d6": (2, 1, 6), "1d20": (1, 1, 20), "4dF": (4, -1, 1)}

# ---------- Loading a story ----------
def load_story(path):
    """Read a story file and return it as a dict."""
    # utf-8-sig also reads files that Windows Notepad saved with a BOM.
    with open(path, encoding="utf-8-sig") as file:
        text = file.read()
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        # Turn Python's error into a plain message with the line and column.
        message = f"{path} line {error.lineno}, column {error.colno}: {error.msg}"
        raise ValueError(message) from None

def make_rng(seed):
    """Make the dice. The same seed always gives the same rolls."""
    return random.Random(seed)

def new_state(story):
    """Make the state for a brand new game, at the start scene."""
    fields = {}
    for field in story["fields"]:
        fields[field["id"]] = ""            # every field starts empty
    meters = {}
    for meter in story.get("meters", []):
        meters[meter["id"]] = meter["start"]
    return {"story": story["id"], "scene": story["start"], "group": 0, "fields": fields,
            "meters": meters, "flags": [], "trail": [story["start"]]}

# ---------- Looking things up ----------
def find_scene(story, scene_id):
    """Return the scene with this id, or None if there is no such scene."""
    for scene in story["scenes"]:
        if scene["id"] == scene_id:
            return scene
    return None

def is_over(story, state):
    """True when the player is at an ending."""
    return state["scene"] in story["endings"]

def get_ending(story, state):
    """Return the ending the player is at."""
    return story["endings"][state["scene"]]

# ---------- Conditions ----------
def _test_simple(cond, state):
    """Test one of the four simple forms: flag, field, meter gte, meter lte."""
    if "flag" in cond:
        return cond["flag"] in state["flags"]
    if "field" in cond:
        return state["fields"].get(cond["field"]) == cond["is"]
    if "gte" in cond:
        return state["meters"][cond["meter"]] >= cond["gte"]
    if "lte" in cond:
        return state["meters"][cond["meter"]] <= cond["lte"]
    raise ValueError(f"Unknown condition: {cond}")

def test_condition(cond, state):
    """True when the condition holds. No condition at all counts as true."""
    if cond is None:
        return True
    # not, all and any hold simple forms only (one level), so no recursion.
    if "not" in cond:
        return not _test_simple(cond["not"], state)
    if "all" in cond:                       # every inner condition is true
        return all(_test_simple(inner, state) for inner in cond["all"])
    if "any" in cond:                       # at least one inner condition is true
        return any(_test_simple(inner, state) for inner in cond["any"])
    return _test_simple(cond, state)

def visible(items, state):
    """Return the beats or options whose 'when' is true, in written order."""
    shown = []
    for item in items:
        if test_condition(item.get("when"), state):
            shown.append(item)
    return shown

# ---------- Choice groups ----------
def _group_index(story, state):
    """The index of the next group that has a visible option, or None."""
    scene = find_scene(story, state["scene"])
    if scene is None:                       # an ending has no choices
        return None
    groups = scene.get("choices", [])
    for index in range(state["group"], len(groups)):
        if visible(groups[index]["options"], state):
            return index
    return None                             # every question is done

def current_group(story, state):
    """The question to ask now, or None when this scene's questions are done."""
    index = _group_index(story, state)
    if index is None:
        return None
    return find_scene(story, state["scene"])["choices"][index]

# ---------- Effects ----------
def _apply_effect(story, state, effect):
    """Make one change to the state. The state must already be a copy."""
    if "flag" in effect:
        if effect["flag"] not in state["flags"]:
            state["flags"].append(effect["flag"])
            state["flags"].sort()           # flags stay a sorted list
    elif "set" in effect:
        for field_id, word in effect["set"].items():
            state["fields"][field_id] = word
    elif "meter" in effect:
        meter_id = effect["meter"]
        value = state["meters"][meter_id] + effect["add"]
        for meter in story["meters"]:
            if meter["id"] == meter_id:
                value = max(meter["min"], min(meter["max"], value))   # clamp
        state["meters"][meter_id] = value

def _move_to(state, target):
    """Enter a scene or an ending. The state must already be a copy."""
    state["scene"] = target
    state["group"] = 0
    state["trail"].append(target)

# ---------- Dice ----------
def roll_dice(dice, rng):
    """Roll the dice. '2d6' gives two faces, like [3, 5]."""
    count, low, high = DICE[dice]
    faces = []
    for _ in range(count):
        faces.append(rng.randint(low, high))
    return faces

def _is_success(resolver, total, vs):
    """OSE: meet or beat vs. Fate: beat vs (a tie is a fail)."""
    if resolver == "fate4df":
        return total > vs
    return total >= vs

def _roll(story, state, roll, rng):
    """Roll for an option and return the roll report."""
    faces = roll_dice(roll["dice"], rng)
    bonus = state["meters"][roll["add"]]
    total = sum(faces) + bonus
    result = "fail"
    if _is_success(story.get("resolver"), total, roll["vs"]):
        result = "success"
    return {"dice": roll["dice"], "faces": faces, "add": roll["add"], "bonus": bonus,
            "total": total, "vs": roll["vs"], "result": result}

# ---------- Making a pick ----------
def choose(story, state, option_key, rng):
    """Apply one pick. Return (new_state, beats, report). The old state is not changed."""
    index = _group_index(story, state)
    if index is None:
        raise ValueError("There is no question to answer right now.")
    group = find_scene(story, state["scene"])["choices"][index]
    option = None
    for item in visible(group["options"], state):
        if item["key"] == option_key:
            option = item
    if option is None:
        raise ValueError(f"'{option_key}' is not a visible option of group '{group['key']}'.")

    new = copy.deepcopy(state)              # work on a copy, never the original
    new["group"] = index + 1                # the next question in this scene
    # 1. The option's effects.
    for effect in option.get("effects", []):
        _apply_effect(story, new, effect)
    # 2. The roll, then 3. the result's effects.
    report, result = None, {}
    if "roll" in option:
        report = _roll(story, new, option["roll"], rng)
        result = option["roll"]["results"][report["result"]]
        for effect in result.get("effects", []):
            _apply_effect(story, new, effect)
    # 4. The beats, chosen AFTER the effects, so they see the new state.
    beats = visible(option.get("then", []), new) + visible(result.get("then", []), new)
    # 5. Leave the scene now, if the option says where to.
    if "to" in option:
        _move_to(new, option["to"])
    return new, beats, report

def leave_scene(story, state):
    """Follow the scene's exit: next, ending, or the first route that matches."""
    scene = find_scene(story, state["scene"])
    if scene is None:
        raise ValueError("The game is over; there is no scene to leave.")
    new = copy.deepcopy(state)
    if "next" in scene:
        target = scene["next"]
    elif "ending" in scene:
        target = scene["ending"]
    else:
        target = scene["route"][-1]["to"]   # the last entry is the default
        for entry in scene["route"]:
            if test_condition(entry.get("when"), new):
                target = entry["to"]
                break
    _move_to(new, target)
    return new

# ---------- Save and load ----------
def save_game(state, path):
    """Write the state to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)

def load_game(story, path):
    """Read a saved state and check that it fits this story."""
    with open(path, encoding="utf-8") as file:
        try:
            state = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path} is not valid JSON (line {error.lineno}).") from None
    if not isinstance(state, dict) or sorted(state) != sorted(STATE_KEYS):
        raise ValueError(f"A save file needs exactly these keys: {', '.join(STATE_KEYS)}.")
    if state["story"] != story["id"]:
        raise ValueError(f"That save is for the story '{state['story']}', not '{story['id']}'.")
    if find_scene(story, state["scene"]) is None and state["scene"] not in story["endings"]:
        raise ValueError(f"The save names '{state['scene']}', which is not in this story.")
    if not isinstance(state["group"], int) or state["group"] < 0:
        raise ValueError("The save's group must be a whole number, 0 or more.")
    for kind, declared in (("fields", story["fields"]), ("meters", story.get("meters", []))):
        wanted = sorted(item["id"] for item in declared)
        if not isinstance(state[kind], dict) or sorted(state[kind]) != wanted:
            raise ValueError(f"The save's {kind} do not match this story's {kind}: {wanted}.")
    if not isinstance(state["flags"], list) or not isinstance(state["trail"], list):
        raise ValueError("The save's flags and trail must be lists.")
    state["flags"] = sorted(state["flags"])
    return state
