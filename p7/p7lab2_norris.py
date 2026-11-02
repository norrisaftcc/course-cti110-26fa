# CTI 110
# P7LAB2 - Load a Story
# norris
# 11/12/26

# The story leaves the Python. It lives in toy_story.json, as data.
# This short version follows only "to", "next" and "ending".
# No "route", no "effects", no "when": the kit's engine.py does those.

# WHAT THIS TEACHES
#   - JSON: a text format for dicts, lists, strings and numbers.
#     json.load() turns a JSON file into the Python dict you already know.
#   - Separating DATA from CODE: to change the story, edit the JSON. This
#     program does not change. Writers and programmers can work apart.
#   - Walking a data structure with loops: scenes -> choice groups -> options.
#   - A small state machine: a scene points to its next scene (or ending),
#     and a loop follows the pointers until an ending is reached.
#   - Honest limits. This is the SHORT version. Its limits are marked below.
#     The kit's engine.py shows how a real one handles them.
#
# The shape of toy_story.json (only the parts used here):
#   "title", "start", "endings": {id: {"title", "beats"}}
#   "scenes": [ {"id", "title", "beats": [{"text"}],
#                "choices": [ {"ask", "options": [{"label", "sub",
#                                                  "then", "to"}]} ],
#                "next" OR "ending"} ]
# A scene with choices can end early with an option's "to". Otherwise it
# falls through to its own "next" or "ending".

import json


# Loop over the list of scenes. Return the one with this id, or None.
# None is Python's "nothing here". The caller must be ready for it.
def find_scene(story, scene_id):
    for scene in story["scenes"]:
        if scene["id"] == scene_id:
            return scene       # return leaves the loop AND the function
    return None


# Print each beat's text. NOTE: this shows EVERY beat, even one with a
# "when". We keep no state, so we cannot test a "when". The kit can.
# A "beat" is one paragraph of the story.
def show_beats(beats):
    for beat in beats:
        print(beat["text"])


# Number ALL the options in one group and return the one picked.
# ON PURPOSE this IGNORES "when". The kit hides an option whose "when" is
# false. Here every option shows, so a Wizard can "Lift the stone lid".
def pick_option(group):
    print()
    print(group["ask"])
    number = 0
    for option in group["options"]:
        number = number + 1
        print(f"  {number}. {option['label']}")
        # "sub" is optional. Test with "in" before reading it, or a missing
        # key would raise a KeyError.
        if "sub" in option:
            print(f"     {option['sub']}")
    # INPUT -- validate with a while loop, as in P4LAB2
    # Order matters in the test: isdigit() runs first. If it is False, the
    # "or" stops there, so int() never sees text like "abc" and cannot crash.
    pick = input(f"Pick 1-{number}: ").strip()
    while not pick.isdigit() or int(pick) < 1 or int(pick) > number:
        print("That is not on the list.")
        pick = input(f"Pick 1-{number}: ").strip()
    return group["options"][int(pick) - 1]     # people count from 1, lists from 0


def main():
    # Run this from inside the p7 folder: cd p7
    # (The path is relative, so Python looks in the folder you ran it from.)
    # open() with no close is fine for a short script. p7lab3 shows the
    # tidier "with" form, which closes the file for you.
    story = json.load(open("toy_story.json"))
    print(story["title"])

    scene = find_scene(story, story["start"])
    # Loop until scene is None. An ending sets it to None to stop the loop.
    while scene != None:
        print()
        print(scene["title"])
        show_beats(scene["beats"])

        # Ask each choice group in order. An option with "to" leaves early.
        # target stays "" until some option or exit names where to go.
        target = ""
        if "choices" in scene:
            for group in scene["choices"]:
                if target == "":
                    option = pick_option(group)
                    # "then" is text that appears right after the pick.
                    if "then" in option:
                        show_beats(option["then"])
                    if "to" in option:
                        target = option["to"]

        # The groups are done. No "to"? Then follow the scene's own exit.
        if target == "":
            if "next" in scene:
                target = scene["next"]
            else:
                target = scene["ending"]

        # The target is a scene id or an ending id (endings have their own dict)
        # "in" on a dict tests the KEYS. So this asks: is it an ending's id?
        if target in story["endings"]:
            ending = story["endings"][target]
            print()
            print(ending["title"])
            show_beats(ending["beats"])
            print("THE END")
            scene = None          # None ends the while loop above
        else:
            scene = find_scene(story, target)


# at the bottom -- start the program
main()
