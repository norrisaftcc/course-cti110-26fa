# CTI 110
# CYOA KIT - Display (plain)
# norris
# 10/15/26

# The plain display: ASCII text, wrapped at 72 columns. It only SHOWS
# things and READS answers; it never changes the state or decides a rule.
# Its output is the reference for every tests/*.out file: keep it stable.

import textwrap

WIDTH = 72
SETTINGS = {"echo": False}      # a dict, so functions can change it without 'global'

# Some story text uses fancy characters. Plain output is ASCII only.
ASCII_SWAPS = {"\u2014": "--", "\u2013": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
               "\u2026": "...", "\u00d7": "x", "\u00b7": "-", "\u2022": "*", "\u2212": "-", "\u00a0": " "}

def to_ascii(text):
    """Swap fancy characters for plain ones. Anything else unknown becomes '?'."""
    for fancy, plain in ASCII_SWAPS.items():
        text = text.replace(fancy, plain)
    return text.encode("ascii", "replace").decode("ascii")

def say(text, indent=""):
    """Print text wrapped at 72 columns, every line starting with indent."""
    lines = textwrap.wrap(to_ascii(text), WIDTH, initial_indent=indent, subsequent_indent=indent)
    if not lines:                   # an empty line still shows its indent
        lines = [indent.rstrip()]
    for line in lines:
        print(line)

def show_beat(beat):
    """Print one beat: an optional speaker, the text, an optional screen."""
    print()
    speaker = ""
    if "speaker" in beat:
        speaker = beat["speaker"].upper() + ": "     # chen -> CHEN:
    say(speaker + beat["text"])
    for line in beat.get("screen", []):
        say(line, "  | ")

def start(echo):
    """Get ready. With echo on, ask() prints each answer it reads."""
    SETTINGS["echo"] = echo

def stop():
    """Nothing to clean up for plain text."""

def show_title(story):
    """The story's title, and its subtitle if it has one."""
    print()
    print("=" * WIDTH)
    say(story["title"].upper(), "  ")
    if "subtitle" in story:
        say(story["subtitle"], "  ")
    print("=" * WIDTH)

def show_scene(scene, beats):
    """The scene's title, its place, then its beats."""
    print()
    say("== " + scene["title"] + " ==")
    if "place" in scene:
        say("(" + scene["place"] + ")")
    show_beats(beats)

def show_beats(beats):
    """Each beat as its own paragraph."""
    for beat in beats:
        show_beat(beat)

def show_roll(report):
    """One line: the dice, the faces, the bonus, the total and the result."""
    faces = ", ".join(str(face) for face in report["faces"])
    print()
    say(f"Roll {report['dice']} [{faces}] + {report['add']} {report['bonus']}"
        f" = {report['total']} vs {report['vs']}: {report['result'].upper()}")

def show_status(story, state):
    """Meters (unless hud is false), then the fields that are filled in."""
    meters = []
    for meter in story.get("meters", []):
        if meter.get("hud", True):
            meters.append(f"{meter['label']} {state['meters'][meter['id']]}/{meter['max']}")
    fields = []
    for field in story["fields"]:
        if state["fields"][field["id"]] != "":
            fields.append(f"{field['label']}: {state['fields'][field['id']]}")
    parts = [part for part in ("  ".join(meters), "  ".join(fields)) if part != ""]
    if parts:
        print()
        say("  |  ".join(parts))         # Exposure 3/6  Nerves 1/4  |  Role: hacker

def show_choices(group, options):
    """The question, its gate mark, then the options numbered from 1."""
    mark = "[plan]"
    if group["gate"] == "exec":
        mark = "[final]"
    print()
    say(group["ask"] + " " + mark)
    for number, option in enumerate(options, start=1):
        say(f"{number}. {option['label']}", "  ")
        if "sub" in option:
            say(option["sub"], "     ")

def ask(prompt):
    """Read one answer. End of input or Ctrl+C counts as 'q'."""
    try:
        answer = input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"
    if SETTINGS["echo"]:
        print(answer)
    return answer.strip()

def show_message(text):
    """One short line: an error, 'Saved.', or the help."""
    say(text)

def show_ending(ending, beats, state):
    """The ending's title, its beats, THE END, and the trail."""
    print()
    print("*" * WIDTH)
    say(ending["title"].upper(), "  ")
    print("*" * WIDTH)
    show_beats(beats)
    print()
    print("THE END")
    say("Trail: " + " > ".join(state["trail"]))
