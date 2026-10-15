# Story Format: The Contract

This file is the contract for the CTI 110 story unit. Every story file, the engine, the three display modules, the checker, the tests, the lessons and the AI tutor follow it. If another file disagrees with this one, this file wins. A builder who needs a change stops and reports it. The instructor changes this file first, then the code.

The reader of most of this file is a builder or the instructor. Students read sections 1 to 8. Sections 9 to 12 are for the people who build the kit.

---

## 1. One story, one file

A story is one JSON file, `story.json`. It holds every word of the game and every rule of the game's world. It holds no code.

The engine reads the file and plays it. You never change the engine. You change the story.

| Layer | File | Owns | May **not** |
|---|---|---|---|
| Story (data) | `stories/<name>.json` | Every scene, choice, ending, field, meter and flag. All game text. | Hold code. Hold comments (JSON has none; put notes in your blueprint). |
| Engine (rules) | `engine.py` | Conditions, effects, dice, moving between scenes, save and load. | Call `print` or `input`. Hold game text. Know a scene id. |
| Display (screen) | `display_plain.py`, `display_ansi.py`, `display_curses.py` | How text, choices and meters look. Reading what the player types. | Import `engine`. Change the state. Decide which choices show. |
| Console (glue) | `game.py` | The play loop: show, ask, pass the pick to the engine, save, load, restart, quit. | Decide a rule. Hold game text. |

**One rule, one home.** The story lives in `story.json`, not in the Python.

---

## 2. Where this format comes from

The format is a strict subset of the **Stage** script schema (`stage/SPEC.md`, section 2, in the Fort on the Lake repository, main at `169ee8f`). The Stage is a visual-novel engine. *The Dead Drop* (High Tech, Low Lives) is a Stage pack.

"Strict subset" means:

- Every key in a story file is a Stage key, with the same spelling and the same meaning.
- A story file is the Stage's `pack.json` and `script.json` merged into one file, minus the art, notes and motion keys.
- A story file is **not** a drop-in Stage pack. The Stage also needs keys that are about art and the web page. A converter (not part of this unit) adds them. Section 13 lists them.

Key names are copied exactly from the Stage spec. Do not rename them, even when a plainer word exists.

---

## 3. The top level

```json
{
  "id": "toy",
  "title": "The Locked Gate",
  "start": "gate",
  "fields": [ { "id": "role", "label": "Role" } ],
  "scenes": [ ... ],
  "endings": { ... }
}
```

| Key | Required | Type | Stage home | What it is |
|---|---|---|---|---|
| `id` | Yes | text | `pack.json` `id` | The story's short name: lowercase letters, digits, `_`. The save file uses it. |
| `title` | Yes | text | `pack.json` `title` | The name on the title screen. |
| `subtitle` | No | text | `pack.json` `subtitle` | One line under the title. |
| `start` | Yes | scene id | `pack.json` `start` | The first scene. |
| `fields` | Yes | list | `pack.json` `fields` | The character sheet. Words the story writes down. See section 5. |
| `meters` | No | list | `pack.json` `meters` | Numbers that go up and down. See section 5. |
| `resolver` | Only if a roll is used | `"ose"` or `"fate4df"` | `pack.json` `resolver` | How dice are read. See section 8. |
| `scenes` | Yes | list | `script.json` `scenes` | The scenes, in any order. |
| `endings` | Yes | object | `script.json` `endings` | The endings, keyed by ending id. |

No other key is allowed. The checker reports any other key as a problem, so a typo such as `"sceens"` is caught.

**Ids.** Scene ids and ending ids share one name space: no scene may have the same id as an ending. An id is lowercase letters, digits and `_`, and starts with a letter: `jetty`, `c2`, `oil_store`. Use the id, never the title, to name a place.

---

## 4. Scenes, beats, choices, options, endings

### 4.1 Scene

```json
{
  "id": "yard",
  "title": "The Yard",
  "place": "Behind the gate",
  "beats": [ { "text": "Past the gate, a dark well." } ],
  "choices": [ ... ],
  "next": "gate"
}
```

