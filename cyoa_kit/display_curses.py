# CTI 110
# CYOA KIT - Display (curses)
# norris
# 10/15/26

# A full-screen display with curses. Same eleven functions as display_plain.
#
#   +--------------------------------------+
#   | story text scrolls here              |   the text window
#   |                                      |
#   | Exposure 3/6  |  Role: hacker        |   the status line
#   | > _                                  |   the input line
#   +--------------------------------------+
#
# curses comes with Python on macOS, Linux and Codespaces.
# On Windows, first run:  pip install windows-curses
# game.py only uses this display when output is a real terminal.

import curses
import locale
import textwrap

# Everything this display needs to remember. A dict, so no 'global'.
SCREEN = {"main": None, "text": None, "status": None, "input": None, "lines": 0}

# ---------- Setting up and putting back ----------

def start(echo):
    """Take over the terminal and make the three windows."""
    locale.setlocale(locale.LC_ALL, "")          # lets curses draw Unicode
    main = curses.initscr()
    SCREEN["main"] = main               # echo is not needed: answers always show
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)     # titles
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # speakers
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)     # status line
    height, width = main.getmaxyx()
    SCREEN["text"] = curses.newwin(height - 2, width, 0, 0)
    SCREEN["text"].scrollok(True)
    SCREEN["status"] = curses.newwin(1, width, height - 2, 0)
    SCREEN["input"] = curses.newwin(1, width, height - 1, 0)
    SCREEN["text"].refresh()

def stop():
    """Always give the terminal back, even after an error."""
    if SCREEN["main"] is None:
        return
    try:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    except curses.error:
        pass
    SCREEN["main"] = None

# ---------- Small helpers ----------

def style(name):
    """The curses attribute for a kind of text."""
    if name == "plain":
        return curses.A_NORMAL
    if not curses.has_colors():
        return curses.A_BOLD
    if name == "title":
        return curses.color_pair(1) | curses.A_BOLD
    if name == "speaker":
        return curses.color_pair(2) | curses.A_BOLD
    if name == "dim":
        return curses.A_DIM
    return curses.A_NORMAL

def wait_for_key():
    """Pause when a screen is full, so no text scrolls away unread."""
    line = SCREEN["input"]
    line.erase()
    put(line, "-- more: press any key --", curses.A_REVERSE)
    line.refresh()
    line.getch()
    SCREEN["lines"] = 0

def put(window, text, attribute):
    """Draw text and ignore the error curses gives at the last corner."""
    try:
        window.addstr(text, attribute)
    except curses.error:
        pass

def add_line(text, name="plain"):
    """Add one line to the text window. Long text is wrapped first."""
    window = SCREEN["text"]
    height, width = window.getmaxyx()
    for part in textwrap.wrap(text, width - 1) or [""]:
        if SCREEN["lines"] >= height - 1:
            wait_for_key()
        put(window, part + "\n", style(name))
        SCREEN["lines"] = SCREEN["lines"] + 1
    window.refresh()

def add_beat(beat):
    """One beat: a speaker name, the text, and the screen lines in a frame."""
    add_line("")
    if "speaker" in beat:
        add_line(beat["speaker"].upper(), "speaker")
    add_line(beat["text"])
    for line in beat.get("screen", []):
        add_line("  | " + line, "title")

# ---------- The eleven display functions ----------

def show_title(story):
    add_line("")
    add_line(" ".join(story["title"].upper()), "title")
    if "subtitle" in story:
        add_line(story["subtitle"], "dim")

def show_scene(scene, beats):
    add_line("")
    add_line("== " + scene["title"] + " ==", "title")
    if "place" in scene:
        add_line(scene["place"], "dim")
    show_beats(beats)

def show_beats(beats):
    for beat in beats:
        add_beat(beat)

def show_roll(report):
    faces = ", ".join(str(face) for face in report["faces"])
    add_line("")
    add_line(f"Roll {report['dice']} [{faces}] + {report['add']} {report['bonus']}"
             f" = {report['total']} vs {report['vs']}: {report['result'].upper()}",
             "speaker")

def show_status(story, state):
    """Draw the status line: meters and fields."""
    parts = []
    for meter in story.get("meters", []):
        if meter.get("hud", True):
            parts.append(f"{meter['label']} {state['meters'][meter['id']]}/{meter['max']}")
    for field in story["fields"]:
        if state["fields"][field["id"]] != "":
            parts.append(f"{field['label']}: {state['fields'][field['id']]}")
    line = SCREEN["status"]
    width = line.getmaxyx()[1]
    line.erase()
    line.bkgd(" ", style("plain") | curses.A_REVERSE)
    put(line, (" " + "  |  ".join(parts))[:width - 1], curses.A_REVERSE)
    line.refresh()

def show_choices(group, options):
    mark = "[plan]"
    if group["gate"] == "exec":
        mark = "[final]"
    add_line("")
    add_line(group["ask"] + " " + mark, "title")
    for number, option in enumerate(options, start=1):
        add_line(f"  {number}. {option['label']}")
        if "sub" in option:
            add_line("     " + option["sub"], "dim")

def ask(prompt):
    """Read one line on the input line. Ctrl+C counts as 'q'."""
    line = SCREEN["input"]
    line.erase()
    put(line, prompt, curses.A_BOLD)
    line.refresh()
    SCREEN["lines"] = 0
    curses.echo()                       # show the keys as they are typed
    try:
        answer = line.getstr().decode("utf-8", "replace")
    except KeyboardInterrupt:
        answer = "q"
    finally:
        curses.noecho()
    add_line(prompt + answer)           # keep the answer in the story text
    return answer.strip()

def show_message(text):
    add_line(text, "speaker")

def show_ending(ending, beats, state):
    add_line("")
    add_line(" ".join(ending["title"].upper()), "title")
    show_beats(beats)
    add_line("")
    add_line("T H E   E N D", "title")
    add_line("Trail: " + " > ".join(state["trail"]), "dim")
