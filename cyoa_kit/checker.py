# CTI 110
# CYOA KIT - Checker
# norris
# 10/15/26

# Checks a story:  python3 checker.py stories/toy.json [--banned FILE]
# Part 1 checks the SHAPE (rules 1-13). Part 2 PLAYS every path (rules 14-21).
# Each line starts with OK, WARNING or PROBLEM. Rules: STORY-FORMAT.md, 11.4.

import hashlib
import json
import os
import re
import sys
import types
from collections import deque

import engine

# The SHA-256 of the kit's engine.py. Students never change the engine.
ENGINE_SHA256 = "5c7e221756657f19c3e072e80cbb2b4b91a9997a9eb90c695c63c2ecee6d1b16"
STATE_CAP = 50000
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
SIMPLE_FORMS = [["flag"], ["field", "is"], ["gte", "meter"], ["lte", "meter"]]

# For each kind of object: its rule, and what each key holds. "!" marks a key
# it must have; "list+" is a list of one or more; "a|b" means a or b.
SHAPES = {
    "the story": (2, {"id": "text!", "title": "text!", "subtitle": "text", "start": "text!",
                      "fields": "list!", "meters": "list", "resolver": "ose|fate4df",
                      "scenes": "list+!", "endings": "object!"}),
    "a field": (13, {"id": "text!", "label": "text!", "side": "front|back"}),
    "a meter": (13, {"id": "text!", "label": "text!", "min": "whole!", "max": "whole!",
                     "start": "whole!", "hud": "bool"}),
    "a scene": (5, {"id": "text!", "title": "text!", "place": "text", "beats": "list+!",
                    "choices": "list", "next": "text", "ending": "text", "route": "list+"}),
    "a beat": (8, {"text": "text!", "speaker": "text", "when": "object", "screen": "list"}),
    "a group": (9, {"key": "text!", "ask": "text!", "gate": "plan|exec!", "options": "list+!"}),
    "an option": (9, {"key": "text!", "label": "text!", "sub": "text", "when": "object",
                      "effects": "list", "then": "list", "to": "text", "roll": "object"}),
    "a route entry": (7, {"when": "object", "to": "text!"}),
    "an ending": (8, {"title": "text!", "beats": "list+!"}),
    "a roll": (12, {"dice": "1d6|2d6|1d20|4dF!", "add": "text!", "vs": "whole!", "results": "object!"}),
    "a roll result": (12, {"effects": "list", "then": "list"}),
}
WORDS = {"text": "text, not empty", "whole": "a whole number", "list": "a list", "bool": "true or false",
         "list+": "a list with at least one item", "object": "an object { ... }"}

HIGHEST = types.SimpleNamespace(randint=lambda low, high: high)   # stand-in dice: the top face
LOWEST = types.SimpleNamespace(randint=lambda low, high: low)     # stand-in dice: the bottom face

def ok(report, text):
    report["lines"].append("OK " + text)
def warning(report, where, text, rule):
    report["lines"].append(f"WARNING {where + ': ' if where else ''}{text} ({rule})")
    report["warnings"] = report["warnings"] + 1
def problem(report, where, text, rule):
    report["lines"].append(f"PROBLEM {where + ': ' if where else ''}{text} (rule {rule})")
    report["problems"] = report["problems"] + 1

def name_of(kind, item, key, number):
    """Name an object for a message: "group 'well'", or "group 2" if it has no key."""
    if isinstance(item, dict) and isinstance(item.get(key), str):
        return f"{kind} '{item[key]}'"
    return f"{kind} {number}"
def count(items, word):
    """'1 scene' or '2 scenes'."""
    return f"1 {word}" if len(items) == 1 else f"{len(items)} {word}s"
def holds(value, kind):
    """True when value is the kind of thing the SHAPES table asks for."""
    if kind == "text":
        return isinstance(value, str) and value.strip() != ""
    if kind == "whole":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "list+":
        return isinstance(value, list) and value != []
    if "|" in kind:
        return value in kind.split("|")
    return isinstance(value, {"list": list, "object": dict, "bool": bool}[kind])

