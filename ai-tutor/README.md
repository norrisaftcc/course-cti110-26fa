# Your AI Tutor

CTI 110, Fall 2026. Set up in P6LAB1 (Tue 11/03/26). Swapped at P7LAB1 (Tue 11/10/26) and at the blueprint gate (Tue 11/24/26).

---

## What it is

The AI tutor is a set of small instruction files that you copy into your repository. They tell the AI tools in your Codespace how to help you. GitHub Copilot Chat reads them. Claude Code reads them. Other AI tools that read `AGENTS.md` read them too.

With these files in place, your AI acts like a tutor, not like an answer machine. It asks what you tried. It explains why. It gives hints in steps. It leaves the key lines for you to write, marked `# TODO(human)`. It ends with a question to check that you understood.

## Why it teaches instead of solving

The course rule, in one sentence:

> You may use AI exactly to the degree that you can verify its output, and this course exists to build that verification ability.

To *verify* means to check that an answer is right. You can only check code you understand. So the tutor helps you understand first. In the final project you present your own code live. A student who cannot explain their own software fails the presentation. The tutor is set up so that you can.

---

## Which rung is in force, and when

The course's AI Assistance Ladder has rungs. Each rung allows a bit more help. Your tutor files hold one rung at a time.

| Dates | Rung | Name | Folder |
|---|---|---|---|
| Tue 11/03/26 (P6LAB1) to Thu 11/05/26 | 2 | Explainer: AI as explainer, not author | `ai-tutor/rung-2/` |
| Tue 11/10/26 (P7LAB1) to Tue 11/24/26 | 3 | Reviewer: AI as reviewer | `ai-tutor/rung-3/` |
| Thu 11/19/26 to Tue 11/24/26 | none on the blueprint | You write `blueprint.md` and `story.json` with **no AI** | (the Rung 3 files stay in; the tutor says no) |
| Tue 11/24/26 (blueprint gate, after sign-off) to Thu 12/03/26 | 4 | Collaborator: AI as collaborator, final project only | `ai-tutor/rung-4/` |

Your instructor tells you when to swap. Swap at the start of class on those days.

---

## Install it in your Codespace (P6LAB1)

Your instructor puts the `ai-tutor` folder in your class repository, at the top level. You copy one rung's files from it into the top of your repository.

1. Open your repository's Codespace.
2. Open a terminal: **Terminal > New Terminal**.
3. Go to the top folder of your repository. This command works from anywhere inside it:

   ```
   cd "$(git rev-parse --show-toplevel)"
   ```

4. Check that the tutor folder is there:

   ```
   ls ai-tutor
   ```

   You should see `rung-2`, `rung-3` and `rung-4`, and this handout, `README.md`.
5. Copy Rung 2 in. This is the one command:

   ```
   cp -r ai-tutor/rung-2/. .
   ```

   The `/.` at the end of `rung-2/.` matters. It copies the hidden folders (`.github` and `.claude`) too.
6. Check the files:

   ```
   ls -a
   ls .github .claude .claude/output-styles
   ```

### What files appear

| File | Which tool reads it | What it holds |
|---|---|---|
| `AGENTS.md` | Many AI tools, including Copilot Chat in VS Code | The tutor's rules for this rung. Line 1 names the rung. |
| `.github/copilot-instructions.md` | GitHub Copilot Chat | The same rules, word for word. |
| `CLAUDE.md` | Claude Code | One line, `@AGENTS.md`, which pulls in the rules. Then a line naming the rung. |
| `.claude/settings.json` | Claude Code | Picks the tutor style, `CTI 110 Tutor`. At Rungs 2 and 3 it also stops Claude Code from editing your files. |
| `.claude/output-styles/cti110-tutor.md` | Claude Code | How the tutor answers: ask, explain why, hint, `TODO(human)`, check. |

Commit them, so they stay in your repository:

```
git add AGENTS.md CLAUDE.md .github .claude
git commit -m "Install CTI 110 tutor, Rung 2"
```

If your repository already had its own `AGENTS.md`, `CLAUDE.md` or `.claude/settings.json`, the copy replaces it. Ask your instructor first if that worries you.

---

## Check that it works

Ask the tutor: **"What rung are you on?"**

It should start its answer with the first line of `AGENTS.md`:

| Rung | The tutor should say |
|---|---|
| 2 | `CTI 110 Tutor - Rung 2 (Explainer)` |
| 3 | `CTI 110 Tutor - Rung 3 (Reviewer)` |
| 4 | `CTI 110 Tutor - Rung 4 (Collaborator)` |

### In GitHub Copilot Chat

1. Open the Chat view (the chat icon at the top or on the side bar).
2. Start a **new** chat. An old chat may not see the new files.
3. If the chat box has a mode picker, choose **Ask** at Rungs 2 and 3. Ask mode answers questions. Other modes may try to change your files.
4. Type: `What rung are you on?`
5. Under the answer, open **References**. You should see `copilot-instructions.md` or `AGENTS.md` in the list. That means Copilot read the tutor files.

### In Claude Code

1. In the terminal, at the top of your repository, type `claude` and press Enter.
2. The first time, it asks whether you trust this folder. Say yes. It is your own repository.
3. Type `/output-style` and press Enter. It lists the styles and marks the one in use. It should be **CTI 110 Tutor**. (Or type `/config` and look at **Output style**.)
4. Type: `What rung are you on?`

If Claude Code is not installed in your Codespace, use Copilot Chat. Your instructor will say which tools the class uses.

### The real test

