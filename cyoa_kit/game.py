# CTI 110
# CYOA KIT - Game
# norris
# 10/15/26

# The console: it shows a scene, asks a question, and hands the answer
# to the engine. It holds no rules and no story text.
#
#   python3 game.py stories/toy.json
#   python3 game.py stories/toy.json --display ansi --seed 7
#   python3 game.py stories/toy.json --seed 1 --echo < tests/toy_walk_away.in

import os
import random
import sys

import engine

USAGE = "Usage: python3 game.py STORY.json [--display plain|ansi|curses] [--seed N] [--echo]"
HELP = "Keys: a number picks. s save, l load, r restart, h help, q quit."

# ---------- Setting up ----------
def read_options(argv):
    """Read the command line into a dict of options."""
    options = {"story": None, "display": os.environ.get("CYOA_DISPLAY", "plain"),
               "seed": os.environ.get("SEED"), "echo": False}
    index = 0
    while index < len(argv):
        word = argv[index]
        if word == "--echo":
            options["echo"] = True
        elif word in ("--display", "--seed") and index + 1 < len(argv):
            options[word[2:]] = argv[index + 1]       # "--seed" -> "seed"
            index = index + 1
        elif options["story"] is None and not word.startswith("--"):
            options["story"] = word
        else:
            sys.exit(f"I do not understand '{word}'.\n{USAGE}")
        index = index + 1
    if options["story"] is None:
        sys.exit(USAGE)
    if options["display"] not in ("plain", "ansi", "curses"):
        sys.exit(f"--display must be plain, ansi or curses.\n{USAGE}")
    # The seed: from --seed, else from SEED, else a new one we print.
    options["picked"] = options["seed"] is None
    if options["picked"]:
        options["seed"] = random.randint(1, 99999)
    elif not str(options["seed"]).isdigit():
        sys.exit(f"The seed must be a whole number.\n{USAGE}")
    options["seed"] = int(options["seed"])
    return options

def pick_display(name):
    """Import the display module with this name. Curses may fall back to plain."""
    if name == "ansi":
        import display_ansi
        return display_ansi
    if name == "curses":
        if not sys.stdout.isatty():
            reason = "curses needs a terminal, and output is not a terminal"
        else:
            try:
                import display_curses
                return display_curses
            except ImportError:
                reason = "Python cannot load curses (on Windows: pip install windows-curses)"
        print(f"Using the plain display: {reason}.", file=sys.stderr)
    import display_plain
    return display_plain

# ---------- Small steps of the play loop ----------
def show_place(story, state, display):
    """Show the scene the player is in. (An ending is shown by the loop.)"""
    if not engine.is_over(story, state):
        scene = engine.find_scene(story, state["scene"])
        display.show_scene(scene, engine.visible(scene["beats"], state))

def restart(story, display):
    """Start a new game: the title, then the first scene."""
    display.show_title(story)
    state = engine.new_state(story)
    show_place(story, state, display)
    return state

def take_pick(story, state, option, rng, display):
    """Hand one pick to the engine, then show what happened."""
    new_state, beats, report = engine.choose(story, state, option["key"], rng)
    if report is not None:
        display.show_roll(report)
    display.show_beats(beats)
    if len(new_state["trail"]) > len(state["trail"]):     # the pick moved us
        show_place(story, new_state, display)
    return new_state

def save(story, state, display):
    """Save the game to save_<story id>.json in this folder."""
    path = f"save_{story['id']}.json"
    try:
        engine.save_game(state, path)
        display.show_message(f"Saved to {path}.")
    except OSError as error:
        display.show_message(f"Could not save: {error}")

def load(story, state, display):
    """Load the saved game. If that fails, keep playing where we are."""
    path = f"save_{story['id']}.json"
    try:
        loaded = engine.load_game(story, path)
    except FileNotFoundError:
        display.show_message("There is no save yet. Type s to save first.")
        return state
    except (OSError, ValueError) as error:
        display.show_message(f"Could not load: {error}")
        return state
    display.show_message(f"Loaded {path}.")
    show_place(story, loaded, display)
    return loaded

def handle_answer(story, state, answer, options, rng, display):
    """Act on one answer at a question. Return the state to play on."""
    if answer.isdecimal() and 1 <= int(answer) <= len(options):     # isdecimal: digits only
        return take_pick(story, state, options[int(answer) - 1], rng, display)
    if answer == "s":
        save(story, state, display)
    elif answer == "l":
        return load(story, state, display)
    elif answer == "r":
        return restart(story, display)
    elif answer == "h":
        display.show_message(HELP)
    else:
        display.show_message(f"Choose 1-{len(options)}, or s, l, r, h, q.")
    return state

def ending_turn(story, state, display):
    """Show the ending, then ask until the player types r or q. True means restart."""
    ending = engine.get_ending(story, state)
    display.show_ending(ending, engine.visible(ending["beats"], state), state)
    while True:
        answer = display.ask("r = play again, q = quit > ").lower()
        if answer in ("r", "q"):
            return answer == "r"
        display.show_message("Type r to play again, or q to quit.")

# ---------- The play loop ----------
def play(story, display, seed, picked):
    """Play the story until the player quits."""
    rng = engine.make_rng(seed)
    display.show_title(story)
    replay = f". Replay with --seed {seed}." if picked else ""     # only when we chose the seed
    display.show_message(f"Seed: {seed}{replay}")
    state = engine.new_state(story)
    show_place(story, state, display)
    while True:
        # Step 1. At an ending: show it, then restart or quit.
        if engine.is_over(story, state):
            if not ending_turn(story, state, display):
                return
            state = restart(story, display)
            continue
        # Step 2. No question left in this scene: leave it.
        group = engine.current_group(story, state)
        if group is None:
            state = engine.leave_scene(story, state)
            show_place(story, state, display)
            continue
        # Step 3. Show the status and the question, then read an answer.
        options = engine.visible(group["options"], state)
        display.show_status(story, state)
        display.show_choices(group, options)
        answer = display.ask("> ").lower()
        # Step 4. Quit, or act on the answer.
        if answer == "q":
            return
        state = handle_answer(story, state, answer, options, rng, display)

def main():
    """Read the options, load the story, play, and always clean up."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")    # lets Windows print Unicode
    except (AttributeError, OSError, ValueError):
        pass
    options = read_options(sys.argv[1:])
    try:
        story = engine.load_story(options["story"])
    except (OSError, ValueError) as error:
        sys.exit(f"Cannot load the story: {error}")
    display = pick_display(options["display"])
    try:
        display.start(options["echo"])
    except Exception as error:                      # e.g. curses cannot use this terminal
        display.stop()                              # put the screen back first
        print(f"Using the plain display: {display.__name__} could not start ({error}).",
              file=sys.stderr)
        display = pick_display("plain")
        display.start(options["echo"])
    try:
        play(story, display, options["seed"], options["picked"])
    except KeyboardInterrupt:
        pass                                        # Ctrl+C: quit cleanly
    finally:
        display.stop()                              # always put the screen back
    print("Goodbye.")

if __name__ == "__main__":
    main()
