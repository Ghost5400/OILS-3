"""
arcade.session — Gamification, user profile, local database, XP, and badges.
"""
import os
import json
import time
import random

from arcade.core import (
    PROJECT_ROOT, Color, clear_screen, prompt_input, typewrite,
)
import arcade.core as _core_mod

DB_PATH = os.path.join(PROJECT_ROOT, "oils_local_db.json")

_SESSION = {
    "xp": 0, "streak": 0, "max_streak": 0,
    "correct": 0, "wrong": 0,
    "experiments_done": [], "badges": [],
    "start_time": time.time()
}

def _save_to_local_db():
    """Saves user progress right to their local device — no cloud/backend needed!"""
    try:
        data = {
            "xp": _SESSION.get("xp", 0),
            "max_streak": _SESSION.get("max_streak", 0),
            "correct": _SESSION.get("correct", 0),
            "wrong": _SESSION.get("wrong", 0),
            "experiments_done": sorted(list(set(_SESSION.get("experiments_done", [])))),
            "badges": sorted(list(set(_SESSION.get("badges", [])))),
            "last_saved": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def _clear_local_db():
    """Removes the local database file and resets session to start fresh."""
    _SESSION["xp"] = 0
    _SESSION["streak"] = 0
    _SESSION["max_streak"] = 0
    _SESSION["correct"] = 0
    _SESSION["wrong"] = 0
    _SESSION["experiments_done"] = []
    _SESSION["badges"] = []
    if os.path.isfile(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

def _load_from_local_db():
    """Loads existing progress from the local device database on startup."""
    if os.path.isfile(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            _SESSION["xp"] = data.get("xp", 0)
            _SESSION["max_streak"] = data.get("max_streak", 0)
            _SESSION["correct"] = data.get("correct", 0)
            _SESSION["wrong"] = data.get("wrong", 0)
            _SESSION["experiments_done"] = data.get("experiments_done", [])
            _SESSION["badges"] = data.get("badges", [])
            return True
        except Exception:
            pass
    return False

def _init_profile_dialog():
    """Asks user on startup if they want to resume saved progress or start fresh."""
    if not os.path.isfile(DB_PATH):
        return
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        saved_xp = data.get("xp", 0)
        saved_badges = len(data.get("badges", []))
        saved_exps = len(data.get("experiments_done", []))
        if saved_xp == 0 and saved_badges == 0 and saved_exps == 0:
            return

        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}{'═'*78}{Color.RESET}")
        print("  💾 LOCAL DATABASE FOUND ON THIS DEVICE")
        print(f"{Color.CYAN}{Color.BOLD}{'═'*78}{Color.RESET}\n")
        print("  We found a previously saved adventure on your laptop:\n")
        print(f"    ⭐ Total XP     : {Color.YELLOW}{saved_xp} XP{Color.RESET} (Level {saved_xp // 100} · {_get_rank(saved_xp)})")
        print(f"    🎖️ Badges       : {Color.MAGENTA}{saved_badges} Unlocked{Color.RESET}")
        print(f"    🧪 Completed    : {Color.GREEN}{saved_exps} Lab Experiments{Color.RESET}")
        if data.get("last_saved"):
            print(f"    🕒 Last Saved   : {Color.DIM}{data.get('last_saved')}{Color.RESET}")
        print()
        print(f"  {Color.GREEN}{Color.BOLD}[Enter / C]{Color.RESET}  Continue your saved adventure")
        print(f"  {Color.YELLOW}{Color.BOLD}[F]{Color.RESET}          Start completely fresh from Level 0 (Reset local save)\n")

        choice = prompt_input(f"  {Color.BOLD}Your choice [Enter to continue, or 'F' to start fresh]: {Color.RESET}").strip().upper()
        if choice in ("F", "FRESH", "RESET", "NEW"):
            _clear_local_db()
            print(f"\n  {Color.YELLOW}✨ Local save cleared! Starting completely fresh from Level 0!{Color.RESET}")
            time.sleep(1.0)
        else:
            _load_from_local_db()
            print(f"\n  {Color.GREEN}✔ Welcome back! Loaded your saved adventure.{Color.RESET}")
            time.sleep(0.7)
    except Exception:
        pass

_BADGES = {
    "first_blood":   {"name": "🎯 First Blood", "desc": "Answer your very first question correctly!"},
    "streak_3":      {"name": "🔥 On A Roll", "desc": "Score a 3-question streak!"},
    "streak_5":      {"name": "⚡ Lightning Coder", "desc": "Score a 5-question streak without a single mistake!"},
    "streak_10":     {"name": "🌋 Unstoppable Force", "desc": "Score a 10-question winning streak!"},
    "git_survivor":  {"name": "🐙 Git Survivor", "desc": "Successfully resolve a real-world Git challenge!"},
    "dsa_doctor":    {"name": "🩺 DSA Specialist", "desc": "Diagnose and resolve a tricky DSA bug!"},
    "java_marshal":  {"name": "☕ JVM Whisperer", "desc": "Tame a Java runtime exception disaster!"},
    "xp_500":        {"name": "📚 Bookworm", "desc": "Earn 500 total XP!"},
    "xp_1000":       {"name": "💎 High Achiever", "desc": "Cross the 1,000 XP milestone!"},
    "xp_2500":       {"name": "👑 Code Master", "desc": "Attain 2,500 XP — dedicated mastery of 3rd sem code!"},
    "vault_dweller": {"name": "🔍 Code Inspector", "desc": "Inspect verified code inside the In-Terminal Code Vault!"},
    "quickfire_ace": {"name": "⚡ Quick-Fire Ace", "desc": "Complete the 5-Question Mixed Quick-Fire Gauntlet!"},
    "danger_radar":  {"name": "🧪 Git Bomb Defuser", "desc": "Inspect hazardous Git commands & master rescue plans in the Sandbox!"},
}

def _unlock_badge(badge_id):
    if badge_id in _BADGES and badge_id not in _SESSION["badges"]:
        _SESSION["badges"].append(badge_id)
        _save_to_local_db()
        b = _BADGES[badge_id]
        print(f"\n  {Color.MAGENTA}{Color.BOLD}╔════════════════════════════════════════════════════════════════════╗")
        print(f"  ║  🎖️  ACHIEVEMENT UNLOCKED: {b['name']:<39}║")
        print(f"  ║  ↳ {b['desc']:<62}║")
        print(f"  ╚════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

def _check_milestone_badges():
    if _SESSION["correct"] >= 1:
        _unlock_badge("first_blood")
    if _SESSION["streak"] >= 3:
        _unlock_badge("streak_3")
    if _SESSION["streak"] >= 5:
        _unlock_badge("streak_5")
    if _SESSION["streak"] >= 10:
        _unlock_badge("streak_10")
    if _SESSION["xp"] >= 500:
        _unlock_badge("xp_500")
    if _SESSION["xp"] >= 1000:
        _unlock_badge("xp_1000")
    if _SESSION["xp"] >= 2500:
        _unlock_badge("xp_2500")

_FUNNY_PRAISES = [
    "Awesome job! That was spot on! 🌟",
    "Your brain just connected the dots! 🧠✨",
    "High five! That was clean and accurate! 🙌",
    "You're making real progress, one step at a time! 🚀",
    "Look at that — you're getting comfortable with this! 💡",
    "Even your computer is nodding in approval! 💻✨",
    "Clean logic! That's how it's done! 🎯",
    "Step by step, you're picking this up! 🌱",
    "Great catch! Code makes sense when you take your time! 👏",
    "Your understanding just leveled up! 📈",
    "Brilliant! The concepts are starting to click! 🧩",
    "Nice and steady! You nailed that one! 💎",
    "Zero hesitation, perfect choice! 🎉",
    "You're building real programming intuition! 🧠",
    "Keep this energy going — you're doing great! ✨",
]

_FUNNY_ROASTS = [
    "Oops! No worries at all — even NASA engineers miss things! 🚀",
    "Nice try! Making mistakes is literally how we learn code! 🌱",
    "Brain had a little hiccup! Read the clue and take another shot! ☕",
    "Hey, learning code is tricky! Give yourself credit for trying! 💡",
    "Computer says 'Almost there!' Let's see why the other option works! 💻",
    "Don't sweat it! Even the creators of C had bugs on day one! 🤷",
    "Semicolons and brackets love playing hide-and-seek! Try again! 🙈",
    "Mistakes are just undocumented learning features! 🐛✨",
    "Every wrong answer gets you closer to the right one! 🎯",
    "Take a breath! Code is a journey, not a sprint! 🧘",
    "No big deal! That's why we have hints and second chances! 💡",
    "Debugging is 90% of programming anyway! You're in good company! 🔍",
    "A tiny slip! The explanation below makes it crystal clear! 📖",
    "Progress isn't a straight line — keep exploring! 🌟",
    "You've got this! One step at a time! 💪",
]

_MEME_QUOTES = [
    "\"It compiles. Ship it.\" — Every CS student ever 🚀",
    "\"Why does it work? I don't know and I'm scared to ask.\" 😰",
    "\"Undefined behaviour: a love story.\" 💔",
    "\"I'll fix it in production.\" — Famous last words 💀",
    "\"It works on my machine!\" — The classic alibi 🤷",
    "\"Just one more bug, then I'll sleep.\" (3 AM) 🌙",
    "\"git commit -m 'final_FINAL_v3_ACTUALLY_FINAL'\" 😭",
    "\"The code doesn't have bugs, it has undocumented features.\" 🐛✨",
    "\"Semicolon? What semicolon? Oh THAT semicolon!\" 🤦",
    "\"sudo make me a sandwich.\" — The engineer's prayer 🥪",
    "\"It's not a bug, it's a feature request from reality.\" 🌟",
    "\"Have you tried turning it off and on again?\" — Also engineering. 🔄",
    "\"Documentation? We don't do that here.\" 📚🚫",
    "\"rm -rf / — just kidding... mostly.\" 💣",
    "\"malloc(sizeof(clue)) returned NULL.\" — Classic student moment 😂",
    "\"The best code is simple code.\" — Smart thinker 🧠",
    "\"Take it one concept at a time. Nobody learns it in a day!\" ⏳",
    "\"// TODO: understand this when I wake up\" — real comment energy 📝",
]

_RANK_TITLES = [
    (0,    "🌱 Code Explorer"),
    (100,  "🐣 Curious Beginner"),
    (250,  "📚 Logic Builder"),
    (500,  "🔗 Pointer Friend"),
    (800,  "🧠 Pattern Finder"),
    (1200, "⚡ Code Crafter"),
    (1700, "🌟 Steady Developer"),
    (2500, "💎 Silicon Sage"),
]

def _get_rank(xp):
    rank = _RANK_TITLES[0][1]
    for threshold, title in _RANK_TITLES:
        if xp >= threshold:
            rank = title
    return rank

def _xp_bar(xp, width=40):
    """Returns a coloured ASCII XP progress bar string."""
    lvl = xp // 100
    xp_in_level = xp % 100
    filled = int(xp_in_level / 100 * width)
    bar = Color.GREEN + "█" * filled + Color.DIM + "░" * (width - filled) + Color.RESET
    return f"  {Color.BOLD}LVL {lvl}{Color.RESET} [{bar}] {xp_in_level}/100 XP  |  {Color.YELLOW}Total: {xp} XP{Color.RESET}  |  Rank: {_get_rank(xp)}"

def _award_xp(points, reason=""):
    """Awards XP, increments streak, prints XP gain line."""
    _SESSION["xp"] += points
    _SESSION["streak"] += 1
    _SESSION["correct"] += 1
    if _SESSION["streak"] > _SESSION["max_streak"]:
        _SESSION["max_streak"] = _SESSION["streak"]
    streak = _SESSION["streak"]
    xp = _SESSION["xp"]
    bonus = 0
    bonus_msg = ""
    if streak == 3:
        bonus = 25
        bonus_msg = f"  {Color.RED}🔥 HOT STREAK x3! Bonus +{bonus} XP!{Color.RESET}"
    elif streak == 5:
        bonus = 50
        bonus_msg = f"  {Color.RED}🔥🔥 ON FIRE x5! Bonus +{bonus} XP!{Color.RESET}"
    elif streak >= 7:
        bonus = 75
        bonus_msg = f"  {Color.RED}🔥🔥🔥 UNSTOPPABLE x{streak}! Bonus +{bonus} XP!{Color.RESET}"
    if bonus:
        _SESSION["xp"] += bonus
    fire = "🔥" * min(streak, 5)
    print(f"\n  {Color.GREEN}{Color.BOLD}+{points} XP!{Color.RESET}  Streak: {fire} x{streak}  |  Total: {Color.YELLOW}{xp + bonus} XP{Color.RESET}")
    if bonus_msg:
        print(bonus_msg)
    _check_milestone_badges()
    _save_to_local_db()

def _break_streak(reason=""):
    """Resets streak on wrong answer."""
    _SESSION["streak"] = 0
    _SESSION["wrong"] += 1
    _save_to_local_db()

def _show_session_header():
    """Print a compact XP/streak header at top of screens."""
    xp = _SESSION["xp"]
    streak = _SESSION["streak"]
    fire = ("🔥" * min(streak, 5)) if streak > 0 else "  "
    quote = random.choice(_MEME_QUOTES)
    print(f"  {Color.DIM}{quote}{Color.RESET}")
    print(_xp_bar(xp))
    status_line = []
    if streak >= 2:
        status_line.append(f"{Color.RED}{Color.BOLD}{fire} Streak x{streak}!{Color.RESET}")
    status_line.append(f"{Color.DIM}💾 Local DB: Active (Saved on your device){Color.RESET}")
    print(f"  {'  |  '.join(status_line)}\n")

def _end_of_session_summary():
    """Full end-of-session stats screen — asks before saving progress."""
    clear_screen()
    elapsed = int(time.time() - _SESSION["start_time"])
    mins = elapsed // 60
    secs = elapsed % 60
    xp = _SESSION["xp"]
    correct = _SESSION["correct"]
    wrong = _SESSION["wrong"]
    total = correct + wrong
    accuracy = int(correct / total * 100) if total > 0 else 0
    rank = _get_rank(xp)
    exps_done = len(_SESSION["experiments_done"])

    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*72}{Color.RESET}")
    print(f"{Color.MAGENTA}{Color.BOLD}  🎮 SESSION COMPLETE — OILS-3 MASTER ARCADE{Color.RESET}")
    print(f"{Color.MAGENTA}{Color.BOLD}{'═'*72}{Color.RESET}\n")

    typewrite(f"  ⏱️  Time Played   : {mins}m {secs}s", 0.012, Color.CYAN)
    typewrite(f"  🧪 Experiments   : {exps_done} completed", 0.012, Color.GREEN)
    typewrite(f"  ✅ Correct       : {correct}", 0.012, Color.GREEN)
    typewrite(f"  ❌ Wrong         : {wrong}", 0.012, Color.RED)
    typewrite(f"  🎯 Accuracy      : {accuracy}%", 0.012, Color.YELLOW)
    typewrite(f"  🔥 Best Streak   : x{_SESSION['max_streak']}", 0.012, Color.RED)
    print()
    typewrite(f"  {Color.YELLOW}{Color.BOLD}Total XP Earned  : {xp} XP{Color.RESET}", 0.012)
    typewrite(f"  {Color.CYAN}{Color.BOLD}Current Rank     : {rank}{Color.RESET}", 0.015)
    print()
    badges_count = len(_SESSION["badges"])
    typewrite(f"  🎖️ Badges Earned : {badges_count}/{len(_BADGES)} Unlocked", 0.012, Color.MAGENTA)
    if _SESSION["badges"]:
        badge_names = ", ".join(_BADGES[bid]["name"] for bid in _SESSION["badges"])
        print(f"     ↳ {badge_names}")
    print()
    print(_xp_bar(xp, width=50))
    print()

    if accuracy >= 90:
        typewrite("  🌟 FANTASTIC SESSION! You're building genuine understanding, step by step! 💎", 0.015, Color.GREEN)
    elif accuracy >= 70:
        typewrite("  🌟 Really good effort! Every single concept you practice is starting to click!", 0.015, Color.YELLOW)
    elif accuracy >= 50:
        typewrite("  📚 Steady progress! Take your time, learning to code is a gradual journey!", 0.015, Color.CYAN)
    else:
        typewrite("  💡 Learning to code takes patience and practice. You took great steps today! 🫡", 0.015, Color.WHITE)

    print(f"\n{Color.CYAN}{'─'*72}{Color.RESET}")
    print(f"  {Color.BOLD}💾 LOCAL DEVICE DATABASE SAVE:{Color.RESET}")
    print("  Do you want to save what you've done until now to this device,")
    print("  or would you like to start fresh when you open the terminal again?\n")
    print(f"    {Color.GREEN}[Enter / Y]{Color.RESET}  Save my progress to this device (Resume next time)")
    print(f"    {Color.YELLOW}[N / F]{Color.RESET}      Don't save — start completely fresh next time\n")
    save_choice = prompt_input(f"  {Color.BOLD}Save progress to device? [Y/n]: {Color.RESET}").strip().upper()

    if save_choice in ("", "Y", "YES", "S", "SAVE"):
        _save_to_local_db()
        print(f"\n  {Color.GREEN}✔ Progress saved locally on your device! You can pick up right here next time! 🫡{Color.RESET}\n")
    else:
        _clear_local_db()
        print(f"\n  {Color.YELLOW}🔄 Local save cleared! You will start completely fresh next time! 🫡{Color.RESET}\n")

    print(f"{Color.MAGENTA}{Color.BOLD}{'═'*72}{Color.RESET}\n")
    prompt_input("  Press Enter to exit... 🫡  ")

def _show_trophy_case():
    """Displays the interactive achievement trophy case."""
    clear_screen()
    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*78}{Color.RESET}")
    print("  🏆 OILS-3 TROPHY CASE & ACHIEVEMENT CABINET")
    print(f"{Color.MAGENTA}{Color.BOLD}{'═'*78}{Color.RESET}")
    _show_session_header()

    unlocked_count = len(_SESSION["badges"])
    total_count = len(_BADGES)
    print(f"  {Color.BOLD}Your Collection: {Color.YELLOW}{unlocked_count}/{total_count} Badges Unlocked{Color.RESET}\n")

    for bid, b in _BADGES.items():
        if bid in _SESSION["badges"]:
            status = f"{Color.GREEN}{Color.BOLD}[🏆 UNLOCKED]{Color.RESET}"
            title = f"{Color.GREEN}{Color.BOLD}{b['name']}{Color.RESET}"
        else:
            status = f"{Color.DIM}[🔒 LOCKED]{Color.RESET}  "
            title = f"{Color.DIM}{b['name']}{Color.RESET}"
        print(f"  {status} {title:<36} {Color.DIM}— {b['desc']}{Color.RESET}")

    print(f"\n{Color.DIM}{'─'*78}{Color.RESET}")
    prompt_input("\n  Press Enter to return to Main Arcade Menu... ")

BANNER_ART = r"""
   ____  ___ _     ____       _____
  / __ \|_ _| |   / ___|     |___ /
 | |  | || || |   \___ \ _____  |_ \
 | |__| || || |___ ___) |_____|___) |
  \____/|___|_____|____/      |____/
"""

BANNER = f"""{Color.CYAN}{Color.BOLD}{BANNER_ART}{Color.RESET}
{Color.YELLOW}{Color.BOLD}        🚀 Oops, I Learnt Something! — 3rd Sem Engineering Survival Arcade (VTU 2025)
{Color.DIM}        Git · DSA Lab (1BCSL306) · Java OOP Lab (1BCS302){Color.RESET}
"""



# Inject real funny praise and roast lists into arcade.core
_core_mod._FUNNY_PRAISES = _FUNNY_PRAISES
_core_mod._FUNNY_ROASTS = _FUNNY_ROASTS
