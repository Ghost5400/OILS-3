"""
arcade.core — Shared terminal utilities and formatting for OILS-3.
"""
import os
import sys
import time
import random

# Absolute project root directory: C:\...\OILS-3
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Stubs populated by arcade.session
_FUNNY_PRAISES = ["Great job!"]
_FUNNY_ROASTS = ["Nice try!"]

# Terminal Colors & Formatting
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def print_slow(text, delay=0.010, color=""):
    """Prints text with a subtle typing effect."""
    if color:
        sys.stdout.write(color)
        sys.stdout.flush()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if color:
        sys.stdout.write(Color.RESET)
    print()

def typewrite(text, delay=0.010, color="", newline=True):
    """Smooth typewriter effect — good for story/narrative lines."""
    if color:
        sys.stdout.write(color)
        sys.stdout.flush()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if color:
        sys.stdout.write(Color.RESET)
    if newline:
        print()

def spinner(label="Running", duration=1.4, color=None):
    """Animated CLI spinner — looks like a real terminal command executing."""
    _c = color or Color.CYAN
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {_c}{frames[i % len(frames)]}{Color.RESET}  {label}...")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  {Color.GREEN}✔{Color.RESET}  {label}... done!      \n")
    sys.stdout.flush()

def progress_bar(label="Loading", total=20, delay=0.045, color=None):
    """Animated progress bar — great for chapter transitions and quiz warmup."""
    _c = color or Color.GREEN
    for i in range(total + 1):
        filled = "█" * i
        empty  = "░" * (total - i)
        pct = int(i / total * 100)
        sys.stdout.write(f"\r  {_c}[{filled}{empty}]{Color.RESET} {pct}%  {label}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def anim_correct():
    """Flash a bright ✅ correct banner with a random funny praise."""
    frames = [
        f"{Color.GREEN}{Color.BOLD}  ✅  CORRECT!  ✅{Color.RESET}",
        f"{Color.WHITE}{Color.BOLD}  ✅  CORRECT!  ✅{Color.RESET}",
        f"{Color.GREEN}{Color.BOLD}  ✅  CORRECT!  ✅{Color.RESET}",
    ]
    for f in frames:
        sys.stdout.write(f"\r{f}")
        sys.stdout.flush()
        time.sleep(0.18)
    print()
    try:
        print(f"  {Color.GREEN}{Color.BOLD}{random.choice(_FUNNY_PRAISES)}{Color.RESET}")
    except Exception:
        pass

def anim_wrong():
    """Flash a red ❌ wrong banner with a random funny roast."""
    frames = [
        f"{Color.RED}{Color.BOLD}  ❌  WRONG!  ❌{Color.RESET}",
        f"{Color.WHITE}{Color.BOLD}  ❌  WRONG!  ❌{Color.RESET}",
        f"{Color.RED}{Color.BOLD}  ❌  WRONG!  ❌{Color.RESET}",
    ]
    for f in frames:
        sys.stdout.write(f"\r{f}")
        sys.stdout.flush()
        time.sleep(0.18)
    print()
    try:
        print(f"  {Color.RED}{random.choice(_FUNNY_ROASTS)}{Color.RESET}")
    except Exception:
        pass

def prompt_input(prompt_text=""):
    """
    Reads user input while keeping typed characters on the same line as the
    prompt.  On Windows we use msvcrt.getwch() to read and echo each
    character ourselves — this completely sidesteps Python 3.14's _pyrepl
    and the Windows Console line-editor, both of which inject a newline
    before they start accepting input, pushing the cursor to the wrong line.
    """
    # Flush any buffered output first so animations don't bleed into the prompt
    sys.stdout.flush()

    # Strip and emit any leading newlines
    while prompt_text.startswith("\n"):
        sys.stdout.write("\n")
        sys.stdout.flush()
        prompt_text = prompt_text[1:]

    # Print the prompt; cursor now sits immediately after it
    if prompt_text:
        sys.stdout.write(prompt_text)
        sys.stdout.flush()

    # ── Windows interactive path: character-by-character echo via msvcrt ────
    # msvcrt.getwch() reads one wide char without echo, completely bypassing
    # Python 3.14 _pyrepl and the Windows Console line-editor.  We only use
    # this when stdin IS a real console (isatty), so piped test harnesses
    # still work via the readline() fallback below.
    if os.name == "nt" and sys.stdin.isatty():
        try:
            import msvcrt
            chars = []
            while True:
                ch = msvcrt.getwch()
                if ch in ("\r", "\n"):          # Enter → done
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break
                elif ch == "\x03":              # Ctrl-C
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    raise KeyboardInterrupt
                elif ch == "\x08":              # Backspace
                    if chars:
                        chars.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                elif ch in ("\x00", "\xe0"):    # Arrow / function key prefix
                    msvcrt.getwch()             # consume second byte, ignore
                elif ch >= " ":                 # Printable character
                    chars.append(ch)
                    sys.stdout.write(ch)
                    sys.stdout.flush()
            return "".join(chars)
        except ImportError:
            pass  # msvcrt unavailable — fall through

    # ── Non-Windows / piped stdin fallback ───────────────────────────────────
    try:
        return sys.stdin.readline().rstrip("\r\n")
    except (EOFError, KeyboardInterrupt):
        return ""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