In P6LAB1 you run `p6/p6lab1_tutor_check.py`, which has a planted bug, and ask the tutor about it. A working tutor asks you a question or gives a hint first. It does not paste the fixed program. The lesson sheet has a checklist.

---

## Swap rungs

Same command, new folder. Run it from the top of your repository.

| When | Command |
|---|---|
| Tue 11/10/26, start of P7LAB1 | `cp -r ai-tutor/rung-3/. .` |
| Tue 11/24/26, after the instructor signs off your blueprint | `cp -r ai-tutor/rung-4/. .` |

The copy overwrites the old rung's files. Every rung has the same five files, so nothing old is left behind.

Then:

1. **Copilot Chat:** start a new chat.
2. **Claude Code:** quit (`/exit`) and start `claude` again. It reads the style file when it starts.
3. Ask: **"What rung are you on?"** Check the answer against the table above.
4. Commit: `git add -A` then `git commit -m "Tutor to Rung 3"` (or 4).

---

## Turn off Copilot's inline suggestions (Rungs 2 and 3)

Inline suggestions are the grey text that appears as you type. Press Tab and it becomes your code. **The tutor files do not control that grey text.** They only guide the chat. So while you build the basics, turn it off. You want to learn to write the line, not to accept it.

Pick one way:

- **The status bar.** At the bottom of the window, click the Copilot icon. In the menu, uncheck inline suggestions (for all files, or just for Python). **Snooze** in the same menu turns them off for a few minutes only.
- **The settings file.** Press F1, type `Preferences: Open User Settings (JSON)` and press Enter. Add this line inside the outer `{ }`:

  ```json
  "github.copilot.enable": { "*": false }
  ```

The grey text is welcome back at Rung 4. Then change `false` to `true`, or check the box again.

---

## What the tutor will and will not do

| | Rung 2: Explainer | Rung 3: Reviewer | Rung 4: Collaborator (final build) |
|---|---|---|---|
| Explain an error or a concept | Yes | Yes | Yes |
| Show a tiny example (3 lines or fewer, made-up names) | Yes | Yes | Yes |
| Make practice problems (labelled "not vetted") | Yes | Yes | Yes |
| Review your code after it runs | No | Yes: at most 3 comments a round (what, which line, why) | Yes |
| Show a fixed piece of your own code | No | Only in a review of code that runs: one piece, 5 lines or fewer, after you tried | Yes, in the files it may change |
| Write code for you | No | No new functions | Yes, in `game.py`, the `display_*.py` files and new `.py` files. It still leaves at least one key line per feature for you. |
| Edit your files | No | No | Only the files above |
| Touch `engine.py`, `checker.py`, `tests/run_tests.py` | No | No | No. They are frozen. |
| Write your story text, blueprint, user stories, map or golden-run answers | No | No | No. Those are yours. |
| Write `prompts.md`, `AI-DISCLOSURE.md` or your talk | No | No | No |
| Remind you about disclosure | - | Yes: a review note and a disclosure line | Yes: `prompts.md` and `AI-DISCLOSURE.md` |

At every rung it asks you to say what the code should do **first**: the expected output in a lab, or your user story in the final project. That is the spec. It also runs the checks it can, and it says so when it has not run something.

### If you say "just give me the answer"

It will say kindly what your rung allows, and offer the next hint. That is on purpose. It is not broken.

---

## If it does not work

| What you see | Why | Fix |
|---|---|---|
| The tutor does not know what rung it is, or names the wrong one. | The files are not at the top of the repository, or the chat is old. | Run `cd "$(git rev-parse --show-toplevel)"`, then the copy command again. Start a new chat. |
| `cp: cannot stat 'ai-tutor/rung-2/.'` | You are not at the top of the repository, or the `ai-tutor` folder is missing. | Run the `cd` command above. Then `ls ai-tutor`. If it is missing, ask your instructor. |
| `.github` or `.claude` is missing after the copy. | You typed `rung-2/*` or `rung-2` instead of `rung-2/.`. | Run the command again exactly: `cp -r ai-tutor/rung-2/. .` |
| Claude Code uses the Default style. | You changed the style with `/output-style` once. That choice is saved in `.claude/settings.local.json`, and it wins over the tutor's file. | Open `.claude/settings.local.json` and delete the `"outputStyle"` line, or pick **CTI 110 Tutor** in `/config`. Restart `claude`. |
| Copilot's References list does not show the tutor files. | The setting that reads them may be off. | Ask your instructor. (The settings are named in `INSTRUCTOR.md`.) |
| The tutor pastes a whole fixed program anyway. | The files guide the AI. They cannot force it. | Check the install, start a new chat, and try again. Tell your instructor. Do not hand in code you did not write. |

---

## An honest note

These files **guide** the AI. They do not **lock** it. A tool can ignore them. You can also ask another AI that has no tutor files at all. Nothing here stops that.

What keeps the course fair is the assignments: you predict before you run, you prove your output with a `diff` or a golden run, the blueprint is written before the build, and at the end you **present**. The presentation is the audit. If code is in your project, you must be able to explain it.

So use the tutor the way it is set up. It makes the right kind of help easy.

## Disclosure (from Rung 3 on)

Saying what AI helped with is normal professional practice, like crediting a source. It is not a confession.

- **Rung 3 (labs):** add a short review note (what you changed because of the review, and why) and one disclosure line, in your own words, at the top of the file.
- **Rung 4 (final):** save every prompt in `cyoa_kit/prompts.md`, numbered and dated, and fill in `cyoa_kit/AI-DISCLOSURE.md` as you go. AI help that is within the rules and disclosed never costs you points.
