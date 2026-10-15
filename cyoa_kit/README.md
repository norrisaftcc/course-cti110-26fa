# The CYOA Kit

This kit plays choose-your-own-adventure stories in the console. A story is one file, `story.json`. The kit reads the file and plays it. You write the story. The kit does the rest.

**One rule, one home.** The story lives in `story.json`, not in the Python.

The kit needs Python 3.10 or newer. It uses the standard library only. There is nothing to install.

---

## What is in the kit

| File | What it does | In your final, you may |
|---|---|---|
| `engine.py` | The rules: conditions, effects, dice, moving between scenes, save and load. It never prints. | **Not change it.** The checker tells you if it changed. |
| `checker.py` | Checks a story before anyone plays it. | **Not change it.** |
| `tests/run_tests.py` | Runs every test. | **Not change it.** |
| `game.py` | The play loop: show a scene, ask, hand the answer to the engine. | Change it. |
| `display_plain.py` | Plain text. Its output is what the tests compare. | Change it. |
| `display_ansi.py` | Colour, a typewriter, boxes and meter bars. | Change it. |
| `display_curses.py` | A full-screen display. | Change it. |
| your own `.py` files | A new feature, a new display. | Add them. |
| `stories/` | `toy.json`, `fort.json`, `dead_drop.json`, and two worked blueprints. | Add your story here. |
| `tests/` | Golden runs (`.in` and `.out`), engine checks, and stories broken on purpose. | Add your golden runs here. |

---

## Play a story

Run these from inside the `cyoa_kit` folder.

```
python3 game.py stories/toy.json
python3 game.py stories/fort.json
python3 game.py stories/dead_drop.json --display ansi
```

On Windows, type `python` or `py` where this page says `python3`.

| Option | What it does |
|---|---|
| `--display plain` | Plain text. This is the default. |
| `--display ansi` | Colour, a typewriter, boxes and meter bars. |
| `--display curses` | A full-screen display. See the note below. |
| `--seed 7` | Use dice seed 7. The same seed and the same answers always give the same game. |
| `--echo` | Print each answer after its prompt. Use it when you pipe in a file of answers. |

If you give no seed, the game picks one and prints it: `Seed: 4821. Replay with --seed 4821.`

You can also set the display and the seed with environment variables: `CYOA_DISPLAY=ansi` and `SEED=7`.

### The keys

| Type | What happens |
|---|---|
| `1`, `2`, `3` ... | Pick that choice. Only the choices you can see have numbers. |
| `s` | Save the game to `save_<story id>.json` in this folder. |
| `l` | Load that save and show the scene again. |
| `r` | Restart from the first scene. |
| `h` | Show the keys. |
| `q` | Quit. Ctrl+C quits too. |

Upper case and lower case both work. At an ending, type `r` to play again or `q` to quit.

### Colour and effects

The ANSI display turns its effects **off** when:

- the output is not a terminal (for example, you pipe it into a file),
- the environment variable `NO_COLOR` is set to anything, or
- `CYOA_EFFECTS=off` is set.

With effects off, it prints exactly what the plain display prints. That is why the tests can run it too.

### The curses display

`curses` comes with Python on macOS, Linux and GitHub Codespaces. On Windows, install it first:

```
pip install windows-curses
```

If Python cannot load curses, or the output is not a terminal, the game uses the plain display. It prints one line that says why.

---

## Check a story

```
python3 checker.py stories/fort.json
python3 checker.py stories/my_story.json --banned banned_words.txt
```

Every line starts with `OK`, `WARNING` or `PROBLEM`. A problem names the scene, the group, the option and the rule number. For example:

```
PROBLEM scene 'yard', group 'well', option 'climb': 'to' names 'tresure', which is not a scene or an ending. (rule 6)
```

The last line is `RESULT: PASS` or `RESULT: FAIL`. Fix every problem. Read every warning.

The checker plays every path through your story. It also prints lines you can use for golden runs:

```
OK shortest way to treasure (role fighter): type 1 1 1 (3 picks)
```

Those numbers are the numbers you type. If the way goes through a dice roll, the line says `(needs success)` or `(needs fail)`. Try seeds until the roll goes that way.

A banned-words file has one word per line. Lines that start with `#` are notes.

---

## Run the tests

```
python3 tests/run_tests.py
```

Each test prints `PASS` or `FAIL`. The run ends with `ALL TESTS PASSED` or `N TESTS FAILED`.

| Test | What it checks |
|---|---|
| Golden runs | Every `tests/*.in` file is played, and the output must match its `.out` file exactly. Each one runs twice: with the plain display and with the ANSI display (piped, so its effects are off). |
| Story checks | The checker on every story in `stories/` must match `tests/check_<story id>.out`. |
| Broken stories | The checker on every story in `tests/broken/` must match its `.out` file. |
| Engine checks | The functions in `tests/test_engine.py`. |
| Kit rules | No kit file uses `class` or `global`. The curses display runs in a pretend terminal (skipped on Windows). |

### Golden runs

A golden run is a file of typed answers, and the exact output they make.

- `tests/<name>.in` holds the answers, one per line. The first line says which story and which seed: `# story: stories/my_story.json seed: 1`. Other lines that start with `#` are notes.
- `tests/<name>.out` holds the output.

For your final, make one golden run for each ending you claim. Name it `tests/story_<ending id>.in`.

### When you change the output on purpose

If you change what the game prints (a new display, new words in your story), the old `.out` files no longer match. Rewrite them:

```
python3 tests/run_tests.py --regen
```

Then read the diff (`git diff tests/`). Check that every change is one you meant. Then run the tests again without `--regen`.

---

## The rules of the story file

The full contract is **STORY-FORMAT.md**. It is in this folder: `cyoa_kit/STORY-FORMAT.md`. It says what every key in `story.json` means, how the lever works, how dice work, and what each checker rule checks. When this README and STORY-FORMAT.md disagree, STORY-FORMAT.md wins.
