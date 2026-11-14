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
    "Spot on buddy! You nailed the core logic! ❤️",
    "Great job! That's exactly how it works in memory. 🧠✨",
    "Brilliant catch! You're really mastering this concept step by step. 🌱",
    "Clean and confident! Keep this momentum going, we've got this! 🙌",
    "Awesome! Your conceptual foundation is getting super solid. 💡",
    "You're making genuine progress, one experiment at a time! 🚀",
    "Look at that — you're getting really comfortable with this! 👏",
    "Step by step, everything is starting to make sense! 🧩",
    "Perfect answer buddy! The examiner will love this clarity. 🌟",
    "You're building real engineering intuition! 💎",
]

_FUNNY_ROASTS = [
    "No worries at all buddy! Learning code takes patience — let's review why this works. ❤️",
    "You're close! Take a breath, trace the logic step-by-step, and it will click. 💡",
    "Mistakes are just steps on the way to mastery! Let's break down the concept together. 🌱",
    "Don't worry buddy, tricky concepts take a moment. We will face it together! 🤝",
    "Good try! Look at the underlying principle and you'll see why the other option fits. 🔍",
    "Every small attempt gets you closer to cracking your lab exam! Keep your spirits high! ✨",
    "Take your time buddy! Nobody masters memory and syntax in a single day. ☕",
    "No stress at all! Let's check the explanation below to make it crystal clear. 📖",
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

def _make_progress_bar(done_count, total_count, width=40):
    """Returns an ASCII progress bar string."""
    pct = int((done_count / total_count) * 100) if total_count > 0 else 0
    pct = min(100, pct)
    filled = int(pct / 100 * width)
    bar = Color.GREEN + "█" * filled + Color.DIM + "░" * (width - filled) + Color.RESET
    return f"[{bar}] {done_count:2d}/{total_count:2d} Experiments ({pct}%)"

def _get_subject_counts():
    """Returns (git_done, dsa_done, java_done)."""
    exps = set(_SESSION.get("experiments_done", []))
    git_done = len([e for e in exps if str(e).startswith("GIT-")])
    dsa_done = len([e for e in exps if str(e).startswith("DSA-")])
    java_done = len([e for e in exps if str(e).startswith("JAVA-")])
    return git_done, dsa_done, java_done

def _completion_bar(width=40):
    """Returns overall completion progress across all subjects."""
    git_done, dsa_done, java_done = _get_subject_counts()
    total_done = git_done + dsa_done + java_done
    total_target = 34  # 12 Git + 12 DSA + 10 Java
    pct = int((total_done / total_target) * 100) if total_target > 0 else 0
    pct = min(100, pct)
    filled = int(pct / 100 * width)
    bar = Color.GREEN + "█" * filled + Color.DIM + "░" * (width - filled) + Color.RESET
    return f"Completion [{bar}] {pct}/100 %"

def _xp_bar(xp=None, width=40):
    """Progress bar string."""
    return f"  {_completion_bar(width)}"

def _award_xp(points, reason=""):
    """Records progress calmly and unlocks any milestone badges."""
    _SESSION["xp"] += points
    _SESSION["streak"] += 1
    _SESSION["correct"] += 1
    if _SESSION["streak"] > _SESSION["max_streak"]:
        _SESSION["max_streak"] = _SESSION["streak"]
    _check_milestone_badges()
    _save_to_local_db()

def _break_streak(reason=""):
    """Records incorrect answer without harsh penalties."""
    _SESSION["streak"] = 0
    _SESSION["wrong"] += 1
    _save_to_local_db()

def _show_session_header(show_welcome=True, subject=None):
    """Print clean learning progress and local DB status header."""
    if show_welcome:
        print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}")

    git_done, dsa_done, java_done = _get_subject_counts()

    if subject == "git":
        bar = _make_progress_bar(git_done, 12, width=40)
        print(f"  {Color.BOLD}Git Lab (1BCSL307A):{Color.RESET}   {bar}")
    elif subject == "dsa":
        bar = _make_progress_bar(dsa_done, 12, width=40)
        print(f"  {Color.BOLD}DSA Lab (1BCSL306):{Color.RESET}    {bar}")
    elif subject == "java":
        bar = _make_progress_bar(java_done, 10, width=40)
        print(f"  {Color.BOLD}Java Lab (1BCS302):{Color.RESET}    {bar}")
    else:
        bar_git = _make_progress_bar(git_done, 12, width=40)
        bar_dsa = _make_progress_bar(dsa_done, 12, width=40)
        bar_java = _make_progress_bar(java_done, 10, width=40)
        print(f"  {Color.BOLD}Git Lab (1BCSL307A):{Color.RESET}   {bar_git}")
        print(f"  {Color.BOLD}DSA Lab (1BCSL306):{Color.RESET}    {bar_dsa}")
        print(f"  {Color.BOLD}Java Lab (1BCS302):{Color.RESET}    {bar_java}")

    print(f"  {Color.DIM}💾 Local DB: Active (Saved on your device){Color.RESET}\n")

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
{Color.YELLOW}{Color.BOLD}        🚀 Oops, I Learnt Something! — 3rd Sem Engineering, An Interactive Game to Crack Your Labs (VTU 2025 Scheme)
{Color.DIM}        Git (1BCSL307A) · DSA Lab (1BCSL306) · Java OOP Lab (1BCS302){Color.RESET}
"""



# Inject real funny praise and roast lists into arcade.core
_core_mod._FUNNY_PRAISES = _FUNNY_PRAISES
_core_mod._FUNNY_ROASTS = _FUNNY_ROASTS