# ---------- Part 1: the shape rules ----------
def check_object(report, where, item, kind):
    """Rule 2 and the kind's own rule: allowed keys, needed keys, right types. True if safe."""
    rule, keys = SHAPES[kind]
    if not isinstance(item, dict):
        problem(report, where, f"{kind} must be an object {{ ... }}.", 2)
        return False
    for key in item:
        if key not in keys:
            problem(report, where, f"'{key}' is not allowed in {kind}. Allowed: {', '.join(keys)}.", 2)
    safe = True
    for key, wanted in keys.items():
        if key not in item and wanted.endswith("!"):
            problem(report, where, f"{kind} needs the key '{key}'.", rule)
            safe = False
        elif key in item and not holds(item[key], wanted.rstrip("!")):
            kind_of = wanted.rstrip("!")
            words = WORDS.get(kind_of, kind_of.replace("|", " or "))
            problem(report, where, f"'{key}' must be {words}.", rule)
            safe = False
    return safe

def unique(report, where, seen, value, what):
    """Rule 3: the same key or id used twice in one place."""
    if value in seen:
        problem(report, where, f"two {what} use '{value}'. Each needs its own.", 3)
    seen.append(value)

def check_condition(report, where, cond, facts):
    """Rule 10: a simple form, or not/all/any around simple forms (one level only)."""
    parts = [cond]
    outer = list(cond)[0] if isinstance(cond, dict) and len(cond) == 1 else None
    if outer in ("not", "all", "any"):
        parts = [cond["not"]] if outer == "not" else cond[outer]
        if not isinstance(parts, list) or not parts:
            return problem(report, where, f"'{outer}' needs a list of conditions.", 10)
    for part in parts:
        if isinstance(part, dict) and part is not cond and set(part) & {"not", "all", "any"}:
            problem(report, where, f"'{outer}' holds not, all or any. One level only: use a flag.", 10)
        elif not isinstance(part, dict) or sorted(part) not in SIMPLE_FORMS:
            problem(report, where, f"{json.dumps(part)} is not a condition (see section 6).", 10)
        elif "flag" in part:
            facts["tested_flags"].append((part["flag"], where))
        elif "field" in part and part["field"] not in facts["fields"]:
            problem(report, where, f"the condition tests '{part['field']}', which is not a field.", 10)
        elif "field" in part:
            facts["tested_values"].append((part["field"], part["is"], where))
        elif part["meter"] not in facts["meters"] or not holds(part.get("gte", part.get("lte")), "whole"):
            problem(report, where, f"{json.dumps(part)} needs a declared meter and a whole number.", 10)

def check_effects(report, where, effects, facts):
    """Rule 11: a list of flag, set and meter-add effects on declared names."""
    for effect in effects:
        form = sorted(effect) if isinstance(effect, dict) else None
        if form == ["flag"] and holds(effect["flag"], "text"):
            facts["set_flags"].append(effect["flag"])
        elif form == ["set"] and isinstance(effect["set"], dict) and effect["set"]:
            for field_id, word in effect["set"].items():
                if field_id not in facts["fields"] or not isinstance(word, str):
                    problem(report, where, f"'set' needs a declared field and text: '{field_id}'.", 11)
                facts["written_values"].append((field_id, word, where))
        elif form != ["add", "meter"]:
            problem(report, where, f"{json.dumps(effect)} is not an effect (see section 6).", 11)
        elif effect["meter"] not in facts["meters"] or not holds(effect["add"], "whole"):
            problem(report, where, f"{json.dumps(effect)} needs a declared meter and a whole number.", 11)

def check_beats(report, where, beats, facts):
    """Rule 8: each beat in a list of beats."""
    for number, beat in enumerate(beats, start=1):
        place = f"{where}, beat {number}"
        if not check_object(report, place, beat, "a beat"):
            continue
        screen = beat.get("screen", [])
        if not all(isinstance(line, str) for line in screen):
            problem(report, place, "'screen' must be a list of text lines.", 8)
            screen = []
        facts["texts"].append((place, "beat", " ".join([beat["text"]] + screen)))
        if "when" in beat:
            check_condition(report, place, beat["when"], facts)