| Key | Required | What it is |
|---|---|---|
| `id` | Yes | The scene id. |
| `title` | Yes | The scene's name, shown as a heading. |
| `place` | No | A small line under the title: where and when. |
| `beats` | Yes, at least one | The text of the scene, in order. |
| `choices` | No | Zero or more choice groups, asked in order after the beats. |
| `next` | Exactly one of these three | Go to this scene when the choices are done. |
| `ending` | | Go to this ending when the choices are done. |
| `route` | | A list of `{ "when": condition, "to": id }`. The first entry whose condition is true wins. The **last** entry has no `when`; it is the default. |

Every scene needs exactly one exit (`next`, `ending` or `route`), even when every option leaves with `to`. The Stage grammar needs it, and it is your safety net.

### 4.2 Beat

```json
{ "text": "Your lamp shows a ladder inside the well.", "when": { "flag": "lamp" } }
```

| Key | Required | What it is |
|---|---|---|
| `text` | Yes | Plain text. `*word*` marks emphasis; it is the only markup. |
| `speaker` | No | Who says this line: a short lowercase id such as `chen` or `g0`. The display prints it as a name. |
| `when` | No | Show this beat only when the condition is true. |
| `screen` | No | A list of short text lines shown on an in-world screen (a phone, a terminal). The display draws a box around them. |

### 4.3 Choice group

A choice group is one question with its answers.

```json
{
  "key": "well",
  "ask": "What do you do at the well?",
  "gate": "exec",
  "options": [ ... ]
}
```

| Key | Required | What it is |
|---|---|---|
| `key` | Yes | A short id, unique inside the scene. |
| `ask` | Yes | The question the player sees. |
| `gate` | Yes | `"plan"` or `"exec"`. |
| `options` | Yes, at least one | The answers. |

**The gate.** Old-school play splits every choice in two kinds. **Plan** is talk, looking and maps: no dice, no danger. **Exec** is doing: it has consequences, and it cannot be taken back. The console marks each group `[plan]` or `[final]`. The engine treats them the same. The mark tells the player which kind of choice this is.

