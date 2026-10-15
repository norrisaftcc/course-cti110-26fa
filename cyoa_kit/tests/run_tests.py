# CTI 110
# CYOA KIT - Test runner
# norris
# 10/15/26

# Runs every test in the kit. Run it from the cyoa_kit folder:
#
#   python3 tests/run_tests.py           check everything
#   python3 tests/run_tests.py --regen   rewrite the .out files, then
#                                        read the diff to see what changed
#
# (a) golden runs: every tests/*.in, with the plain display and the
#     ANSI display (piped, so its effects are off): both must match .out
# (b) the checker on every stories/*.json   -> tests/check_<id>.out
# (c) the checker on every tests/broken/*.json -> tests/broken/<name>.out
# (d) the engine checks in tests/test_engine.py
# (e) no kit file uses 'class' or 'global'
# (f) the curses display in a pretend terminal (skipped on Windows)

import glob
import json
import os
import re
import subprocess
import sys
import tempfile

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADER = re.compile(r"#\s*story:\s*(\S+)\s+seed:\s*(\d+)")
RESULTS = {"failed": 0, "regen": "--regen" in sys.argv}

def first_difference(expected, got):
    """Describe the first line where two texts differ."""
    want, have = expected.splitlines(), got.splitlines()
    for number in range(max(len(want), len(have))):
        line_want = want[number] if number < len(want) else "(no more lines)"
        line_have = have[number] if number < len(have) else "(no more lines)"
        if line_want != line_have:
            return f"line {number + 1}: expected {line_want!r}, got {line_have!r}"
    return "the line endings differ"

def fail(name, why):
    print(f"FAIL {name}: {why}")
    RESULTS["failed"] = RESULTS["failed"] + 1

def compare(name, out_path, got):
    """Compare output with its .out file. With --regen, write the file instead."""
    if RESULTS["regen"]:
        with open(out_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(got)
        print(f"WROTE {os.path.relpath(out_path, KIT)}")
        return
    if not os.path.exists(out_path):
        fail(name, f"there is no {os.path.relpath(out_path, KIT)}; run with --regen")
        return
    with open(out_path, encoding="utf-8") as file:
        expected = file.read()
    if expected == got:
        print(f"PASS {name}")
    else:
        fail(name, first_difference(expected, got))

def run(command, answers="", folder=KIT):
    """Run a command with typed answers piped in. Return (exit code, output, errors)."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(command, input=answers, capture_output=True, text=True,
                            encoding="utf-8", cwd=folder, env=env)
    return result.returncode, result.stdout, result.stderr

def golden_runs():
    """(a) Replay every .in file with both displays."""
    for in_path in sorted(glob.glob(os.path.join(KIT, "tests", "*.in"))):
        name = os.path.basename(in_path)[:-3]
        with open(in_path, encoding="utf-8") as file:
            lines = file.read().splitlines()
        header = HEADER.search("\n".join(lines))
        if header is None:
            fail(name, "the .in file needs a header like '# story: stories/toy.json seed: 1'")
            continue
        answers = "".join(line + "\n" for line in lines if not line.startswith("#"))
        story = os.path.join(KIT, header.group(1))
        out_path = in_path[:-3] + ".out"
        plain_output = ""
        for display in ("plain", "ansi"):
            command = [sys.executable, os.path.join(KIT, "game.py"), story,
                       "--seed", header.group(2), "--echo", "--display", display]
            with tempfile.TemporaryDirectory() as folder:      # save files land here
                code, output, errors = run(command, answers, folder)
            if code != 0:
                fail(f"{name} ({display})", f"the game crashed: {errors.strip()[-300:]}")
            elif display == "plain":
                compare(name, out_path, output)
                plain_output = output
            elif not RESULTS["regen"]:
                compare(f"{name} (ansi, piped)", out_path, output)
            elif output != plain_output:       # with --regen, ansi must match plain
                fail(f"{name} (ansi, piped)", first_difference(plain_output, output))

def checker_runs():
    """(b) and (c): the checker on each story and each broken story."""
    for path in sorted(glob.glob(os.path.join(KIT, "stories", "*.json"))):
        story_id = os.path.basename(path)[:-5]
        try:
            with open(path, encoding="utf-8-sig") as file:
                story_id = json.load(file).get("id", story_id)
        except (ValueError, AttributeError):
            pass                       # the checker will report the bad file
        relative = "stories/" + os.path.basename(path)
        code, output, errors = run([sys.executable, "checker.py", relative])
        compare(f"check_{story_id}", os.path.join(KIT, "tests", f"check_{story_id}.out"),
                output + errors)
    for path in sorted(glob.glob(os.path.join(KIT, "tests", "broken", "*.json"))):
        relative = "tests/broken/" + os.path.basename(path)
        code, output, errors = run([sys.executable, "checker.py", relative])
        compare("broken/" + os.path.basename(path)[:-5], path[:-5] + ".out", output + errors)

def engine_checks():
    """(d) Every test_ function in tests/test_engine.py."""
    sys.path.insert(0, os.path.join(KIT, "tests"))
    import test_engine
    for name, test in test_engine.all_tests():
        try:
            test()
            print(f"PASS test_engine.{name}")
        except Exception as error:     # any error at all is a failed test
            fail(f"test_engine.{name}", f"{type(error).__name__}: {error}")

def keyword_scan():
    """(e) No kit .py file starts a line with the keyword class or global."""
    pattern = re.compile(r"^\s*(class|global)\s")
    paths = glob.glob(os.path.join(KIT, "*.py")) + glob.glob(os.path.join(KIT, "tests", "*.py"))
    found = []
    for path in sorted(paths):
        with open(path, encoding="utf-8") as file:
            for number, line in enumerate(file, start=1):
                if pattern.match(line):
                    found.append(f"{os.path.relpath(path, KIT)} line {number}")
    if found:
        fail("no_class_or_global", "found in " + ", ".join(found))
    else:
        print("PASS no_class_or_global")

def curses_check():
    """(f) The curses display in a pretend terminal. Skipped where it cannot run."""
    code, output, errors = run([sys.executable, os.path.join("tests", "curses_smoke.py")])
    if code == 0:
        print("PASS curses_smoke")
    elif code == 2:
        print(output.strip() or "SKIP curses_smoke")
    else:
        fail("curses_smoke", (output + errors).strip()[-300:])

def main():
    golden_runs()
    checker_runs()
    engine_checks()
    keyword_scan()
    curses_check()
    for path in glob.glob(os.path.join(KIT, "save_*.json")):
        print(f"NOTE {os.path.basename(path)} is a save file in the kit folder; "
              "the tests did not make it.")
    if RESULTS["failed"]:
        print(f"{RESULTS['failed']} TESTS FAILED")
        sys.exit(1)
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    main()