def check_roll(report, where, roll, facts):
    """Rule 12: the dice, a meter to add, a number to compare with, both results."""
    if not check_object(report, where, roll, "a roll"):
        return
    if roll["add"] not in facts["meters"] or not facts["resolver"]:
        problem(report, where, "a roll needs a meter to 'add', and the story needs a 'resolver'.", 12)
    if sorted(roll["results"]) != ["fail", "success"]:
        return problem(report, where, "'results' needs exactly 'fail' and 'success'.", 12)
    for name, result in roll["results"].items():
        place = f"{where}, roll result '{name}'"
        if check_object(report, place, result, "a roll result"):
            check_effects(report, place, result.get("effects", []), facts)
            check_beats(report, place + ", 'then'", result.get("then", []), facts)

def check_groups(report, where, groups, facts):
    """Rules 9 and 3, then 10, 11, 6 and 12: the groups of one scene, and their options."""
    group_keys = []
    for number, group in enumerate(groups, start=1):
        place = where + ", " + name_of("group", group, "key", number)
        if not check_object(report, place, group, "a group"):
            continue
        unique(report, place, group_keys, group["key"], "groups in this scene")
        facts["texts"].append((place, "ask", group["ask"]))
        option_keys = []
        for option_number, option in enumerate(group["options"], start=1):
            spot = place + ", " + name_of("option", option, "key", option_number)
            if not check_object(report, spot, option, "an option"):
                continue
            unique(report, spot, option_keys, option["key"], "options in this group")
            facts["texts"] += [(spot, "label", option["label"]), (spot, "sub", option.get("sub", ""))]
            if "when" in option:
                check_condition(report, spot, option["when"], facts)
            check_effects(report, spot, option.get("effects", []), facts)
            check_beats(report, spot + ", 'then'", option.get("then", []), facts)
            if "to" in option and option["to"] not in facts["targets"]:          # rule 6
                problem(report, spot, f"'to' names '{option['to']}', which is not a scene or an ending.", 6)
            if "roll" in option:
                check_roll(report, spot, option["roll"], facts)

def check_scene(report, number, scene, facts):
    """Rules 5 to 9 for one scene."""
    where = name_of("scene", scene, "id", number)
    if not check_object(report, where, scene, "a scene"):
        return
    facts["texts"] += [(where, "title", scene["title"]), (where, "place", scene.get("place", ""))]
    check_beats(report, where, scene["beats"], facts)
    check_groups(report, where, scene.get("choices", []), facts)
    exits = [key for key in ("next", "ending", "route") if key in scene]
    if len(exits) != 1:
        problem(report, where, f"a scene needs 1 exit ('next', 'ending' or 'route'), not {len(exits)}.", 5)
    for key, names, kinds in (("next", "scenes", "a scene"), ("ending", "endings", "an ending")):
        if key in scene and scene[key] not in facts[names]:                       # rule 6
            problem(report, where, f"'{key}' names '{scene[key]}', which is not {kinds}.", 6)
    route = scene.get("route", [])
    for number, entry in enumerate(route, start=1):
        place = f"{where}, route entry {number}"
        if not check_object(report, place, entry, "a route entry"):
            continue
        if ("when" in entry) != (number < len(route)):
            problem(report, place, "every entry needs a 'when' but the last, which has none.", 7)
        if "when" in entry:
            check_condition(report, place, entry["when"], facts)
        if entry["to"] not in facts["targets"]:                                   # rule 6
            problem(report, place, f"'to' names '{entry['to']}', which is not a scene or an ending.", 6)

