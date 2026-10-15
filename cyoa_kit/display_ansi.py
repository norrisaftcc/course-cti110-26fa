# CTI 110
# CYOA KIT - Display (ANSI)
# norris
# 10/15/26

# The ANSI display: colour, a typewriter, boxes and meter bars.
# It has the same eleven functions as display_plain.
#
# Effects switch OFF when output is not a terminal, when NO_COLOR is
# set, or when CYOA_EFFECTS=off. Then every function just calls the
# display_plain function, so the output is exactly the plain output.

import os
import re
import sys
import textwrap
import time

import display_plain

WIDTH = 72
DELAY = 0.02                # seconds per character for the typewriter
SETTINGS = {"echo": False}

# One colour per job (a "role"). These are ANSI codes.
COLORS = {
    "border": "36", "system": "36",       # cyan: boxes and messages
    "header": "96",                       # bright cyan: titles
    "speaker": "33",                      # amber: who is talking
    "warning": "93",                      # bright amber: rolls, [final]
    "narration": "97",                    # white: story text
    "sub": "90",                          # grey: small print
    "bold": "1", "dim": "2", "reset": "0",
}

ESCAPE = re.compile(r"\033\[[0-9;]*m")    # matches one colour code

def effects_on():
    """True only for a real terminal with colour allowed."""
    if not sys.stdout.isatty():
        return False
    if os.environ.get("NO_COLOR", "") != "":
        return False
    return os.environ.get("CYOA_EFFECTS", "").lower() != "off"

# ---------- Small helpers ----------
def color(text, role):
    """Wrap text in the colour for this role, then reset."""
    return f"\033[{COLORS[role]}m{text}\033[0m"

def visible_width(text):
    """How wide text looks on screen: colour codes take no room."""
    return len(ESCAPE.sub("", text))

def emphasis(text):
    """Show *word* in bold. Code 22 turns bold off and keeps the colour."""
    return re.sub(r"\*([^*]+)\*", "\033[1m\\1\033[22m", text)

def box(title, lines):
    """Print lines inside a box drawn with box characters."""
    inner = WIDTH - 4
    top = "┌"
    if title:
        top = "┌─ " + title + " "
    print(color(top + "─" * (WIDTH - 1 - visible_width(top)) + "┐", "border"))
    for line in lines:
        for part in textwrap.wrap(line, inner) or [""]:
            pad = " " * (inner - visible_width(part))
            print(color("│ ", "border") + color(part, "narration")
                  + pad + color(" │", "border"))
    print(color("└" + "─" * (WIDTH - 2) + "┘", "border"))

def meter_bar(value, low, high):
    """A bar of 10 blocks: filled blocks for the value, light ones for the rest."""
    filled = 10
    if high > low:
        filled = round((value - low) * 10 / (high - low))
    return "█" * filled + "░" * (10 - filled)

def spaced(text):
    """Letter-space a title: 'THE END' becomes 'T H E   E N D'."""
    return " ".join(text.upper())

def type_out(text, role="narration"):
    """Print text one character at a time.
    It never reads the keyboard, so an answer typed early is kept for the next question."""
    for line in textwrap.wrap(text, WIDTH):
        line = emphasis(line)
        sys.stdout.write(f"\033[{COLORS[role]}m")
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(DELAY)
        print("\033[0m")

def beat_out(beat):
    """One beat: a speaker header, the text, and a boxed screen."""
    print()
    if "speaker" in beat:
        print(color("▌ " + beat["speaker"].upper(), "speaker"))
    type_out(beat["text"])
    if "screen" in beat:
        box("SCREEN", beat["screen"])

# ---------- The eleven display functions ----------
def start(echo):
    """Get ready."""
    SETTINGS["echo"] = echo
    display_plain.start(echo)

def stop():
    """Reset the colours, so the terminal is left clean."""
    if effects_on():
        sys.stdout.write("\033[0m")
        sys.stdout.flush()
    display_plain.stop()

def show_title(story):
    if not effects_on():
        return display_plain.show_title(story)
    lines = [color(spaced(story["title"]), "header")]
    if "subtitle" in story:
        lines.append(color(story["subtitle"], "sub"))
    box("", lines)

def show_scene(scene, beats):
    if not effects_on():
        return display_plain.show_scene(scene, beats)
    print()
    head = "━━ " + scene["title"] + " "
    print(color(head + "━" * (WIDTH - len(head)), "header"))
    if "place" in scene:
        print(color(scene["place"], "sub"))
    show_beats(beats)

def show_beats(beats):
    if not effects_on():
        return display_plain.show_beats(beats)
    for beat in beats:
        beat_out(beat)

def show_roll(report):
    if not effects_on():
        return display_plain.show_roll(report)
    sign = "+d" if report["dice"] == "4dF" else "d"        # Fate dice show -1, +0, +1
    faces = " ".join(format(face, sign) for face in report["faces"])
    print()
    print(color(f"⚄ {report['dice']}  [ {faces} ]  + {report['add']} "
                f"{report['bonus']} = {report['total']}  vs {report['vs']}  → ", "warning")
          + color(report["result"].upper(), "bold"))

def show_status(story, state):
    if not effects_on():
        return display_plain.show_status(story, state)
    parts = []
    for meter in story.get("meters", []):
        if meter.get("hud", True):
            value = state["meters"][meter["id"]]
            bar = meter_bar(value, meter["min"], meter["max"])
            parts.append(f"{meter['label']} {bar} {value}/{meter['max']}")
    for field in story["fields"]:
        if state["fields"][field["id"]] != "":
            parts.append(f"{field['label']}: {state['fields'][field['id']]}")
    if parts:
        print()
        print(color("  │  ".join(parts), "system"))

def show_choices(group, options):
    if not effects_on():
        return display_plain.show_choices(group, options)
    mark = color("[plan]", "system")
    if group["gate"] == "exec":
        mark = color("[final]", "warning")
    print()
    print(color(group["ask"], "header") + " " + mark)
    for number, option in enumerate(options, start=1):
        print(color(f"  {number}. ", "bold") + color(option["label"], "narration"))
        if "sub" in option:
            print(color("     " + option["sub"], "sub"))

def ask(prompt):
    if not effects_on():
        return display_plain.ask(prompt)
    sys.stdout.write(color(prompt, "bold"))
    sys.stdout.flush()
    try:
        answer = input()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"
    if SETTINGS["echo"]:
        print(answer)
    return answer.strip()

def show_message(text):
    if not effects_on():
        return display_plain.show_message(text)
    print(color(text, "system"))

def show_ending(ending, beats, state):
    if not effects_on():
        return display_plain.show_ending(ending, beats, state)
    print()
    box("", [color(spaced(ending["title"]), "header")])
    show_beats(beats)
    print()
    print(color(spaced("The End"), "warning"))
    print(color("Trail: " + " → ".join(state["trail"]), "sub"))
