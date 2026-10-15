# CTI 110
# CYOA KIT - Test runner
# norris
# 10/15/26

# Plays the toy story with the curses display inside a pretend terminal
# (a "pseudo-terminal", from Python's pty module), types three answers,
# and checks that the screen showed the story and the game quit cleanly.
#
#   python3 tests/curses_smoke.py
#
# Exit code: 0 = pass, 1 = fail, 2 = skipped (no pty or curses here,
# for example on Windows).

import os
import select
import sys
import time

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (text to wait for on the screen, answer to type then)
SCRIPT = [("Who are you", "1"), ("What do you do", "2"), ("play again", "q")]

def read_until(fd, marker, seconds):
    """Read the terminal's output until marker shows up or time runs out."""
    seen = b""
    deadline = time.time() + seconds
    while time.time() < deadline and marker.encode() not in seen:
        ready = select.select([fd], [], [], 0.1)[0]
        if ready:
            try:
                chunk = os.read(fd, 4096)
            except OSError:            # the game closed the terminal
                break
            if not chunk:
                break
            seen = seen + chunk
    return seen

def start_game():
    """Start game.py in a pretend terminal 40 rows by 100 columns."""
    import pty
    pid, fd = pty.fork()
    if pid == 0:                       # this branch runs in the new process
        import fcntl
        import struct
        import termios
        fcntl.ioctl(0, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 100, 0, 0))
        env = dict(os.environ, TERM="xterm-256color", LINES="40", COLUMNS="100")
        env.pop("NO_COLOR", None)
        game = os.path.join(KIT, "game.py")
        story = os.path.join(KIT, "stories", "toy.json")
        os.execve(sys.executable, [sys.executable, game, story, "--display", "curses",
                                   "--seed", "1"], env)
    return pid, fd

def main():
    try:
        import curses                  # noqa: F401  (only checks that it loads)
        import pty                     # noqa: F401
    except ImportError as error:
        print(f"SKIP curses_smoke: {error}")
        sys.exit(2)
    pid, fd = start_game()
    screen = b""
    for marker, answer in SCRIPT:
        screen = screen + read_until(fd, marker, 10)
        if marker.encode() not in screen:
            os.kill(pid, 9)
            print(f"FAIL curses_smoke: the screen never showed '{marker}'")
            sys.exit(1)
        os.write(fd, (answer + "\r").encode())
    screen = screen + read_until(fd, "Goodbye.", 10)
    code = os.waitstatus_to_exitcode(os.waitpid(pid, 0)[1])
    text = screen.decode("utf-8", "replace")
    if code != 0 or "Goodbye." not in text or "The Gate" not in text:
        print(f"FAIL curses_smoke: exit code {code}; last output: {text[-200:]!r}")
        sys.exit(1)
    print("PASS curses_smoke")

if __name__ == "__main__":
    main()