def check_names(report, story, facts):
    """Rules 13, 3 and 4: fields, meters and ids; 'start' names a scene."""
    for number, field in enumerate(story["fields"], start=1):
        where = name_of("field", field, "id", number)
        if check_object(report, where, field, "a field"):
            unique(report, where, facts["fields"], field["id"], "fields")
    for number, meter in enumerate(story.get("meters", []), start=1):
        where = name_of("meter", meter, "id", number)
        if check_object(report, where, meter, "a meter"):
            unique(report, where, facts["meters"], meter["id"], "meters")
            if not meter["min"] <= meter["start"] <= meter["max"]:
                problem(report, where, "the numbers must go min <= start <= max.", 13)
    facts["scenes"] = [scene["id"] for scene in story["scenes"]
                       if isinstance(scene, dict) and isinstance(scene.get("id"), str)]
    facts["endings"] = list(story["endings"])
    facts["targets"] = facts["scenes"] + facts["endings"]
    for item in [story["id"]] + facts["targets"]:
        if not ID_PATTERN.match(item):
            problem(report, "", f"'{item}' is not an id: use a-z, 0-9 and _, starting with a-z.", 3)
    for item in sorted({item for item in facts["targets"] if facts["targets"].count(item) > 1}):
        problem(report, "", f"two scenes or endings use '{item}'. Each needs its own.", 3)
    if story["start"] not in facts["scenes"]:
        problem(report, "", f"'start' names '{story['start']}', which is not a scene.", 4)

def check_shape(report, story):
    """Run the shape rules, 2 to 13. Return the facts the play rules need."""
    facts = {"fields": [], "meters": [], "set_flags": [], "tested_flags": [], "written_values": [],
             "tested_values": [], "texts": [], "resolver": story.get("resolver")}
    if not check_object(report, "", story, "the story"):
        return facts
    facts["texts"] += [("", "title", story["title"]), ("", "subtitle", story.get("subtitle", ""))]
    check_names(report, story, facts)
    for number, scene in enumerate(story["scenes"], start=1):
        check_scene(report, number, scene, facts)
    for ending_id, ending in story["endings"].items():
        where = f"ending '{ending_id}'"
        if check_object(report, where, ending, "an ending"):
            facts["texts"].append((where, "title", ending["title"]))
            check_beats(report, where, ending["beats"], facts)
    for flag, where in facts["tested_flags"]:
        if flag not in facts["set_flags"]:
            problem(report, where, f"flag '{flag}' is tested, but no effect sets it. Check the spelling.", 10)
    written = [(field_id, word) for field_id, word, where in facts["written_values"]]
    for field_id, word, where in facts["tested_values"]:
        if (field_id, word) not in written:
            problem(report, where, f"'{field_id}' is tested for '{word}', but no 'set' writes '{word}'.", 10)
    return facts

# ---------- Part 2: the play rules ----------
def state_key(state):
    """What makes two states play the same: everything but the trail."""
    return (state["scene"], state["group"], tuple(sorted(state["fields"].items())),
            tuple(sorted(state["meters"].items())), tuple(state["flags"]))

def moves(story, state, notes):
    """Every way the game can go on from this state, as (next state, step) pairs."""
    scene = engine.find_scene(story, state["scene"])
    choices = scene.get("choices", [])
    group = engine.current_group(story, state)
    upto = choices.index(group) if group else len(choices)
    for skipped in choices[state["group"]:upto]:               # rule 19: no visible option
        notes["hidden"].add((scene["id"], skipped["key"]))
    if group is None:
        step = {"scene": scene["id"], "group": None, "option": None, "number": None, "needs": None}
        return [(engine.leave_scene(story, state), step)]
    found, role = [], state["fields"].get("role", "")
    for number, option in enumerate(engine.visible(group["options"], state), start=1):
        notes["seen_by"].setdefault((scene["id"], group["key"], option["key"]), set()).add(role)
        results = []
        for rng in (HIGHEST, LOWEST):                          # every result the dice can reach
            new, beats, report = engine.choose(story, state, option["key"], rng)
            needs = None if report is None else report["result"]
            if needs not in results:
                results.append(needs)
                found.append((new, {"scene": scene["id"], "group": group["key"],
                                    "option": option["key"], "number": number, "needs": needs}))
    return found

def explore(story):
    """Breadth-first search: visit every state the game can reach, nearest first."""
    start = engine.new_state(story)
    first = state_key(start)
    notes = {"start": first, "states": {first: start}, "edges": {}, "came_from": {first: None},
             "hidden": set(), "seen_by": {}, "capped": False}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        here = state_key(state)
        notes["edges"][here] = []
        for new, step in [] if engine.is_over(story, state) else moves(story, state, notes):
            there = state_key(new)
            if there not in notes["states"]:
                if len(notes["states"]) >= STATE_CAP:
                    notes["capped"] = True
                    continue
                notes["states"][there] = new
                notes["came_from"][there] = (here, step)     # the first way in is a shortest one
                queue.append(new)
            notes["edges"][here].append((there, step))
    return notes