If no option in a group is visible (every option's `when` is false), the engine skips the group. The checker warns when this can happen.

### 4.4 Option

```json
{
  "key": "lift",
  "label": "Lift the stone lid",
  "sub": "Fighter only.",
  "when": { "field": "role", "is": "fighter" },
  "effects": [ { "flag": "lid_open" } ],
  "then": [ { "text": "The lid grinds aside." } ],
  "to": "treasure"
}
```

| Key | Required | What it is |
|---|---|---|
| `key` | Yes | A short id, unique inside the group. |
| `label` | Yes | What the player picks. |
| `sub` | No | One small line under the label: the effect in plain words ("Exposure +1"). |
| `when` | No | Hide this option while the condition is false. |
| `effects` | No | A list of changes made when the player picks it. |
| `then` | No | Beats shown right after the pick. |
| `to` | No | Leave the scene now, to a scene id or an ending id. Later groups in this scene are skipped. |
| `roll` | No | A dice roll. See section 8. |

**Numbers on screen.** The console numbers the *visible* options 1, 2, 3 in the order you wrote them. Hidden options take no number. The engine maps the typed number back to the option's `key`. Never pick an option by its position in the file.

### 4.5 Ending

Endings live in the top-level `endings` object, keyed by ending id. They are not scenes.

```json
"endings": {
  "treasure": {
    "title": "Down the Well",
    "beats": [ { "text": "At the bottom, a dry room, and a chest." } ]
  }
}
```

| Key | Required | What it is |
|---|---|---|
| `title` | Yes | The ending's name. |
| `beats` | Yes, at least one | The ending text. Beats may use `when`, so one ending can say different things to a Fighter and a Wizard. |

An ending has no choices. When the player reaches one, the game shows it, then offers restart or quit. Every ending must be reachable.

---

## 5. The state: what the game remembers

The game remembers three kinds of thing. Together with the place the player is, they are the **state**. The save file is the state.

| Kind | Declared where | Holds | Changed by | Tested by |
|---|---|---|---|---|
| **Field** | Top-level `fields` list | A word: `"fighter"`, `"Unnamed (cash)"`. Starts as `""` (empty). | `{ "set": { "role": "wizard" } }` | `{ "field": "role", "is": "wizard" }` |
| **Meter** | Top-level `meters` list | A whole number between `min` and `max`. | `{ "meter": "exposure", "add": 2 }` (use a minus number to lower it) | `{ "meter": "exposure", "gte": 3 }` or `"lte"` |
| **Flag** | Nowhere: a flag exists once an effect sets it | On or off. Starts off. Once on, it stays on. | `{ "flag": "lamp" }` | `{ "flag": "lamp" }` |

### Field

```json
{ "id": "role", "label": "Role" }
```

`id` and `label` are required. `side` (`"front"` or `"back"`) is allowed and ignored by the console; the Stage uses it.

### Meter

```json
{ "id": "exposure", "label": "Exposure", "min": 0, "max": 6, "start": 1 }
```

`id`, `label`, `min`, `max` and `start` are required whole numbers (except the two text keys), with `min <= start <= max`. `hud` (`true` or `false`, default `true`) is allowed: a meter with `"hud": false` is not shown on the status line. An `add` never pushes a meter past `min` or `max`; the engine stops it at the edge.

### Which to use

| You want to remember | Use |
|---|---|
| Who the hero is, or a word that ends up on the character sheet | a field |
| How much of something: suspicion, torches left, a stat for a roll | a meter |
| That something happened: found the key, woke the rats | a flag |

---

## 6. Conditions and effects

### Conditions

A condition is used in a beat's `when`, an option's `when`, and a `route` entry's `when`.

| Form | True when |
|---|---|
| `{ "flag": "lamp" }` | the flag `lamp` is on |
| `{ "field": "role", "is": "fighter" }` | the field `role` holds exactly `fighter` |
| `{ "meter": "exposure", "gte": 3 }` | the meter is 3 or more |
| `{ "meter": "exposure", "lte": 2 }` | the meter is 2 or less |
| `{ "not": { "flag": "lamp" } }` | the inner condition is false |
| `{ "all": [ cond, cond ] }` | every condition in the list is true |
| `{ "any": [ cond, cond ] }` | at least one condition in the list is true |

**One level only.** Inside `not`, `all` and `any`, use only the first four forms. `{ "all": [ { "not": ... } ] }` is not allowed. The Stage allows deeper nesting; this course does not, so the engine needs no recursion. If you need more, use a flag.

### Effects

An effect is used in an option's `effects` and in a roll result's `effects`.

| Form | Does |
|---|---|
| `{ "flag": "lamp" }` | turns the flag on |
| `{ "set": { "role": "fighter" } }` | writes a word into a field (one or more fields per `set`) |
| `{ "meter": "exposure", "add": 1 }` | adds to a meter; `-1` takes away |

### The checker's typo rules

- A flag that some condition tests but no effect sets is a **problem**. It is usually a typo.
- A flag that an effect sets but nothing tests is a **warning**. It does nothing.
- A field value tested with `is` that no `set` ever writes is a **problem** (`"wizzard"`).
- A field, meter or target id that is not declared is a **problem**.

---

## 7. The lever

Every final project has a **lever**: an early choice about who the hero is, stored in a field, that later scenes test. Both worked examples use it.

| Story | Lever field | Values | The might side | The magic side |
|---|---|---|---|---|
| *Fort on the Lake* | `role` | `fighter`, `wizard` | The Fighter: a sword, strong at doors | The Wizard: one Sleep spell |
| *The Dead Drop* | `role` | `enforcer`, `hacker` | The Enforcer: chrome and muscle, through people and doors | The Hacker: code, through the feed and the locks |

The rules of the lever:

1. The field is always named `role`. The checker looks for it by that name.
2. It is set by an option's `set` effect in a choice group of the **start** scene.
3. It has two values (three are allowed, for example a Nomad).
4. Each value opens at least one option that the other values never see (`"when": { "field": "role", "is": "..." }`).
5. Each value can reach at least one ending.

Pattern:

```json
{ "key": "role", "ask": "Who rows to the island?", "gate": "exec",
  "options": [
    { "key": "fighter", "label": "The Fighter", "sub": "A sword. Strong at doors.",
      "effects": [ { "set": { "role": "fighter" } } ] },
    { "key": "wizard", "label": "The Wizard", "sub": "A dagger and one Sleep spell.",
      "effects": [ { "set": { "role": "wizard" } } ] } ] }
```

Later:

```json
{ "key": "shoulder", "label": "Put your shoulder to the door",
  "when": { "field": "role", "is": "fighter" }, "to": "store" }
```

A lever can also add to a meter, so a roll can read it: `{ "meter": "body", "add": 3 }`. *The Dead Drop* does this.

---

## 8. Dice (optional)

Dice are optional. A story with no `roll` needs no `resolver`. *Fort on the Lake* has no dice. *The Dead Drop* has one roll.

There is one form:

```json
"roll": {
  "dice": "4dF",
  "add": "code",
  "vs": 2,
  "results": {
    "fail":    { "effects": [ { "flag": "bad" } ], "then": [ { "text": "The loop stutters." } ] },
    "success": { "effects": [ { "flag": "ok" } ],  "then": [ { "text": "The feed shows an empty seat." } ] }
  }
}
```

| Key | Required | What it is |
|---|---|---|
| `dice` | Yes | One of `"1d6"`, `"2d6"`, `"1d20"`, `"4dF"`. A `4dF` die shows −1, 0 or +1. |
| `add` | Yes | A meter id. Its value is added to the dice. |
| `vs` | Yes | The number to compare against. |
| `results` | Yes | Both `fail` and `success`. Each holds optional `effects` and optional `then`. |

How the total is read depends on the story's `resolver`. These are the Stage's own rules, narrowed to two results:

| `resolver` | Success when | Notes |
|---|---|---|
| `"ose"` | total **≥** `vs` (meet or beat) | Old-School Essentials. Use with `1d6`, `2d6`, `1d20`. |
| `"fate4df"` | total **>** `vs` | Fate. Use with `4dF`. A total equal to `vs` is a tie; in this subset a tie counts as a fail, as the Stage does when `tie` is absent. |

A roll result cannot send the player somewhere by itself. Set a flag in the result, then use a `route` (or a `when`) to send the player on. *The Dead Drop* sets `bad` on a fail and its last scene routes `bad` to the `debrief` ending.

The option's `effects` happen first, then the roll, then the result's `effects`, then all the `then` beats, then `to` if there is one.

**Repeatable dice.** The dice use Python's `random.Random(seed)`. The seed comes from `--seed N` on the command line, or else from the environment variable `SEED`, or else the game picks one and prints it (`Seed: 4821. Replay with --seed 4821.`). The same seed and the same typed answers always give the same game. Tests always set a seed.

The checker does not roll. It follows both results whenever the dice can reach them (4dF + 3 against 2 can reach both; 1d6 + 0 against 9 can only fail).

---

## 9. A tiny complete example

This is `cyoa_kit/stories/toy.json` and `course-cti110-26fa/p7/toy_story.json`. Both files hold exactly this text. It passes the checker with scope warnings only (it is smaller than a final project must be).

```json
{
  "id": "toy",
  "title": "The Locked Gate",
  "start": "gate",
  "fields": [
    { "id": "role", "label": "Role" }
  ],
  "scenes": [
    {
      "id": "gate",
      "title": "The Gate",
      "beats": [
        { "text": "A rusty gate blocks the road. A lamp hangs on a hook beside it." }
      ],
      "choices": [
        {
          "key": "role",
          "ask": "Who are you?",
          "gate": "exec",
          "options": [
            { "key": "fighter", "label": "The Fighter", "sub": "Strong arms.",
              "effects": [ { "set": { "role": "fighter" } } ] },
            { "key": "wizard", "label": "The Wizard", "sub": "One spell.",
              "effects": [ { "set": { "role": "wizard" } } ] }
          ]
        },
        {
          "key": "act",
          "ask": "What do you do?",
          "gate": "plan",
          "options": [
            { "key": "lamp", "label": "Take the lamp",
              "effects": [ { "flag": "lamp" } ],
              "then": [ { "text": "The lamp is warm. Someone lit it today." } ] },
            { "key": "leave", "label": "Walk away", "to": "home" }
          ]
        }
      ],
      "next": "yard"
    },
    {
      "id": "yard",
      "title": "The Yard",
      "beats": [
        { "text": "Past the gate is a yard with a dark well." },
        { "text": "Your lamp shows a ladder inside the well.", "when": { "flag": "lamp" } }
      ],
      "choices": [
        {
          "key": "well",
          "ask": "What do you do at the well?",
          "gate": "exec",
          "options": [
            { "key": "climb", "label": "Climb down the ladder",
              "when": { "flag": "lamp" }, "to": "treasure" },
            { "key": "lift", "label": "Lift the stone lid", "sub": "Fighter only.",
              "when": { "field": "role", "is": "fighter" }, "to": "treasure" },
            { "key": "light", "label": "Cast a light down the well", "sub": "Wizard only.",
              "when": { "field": "role", "is": "wizard" }, "to": "treasure" },
            { "key": "back", "label": "Go home", "to": "home" }
          ]
        }
      ],
      "ending": "home"
    }
  ],
  "endings": {
    "treasure": {
      "title": "Down the Well",
      "beats": [
        { "text": "At the bottom is a dry room and an old chest." },
        { "text": "You lift the chest with one hand.", "when": { "field": "role", "is": "fighter" } },
        { "text": "Your light shows a word carved on the lid.", "when": { "field": "role", "is": "wizard" } }
      ]
    },
    "home": {
      "title": "Home Before Dark",
      "beats": [
        { "text": "You walk home. The gate creaks behind you." }
      ]
    }
  }
}
```

What it shows, in order of a beginner's questions:

| Question | Where in the example |
|---|---|
| How does the game start? | `start` is `gate`. |
| How is the lever set? | Group `role` in `gate`. |
| How does a flag open a choice? | `lamp` is set in `gate`; `climb` shows only with it. |
| How does the lever open a choice? | `lift` (Fighter) and `light` (Wizard). |
| How do I leave early? | `leave` and `back` use `to` an ending. |
| How does a scene end? | `gate` has `next`; `yard` has `ending`. |
| How does one ending change by role? | The beats of `treasure` use `when`. |

---

## 10. The engine (`engine.py`)

The engine is pure functions over plain dicts. It has no classes, no `print`, no `input`, no `global`, and no recursion. Standard library only (`json`, `random`, `copy`). Python 3.10 or newer. A student never edits it; the checker tells you if it changed.

### 10.1 The state dict

```json
{
  "story": "toy",
  "scene": "yard",
  "group": 0,
  "fields": { "role": "wizard" },
  "meters": {},
  "flags": ["lamp"],
  "trail": ["gate", "yard"]
}
```

| Key | Holds |
|---|---|
| `story` | The story's `id`. A save from another story will not load. |
| `scene` | The current scene id, or an ending id once the game is over. |
| `group` | The index (0, 1, 2...) of the next choice group to ask in this scene. |
| `fields` | Every declared field and its word. Starts `""`. |
| `meters` | Every declared meter and its number. Starts at `start`. |
| `flags` | The flags that are on, as a **sorted list** (not a set), so it survives JSON. |
| `trail` | Every scene and ending id entered, in order, starting with `start`. |

These seven keys, and no others. Only text, whole numbers and lists, so `json.dump` and `json.load` give back the same dict.

### 10.2 Public functions (exact names)

| Function | Returns | Does |
|---|---|---|
| `load_story(path)` | story dict | Opens and `json.load`s the file. On bad JSON, raises `ValueError` with a plain message that names the line and column. |
| `make_rng(seed)` | `random.Random` | `random.Random(seed)`. |
| `new_state(story)` | state | The state at the start scene. |
| `find_scene(story, scene_id)` | scene dict or `None` | Looks up a scene by id. |
| `is_over(story, state)` | `True`/`False` | True when `state["scene"]` is an ending id. |
| `get_ending(story, state)` | ending dict | The ending the state is at. |
| `test_condition(cond, state)` | `True`/`False` | One condition, section 6. A missing condition (`None`) is true. |
| `visible(items, state)` | list | The beats or options whose `when` is true, in written order. |
| `current_group(story, state)` | group dict or `None` | The first group at or after `state["group"]` that has a visible option. `None` when the scene's choices are done. |
| `choose(story, state, option_key, rng)` | `(new_state, beats, report)` | Applies one pick: effects, roll, result effects, `then`, `to`. `beats` is the visible `then` beats (option's, then the result's). `report` is the roll report or `None`. Raises `ValueError` if the key is not a visible option of the current group. Never changes the state it was given. |
| `leave_scene(story, state)` | new state | Follows the scene's `next`, `ending` or first matching `route` entry. |
| `roll_dice(dice, rng)` | list of faces | `"2d6"` → `[3, 5]`; `"4dF"` → `[1, 0, -1, 1]`. |
| `save_game(state, path)` | `None` | `json.dump` with `indent=2`. |
| `load_game(story, path)` | state | `json.load`, then checks the seven keys, the story id, the scene id, fields and meters. Raises `ValueError` with a plain message if the save does not fit the story. |

The roll report:

```json
{ "dice": "4dF", "faces": [1, 0, -1, 1], "add": "code", "bonus": 3,
  "total": 4, "vs": 2, "result": "success" }
```

### 10.3 The play loop (in `game.py`)

```
state = new_state(story); show_title; show_scene
loop:
    if is_over: show_ending, then ask "r restart or q quit"
    group = current_group(story, state)
    if group is None: state = leave_scene(story, state); show the new scene or ending; continue
    show_status; show_choices(group, visible options)
    answer = ask(...)
    a number 1..n  -> choose(...); show_roll; show_beats; if the scene changed, show it
    s / l / r / h / q -> save, load, restart, help, quit
    anything else  -> show_message("Choose 1-3, or s, l, r, h, q.")
```

---

## 11. The console (`game.py`) and the files around it

### 11.1 Command line

```
python3 game.py stories/fort.json
python3 game.py stories/fort.json --display ansi
python3 game.py stories/fort.json --seed 7 --echo < tests/fort_fighter_win.in
```

| Option | Default | Does |
|---|---|---|
| (first argument) | required | The story file. |
| `--display plain\|ansi\|curses` | env `CYOA_DISPLAY`, else `plain` | Which display module to use. |
| `--seed N` | env `SEED`, else a new random seed (printed) | The dice seed. |
| `--echo` | off | Print each typed answer after its prompt, so a piped run reads like a typed one. |

`game.py` reads `sys.argv` with a small `read_options(argv)` function. It wraps play in `try` / `finally` so `display.stop()` always runs. Ctrl+C quits cleanly with "Goodbye."

### 11.2 Keys at a choice

| Type | Does |
|---|---|
| `1`, `2`, ... | Pick that visible option. |
| `s` | Save to `save_<story id>.json` in the current folder. |
| `l` | Load that file and show the scene again. |
| `r` | Restart from the start scene. |
| `h` | Show these keys. |
| `q` | Quit. End of input (a piped file runs out) also quits. |

Upper and lower case both work. Spaces around the answer are ignored.

### 11.3 Test vectors (golden runs)

A golden run is a file of typed answers and the exact output they produce.

- `tests/<name>.in`: the answers, one per line. Lines that start with `#` are comments and are removed before the answers are piped in. The first line is a header: `# story: stories/fort.json seed: 1`.
- `tests/<name>.out`: the exact output of `python3 game.py <story> --seed <seed> --echo --display plain` with those answers piped in.
- `python3 tests/run_tests.py` (run inside `cyoa_kit/`) replays every `.in`, compares with its `.out`, prints `PASS <name>` or `FAIL <name>` and the first different line, and ends with `ALL TESTS PASSED` or `N TESTS FAILED`. `--regen` rewrites the `.out` files; check the diff after.
- Every `.in` is also replayed with `--display ansi` and output piped (not a TTY). The output must equal the same `.out`, because effects turn off when output is not a terminal.
- Checker vectors: `tests/check_<story>.out` holds the checker's output for each story in `stories/`. `tests/broken/<name>.json` are stories broken on purpose, each with `tests/broken/<name>.out`.

A student's golden runs use the same format: one `.in` per ending they claim, named `tests/story_<ending id>.in`.

### 11.4 The checker (`checker.py`)

```
python3 checker.py stories/fort.json
python3 checker.py stories/my_story.json --banned banned_words.txt
```

Each line starts with `OK`, `WARNING` or `PROBLEM`. A problem names the scene, the group, the option and the rule:

```
PROBLEM scene 'yard', group 'well', option 'climb': 'to' names 'tresure', which is not a scene or an ending. (rule 6)
```

The last line is exactly `RESULT: PASS (0 problems, N warnings)` or `RESULT: FAIL (N problems, M warnings)`. The exit code is 0 on PASS and 1 on FAIL.

**Shape rules** (each problem cites its number):

| # | Rule |
|---|---|
| 1 | The file is valid JSON and the top level is an object. Bad JSON names the line and column. |
| 2 | The top level has `id`, `title`, `start`, `fields`, `scenes`, `endings`, and no key outside section 3. Every object in the file uses only the keys this contract lists for it. |
| 3 | Ids are unique across scenes and endings, and are lowercase letters, digits and `_`, starting with a letter. Group keys are unique in their scene; option keys are unique in their group. |
| 4 | `start` names a scene. |
| 5 | Each scene has `id`, `title`, at least one beat, and exactly one of `next`, `ending`, `route`. |
| 6 | Every `next` names a scene; every `ending` names an ending; every `to` and `route` `to` names a scene or an ending. |
| 7 | In a `route`, every entry but the last has a `when`; the last has none. |
| 8 | Every beat has non-empty `text`. Each ending has a `title` and at least one beat. |
| 9 | Each group has `key`, `ask`, `gate` (`plan` or `exec`) and at least one option; each option has `key` and `label`. |
| 10 | Conditions use only the forms in section 6, one level deep. Each names a declared field or meter. A tested flag is set somewhere. A tested field value is written somewhere. |
| 11 | Effects use only the forms in section 6, on declared fields and meters; `add` is a whole number. |
| 12 | Each `roll` matches section 8, `add` names a meter, and the story has a `resolver`. |
| 13 | Each meter has whole-number `min`, `max`, `start` with `min <= start <= max`. Each field has `id` and `label`. |

**Play rules** (the checker plays every path; it explores states made of scene, group, fields, meters and flags, and stops with a warning after 50,000 states):

| # | Rule | Level |
|---|---|---|
| 14 | Every scene can be reached. | problem |
| 15 | Every ending can be reached. | problem |
| 16 | No stuck spot: from every reachable state, some ending can still be reached. | problem |
| 17 | At least one real decision: a group where two options lead to different sets of reachable endings. | problem |
| 18 | The lever: a field `role` exists, is set in the start scene, each value has an option only it can see, and each value reaches an ending. | problem |
| 19 | A flag set but never tested; a group whose options can all be hidden. | warning |
| 20 | Size: 6 to 15 scenes and at least 3 endings (the final-project numbers). | warning |
| 21 | Banned words (only with `--banned FILE`): a whole-word, any-case match in any title, beat, ask, label or sub. | problem |

The report also prints, for golden runs:

```
OK endings reached: 3 of 3
OK role fighter reaches: flooded_stair, rowed_home
OK role wizard reaches: fell, flooded_stair, rowed_home
OK shortest way to flooded_stair (role fighter): type 1 1 1 3 1 1 (6 picks)
```

The typed numbers are the numbers on screen, so a student can paste them into a `.in` file. A route through a roll says which result it needs: `type 1 2 1 1 (needs success)`.

The checker also checks the kit itself: `OK engine.py matches the kit` or `WARNING engine.py has changed since the kit was made`. It compares a SHA-256 of `engine.py` with a constant `ENGINE_SHA256` in `checker.py`. This is a guardrail for the final project, where AI may change the display and `game.py` but never the engine.

---

## 12. The display interface

Three modules, one set of functions. `game.py` imports one of them as `display` and calls only these. Each module must define all eleven, with these exact names and parameters.

| Function | Called | Does |
|---|---|---|
| `start(echo)` | once, before play | Set up the screen. `echo` is `True` or `False` (from `--echo`). |
| `stop()` | once, always, in `finally` | Put the terminal back the way it was. |
| `show_title(story)` | at start and after a restart | The `title` and `subtitle`. |
| `show_scene(scene, beats)` | when a scene is entered or reloaded | The scene `title`, its `place`, then `beats` (already filtered). |
| `show_beats(beats)` | after a pick | The `then` beats (already filtered). |
| `show_roll(report)` | after a pick with a roll | One line: dice, faces, bonus, total, `vs`, result. |
| `show_status(story, state)` | before each choice group | Meters with `hud` not `false` (`Exposure 3/6`), and fields that are not empty (`Role: wizard`). Reads the state; never changes it. |
| `show_choices(group, options)` | before each ask | The `ask`, `[plan]` or `[final]`, then the visible options numbered from 1, each with its `sub` under it. |
| `ask(prompt)` | for every answer | Read one line. Return it stripped. Return `"q"` at end of input or on Ctrl+C. If `echo` is on, print the answer after the prompt. |
| `show_message(text)` | errors, "Saved.", help | One short line. |
| `show_ending(ending, beats, state)` | when an ending is reached | The ending `title`, its beats (already filtered), `THE END`, and the trail of scene titles or ids. |

Rules for every display module:

- It never imports `engine`, never calls `choose`, and never assigns into `state`. The checker scans `display_*.py` for `import engine`, `choose(` and `state[` on the left of `=`, and warns.
- `display_plain` prints **ASCII only**, wrapped at 72 columns with `textwrap`. A speaker line prints as `CHEN: text`. A `screen` prints each line as `  | text`. Its output is the reference for every `.out` file.
- `display_ansi` adds colour, a typewriter, boxes and meter bars. It turns **every** effect off, and prints exactly what `display_plain` prints, when output is not a terminal (`sys.stdout.isatty()` is false), when the environment variable `NO_COLOR` is set to anything not empty, or when `CYOA_EFFECTS=off`. The simplest way: call the `display_plain` function when effects are off. Enter skips the typewriter. Box and bar characters may be Unicode, but only when effects are on.
- `display_curses` draws a full-screen layout with `curses` and `curses.wrapper`-style cleanup in `stop()`. `curses` is in the standard library on macOS, Linux and Codespaces. On Windows it needs `pip install windows-curses`. If `curses` cannot be imported, or output is not a terminal, `game.py` uses `display_plain` and prints one line to standard error saying why.

---

## 13. Export to the Stage (later, not in this unit)

To play a story in the Stage, a converter splits the file and adds what the Stage needs. Nothing in a story file has to change.

| The Stage needs | The converter writes |
|---|---|
| `pack.json` `kit`, `storageKey`, `tallies`, `commentary` | `"paper"` or `"feed"`; `"fort-stage.<id>"` or `"htll.<id>"`; `{}`; a default label and kinds |
| Scene `look` and `set` | `"paint"`, and the scene id |
| Ending `look` and `set` | `"paint"`, and the ending id |
| A `rule` note on the first `exec` group | `"notes": ["rule-gate"]` and that note in `notes.json` |
| `sets.json`, `theme.json`, `NOTES.md` | Placeholder sets and themes; a NOTES.md from the student's blueprint |
| `cast.json` entries for each `speaker` | One entry per speaker id |
| A roll's `tie` and `style` | Nothing: the Stage falls back to `fail` and `success` |

Keys this subset leaves out on purpose: scene `look`, `set`; beat `kicker`, `set`, `notes`, `comment`, `reveal`, `look`; group `cost`, `notes`, `comment`, gate `fate`; option `lock`, `hint`, `input`; condition `tally`; effect `tally`; roll results `tie`, `style`; dice `3d6`; nested conditions.
