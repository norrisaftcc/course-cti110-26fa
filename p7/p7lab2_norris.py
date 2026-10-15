# CTI 110
# P7LAB2 - Load a Story
# norris
# 11/12/26

# The story leaves the Python. It lives in toy_story.json, as data.
# This short version follows only "to", "next" and "ending".
# No "route", no "effects", no "when": the kit's engine.py does those.

import json


# Loop over the list of scenes. Return the one with this id, or None.
def find_scene(story, scene_id):
    for scene in story["scenes"]:
        if scene["id"] == scene_id:
            return scene
    return None


# Print each beat's text. NOTE: this shows EVERY beat, even one with a
# "when". We keep no state, so we cannot test a "when". The kit can.
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
        if "sub" in option:
            print(f"     {option['sub']}")
    # INPUT -- validate with a while loop, as in P4LAB2
    pick = input(f"Pick 1-{number}: ").strip()
    while not pick.isdigit() or int(pick) < 1 or int(pick) > number:
        print("That is not on the list.")
        pick = input(f"Pick 1-{number}: ").strip()
    return group["options"][int(pick) - 1]     # people count from 1, lists from 0


def main():
    # Run this from inside the p7 folder: cd p7
    story = json.load(open("toy_story.json"))
    print(story["title"])

    scene = find_scene(story, story["start"])
    while scene != None:
        print()
        print(scene["title"])
        show_beats(scene["beats"])

        # Ask each choice group in order. An option with "to" leaves early.
        target = ""
        if "choices" in scene:
            for group in scene["choices"]:
                if target == "":
                    option = pick_option(group)
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
        if target in story["endings"]:
            ending = story["endings"][target]
            print()
            print(ending["title"])
            show_beats(ending["beats"])
            print("THE END")
            scene = None
        else:
            scene = find_scene(story, target)


# at the bottom -- start the program
main()