def endings_from(story, notes):
    """For every state, the endings it can still reach: copy them back along every step until none change."""
    reach = {key: {key[0]} & set(story["endings"]) for key in notes["states"]}
    changed = True
    while changed:
        changed = False
        for here, edges in reversed(list(notes["edges"].items())):
            for there, step in edges:
                if not reach[there] <= reach[here]:
                    reach[here] = reach[here] | reach[there]
                    changed = True
    return reach

def check_stuck_and_decision(report, notes, reach):
    """Rule 16: no spot with no ending left. Rule 17: a group whose options reach different endings."""
    stuck = {there[0] for here, edges in notes["edges"].items() for there, step in edges
             if reach[here] and not reach[there]}
    if not reach[notes["start"]]:
        stuck.add(notes["start"][0])
    for scene_id in sorted(stuck):
        problem(report, f"scene '{scene_id}'", "a player can get here and then never reach an ending.", 16)
    if not stuck:
        ok(report, "no stuck spots: every state can still reach an ending.")
    for here, edges in notes["edges"].items():
        by_option = {}
        for there, step in edges:
            if step["number"] is not None:
                by_option.setdefault(step["option"], set()).update(reach[there])
        if len({frozenset(endings) for endings in by_option.values()}) > 1:
            return ok(report, f"real decision: scene '{here[0]}', group '{edges[0][1]['group']}'.")
    problem(report, "", "no real decision: give one question options that lead to different endings.", 17)

def check_lever(report, story, notes, facts):
    """Rule 18: the lever. Return each role value with the endings it reaches."""
    if "role" not in facts["fields"]:
        problem(report, "", "there is no field 'role', so the story has no lever.", 18)
        return {}
    where, values = f"scene '{story['start']}'", []
    for field_id, word, place in facts["written_values"]:  # 'set' effects in the start scene
        if field_id == "role" and place.startswith(where + ",") and word not in values:
            values.append(word)
    if len(values) < 2:
        problem(report, where, f"the start scene must set 'role' to 2 or 3 values, not {len(values)}.", 18)
    reaches = {}
    for value in values:
        if not [key for key, roles in notes["seen_by"].items() if roles - {""} == {value}]:
            problem(report, "", f"role '{value}' has no option of its own. Give one a 'when' for it.", 18)
        reaches[value] = sorted({state["scene"] for state in notes["states"].values()
                                 if state["fields"]["role"] == value and engine.is_over(story, state)})
        if not reaches[value]:
            problem(report, "", f"role '{value}' cannot reach any ending.", 18)
    if len(values) >= 2:
        ok(report, f"lever: {where} sets role to {' or '.join(values)}.")
    return reaches

def report_routes(report, notes, reaches):
    """For golden runs: what each role reaches, and a shortest way to each ending."""
    for value, endings in reaches.items():
        if endings:
            ok(report, f"role {value} reaches: {', '.join(endings)}")
        for ending_id in endings:
            # States are stored nearest first, so the first match is a shortest way.
            key = [key for key in notes["states"] if key[0] == ending_id and dict(key[2])["role"] == value][0]
            numbers, needs = [], []
            while notes["came_from"][key] is not None:      # walk back to the start
                key, step = notes["came_from"][key]
                if step["number"] is not None:
                    numbers.insert(0, str(step["number"]))
                if step["needs"]:
                    needs.insert(0, step["needs"])
            line = f"shortest way to {ending_id} (role {value}): type {' '.join(numbers)}"
            needs = f" (needs {', '.join(needs)})" if needs else ""
            ok(report, f"{line} ({count(numbers, 'pick')}){needs}")

def check_play(report, story, facts, words):
    """Run rules 14 to 21 by playing every path."""
    notes = explore(story)
    if notes["capped"]:
        warning(report, "", f"stopped after {STATE_CAP:,} states, so rules 14-18 may miss things.", "cap")
    reached = {key[0] for key in notes["states"]}
    for kind, rule in (("scene", 14), ("ending", 15)):
        for item in [item for item in facts[kind + "s"] if item not in reached]:
            problem(report, f"{kind} '{item}'", f"no path reaches this {kind}. Add a way in or cut it.", rule)
    if reached >= set(facts["endings"]):
        ok(report, f"endings reached: {len(facts['endings'])} of {len(facts['endings'])}")
    if not notes["capped"]:
        check_stuck_and_decision(report, notes, endings_from(story, notes))
    reaches = check_lever(report, story, notes, facts)
    for flag in sorted(set(facts["set_flags"]) - {flag for flag, where in facts["tested_flags"]}):
        warning(report, "", f"flag '{flag}' is set but never tested, so it does nothing.", "rule 19")
    for scene_id, group_key in sorted(notes["hidden"]):
        where = f"scene '{scene_id}', group '{group_key}'"
        warning(report, where, "every option can be hidden; then the game skips it.", "rule 19")
    if not 6 <= len(facts["scenes"]) <= 15:
        warning(report, "", f"{count(facts['scenes'], 'scene')}: a final project needs 6 to 15.", "rule 20")
    if len(facts["endings"]) < 3:
        warning(report, "", f"{count(facts['endings'], 'ending')}: a final project needs 3 or more.", "rule 20")
    for word in words:                                     # rule 21
        pattern = re.compile(r"(?<!\w)" + re.escape(word) + r"(?!\w)", re.IGNORECASE)
        for where, kind, text in facts["texts"]:
            if pattern.search(text):
                problem(report, where, f"the {kind} uses the banned word '{word}'.", 21)
    report_routes(report, notes, reaches)
    ok(report, f"the checker explored {len(notes['states'])} states.")

def check_kit(report):
    """Is engine.py still the kit's engine? Does a display break the display rules?"""
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "engine.py"), "rb") as file:
        code = file.read().replace(b"\r\n", b"\n")        # Windows line ends count the same
    if hashlib.sha256(code).hexdigest() == ENGINE_SHA256:
        ok(report, "engine.py matches the kit")
    else:
        warning(report, "", "engine.py has changed since the kit was made. Put the kit's copy back.", "kit")
    leak = re.compile(r"import engine|from engine|choose\(|state\[[^\]]*\]\s*[-+]?=(?!=)")  # section 12
    for name in sorted(os.listdir(folder)):
        if name.startswith("display_") and name.endswith(".py"):
            with open(os.path.join(folder, name), encoding="utf-8") as file:
                if leak.search(file.read()):
                    warning(report, name, "a display must not use the engine or change the state.", "display")

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        sys.exit("Usage: python3 checker.py STORY.json [--banned FILE]")
    report = {"lines": [], "problems": 0, "warnings": 0}
    check_kit(report)
    try:
        story = engine.load_story(sys.argv[1])
        words = []
        if "--banned" in sys.argv:              # one banned word per line; # starts a comment
            with open(sys.argv[sys.argv.index("--banned") + 1], encoding="utf-8") as file:
                words = [line.strip() for line in file if line.strip()[:1] not in ("", "#")]
    except (OSError, IndexError) as error:
        sys.exit(f"Cannot read the files: {error}")
    except ValueError as error:
        story = None
        problem(report, "", f"{error}. Look for a missing comma, quote or bracket there.", 1)
    if story is not None and not isinstance(story, dict):
        problem(report, "", "the file must hold one object { ... } at the top.", 1)
    elif story is not None:
        facts = check_shape(report, story)
        if report["problems"]:
            warning(report, "", "the story was not played, because of the problems above.", "rules 14-21")
        else:
            ok(report, "shape: " + ", ".join(count(facts[kind], kind[:-1]) for kind in
                                             ("scenes", "endings", "fields", "meters")) + ".")
            check_play(report, story, facts, words)
    print("\n".join(report["lines"]))
    result = "FAIL" if report["problems"] else "PASS"
    print(f"RESULT: {result} ({report['problems']} problems, {report['warnings']} warnings)")
    sys.exit(1 if report["problems"] else 0)

if __name__ == "__main__":
    main()
