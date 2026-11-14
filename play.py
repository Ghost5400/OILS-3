#!/usr/bin/env python3
"""
🎮 OILS-3: OOPS, I LEARNT SOMETHING! (3rd Sem Engineering Edition)
Author: Prajwal D. Chonnad
Repository: prajwalchonnad/OILS-3

Master Arcade Hub for all three 3rd-Sem engineering lab subjects:
  - 🐙 Git Mastery & Survival Arcade
  - 🌳 DSA Lab Studio (1BCSL306 — 12 Experiments, VTU 2025 Scheme)
  - ☕ Java OOP Lab Studio (1BCS302 — 10 Experiments, VTU 2025 Scheme)
"""

import os
import sys
import time
import random
import subprocess

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        os.system("chcp 65001 >nul 2>&1")
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def _configure_console():
    # Auto-launch into a dedicated spacious window on Windows
    if sys.platform == "win32" and "--new-window" not in sys.argv and "--no-window" not in sys.argv:
        script_path = os.path.abspath(__file__)
        try:
            subprocess.Popen(
                [sys.executable, script_path, "--new-window"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print("\n\033[92m[*] Launching 'OILS-3: Master Arcade Hub' in a new dedicated window! 🚀\033[0m\n")
            sys.exit(0)
        except Exception:
            pass

    if sys.platform == "win32":
        try:
            os.system("title 🎮 OILS-3: Oops, I Learnt Something! (3rd Sem Master Arcade)")
            os.system("mode con: cols=112 lines=42 >nul 2>&1")
        except Exception:
            pass

# ── Arcade Submodule Imports ────────────────────────────────────────────────
from arcade.core import (
    Color, clear_screen, prompt_input, spinner,
    print_slow, typewrite, anim_correct, anim_wrong,
)
from arcade.session import (
    _SESSION, _award_xp, _break_streak, _unlock_badge,
    _show_session_header, _end_of_session_summary, _show_trophy_case,
    _init_profile_dialog, _get_rank, _xp_bar,
    BANNER, _BADGES, _clear_local_db,
)
from arcade.git.story import (
    mode_git_arcade, VIVA_QUESTIONS,
)
from arcade.git.sandbox import (
    mode_git_command_sandbox,
    analyze_universal_git_command,
)
from arcade.dsa.studio import mode_dsa_studio, DSA_EXPERIMENTS
from arcade.java.studio import mode_java_studio, JAVA_EXPERIMENTS
from arcade.vault import _show_code_vault

__all__ = [
    "analyze_universal_git_command",
    "mode_git_command_sandbox",
    "main",
]

def mode_quickfire_gauntlet():
    clear_screen()
    print(f"\n{Color.YELLOW}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   ⚡ QUICK-FIRE 5-QUESTION DRILL — DOUBLE XP SPEED RUN! (Git · DSA · Java)   ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}")
    print_slow("5 questions chosen randomly across Git, DSA, and Java. Answer fast for 2X XP!\n", 0.010, Color.CYAN)

    pool = []

    # Git viva questions
    for q in random.sample(VIVA_QUESTIONS, min(2, len(VIVA_QUESTIONS))):
        formatted_opts = []
        for opt in q["options"]:
            if opt.startswith(("A)", "B)", "C)", "D)")):
                formatted_opts.append(f"[{opt[0]}] {opt[3:]}")
            else:
                formatted_opts.append(opt)
        pool.append({
            "subject": "🐙 Git Mastery",
            "prompt": q["q"],
            "opts": formatted_opts,
            "correct": q["ans"],
            "praise": q["praise"],
            "roast": q["roast"]
        })

    # DSA experiment challenges
    dsa_candidates = [e for e in DSA_EXPERIMENTS if "challenge" in e and "opts" in e["challenge"]]
    for e in random.sample(dsa_candidates, min(2, len(dsa_candidates))):
        ch = e["challenge"]
        pool.append({
            "subject": f"🌳 DSA Lab (Exp {e['num']:02d})",
            "prompt": ch["prompt"],
            "opts": ch["opts"],
            "correct": ch.get("correct_opt", "A"),
            "praise": ch.get("praise", "Correct!"),
            "roast": ch.get("roast", "Wrong!")
        })

    # Java experiment challenges
    java_candidates = [e for e in JAVA_EXPERIMENTS if "challenge" in e and "opts" in e["challenge"]]
    for e in random.sample(java_candidates, min(1, len(java_candidates))):
        ch = e["challenge"]
        pool.append({
            "subject": f"☕ Java OOP (Exp {e['num']:02d})",
            "prompt": ch["prompt"],
            "opts": ch["opts"],
            "correct": ch.get("correct_opt", "A"),
            "praise": ch.get("praise", "Correct!"),
            "roast": ch.get("roast", "Wrong!")
        })

    random.shuffle(pool)
    pool = pool[:5]

    score = 0
    for idx, q in enumerate(pool, 1):
        clear_screen()
        print(f"\n{Color.YELLOW}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║   ⚡ QUICK-FIRE DRILL: Question {idx}/5  |  Current Score: {score}/{idx-1}                   ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}")
        print(f"  {Color.MAGENTA}{Color.BOLD}Subject: {q['subject']}{Color.RESET}\n")
        print(f"  {Color.BOLD}{Color.WHITE}{q['prompt']}{Color.RESET}\n")

        for opt in q["opts"]:
            print(f"    {Color.CYAN}{opt}{Color.RESET}")

        while True:
            ans = prompt_input(f"\n{Color.BOLD}Your Answer [A / B / C / D] (0=Menu): {Color.RESET}").strip().upper()
            if ans in ("0", "MENU", "Q", "EXIT"):
                return
            if ans in ("A", "B", "C", "D"):
                break
            print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")

        spinner("Evaluating response at 2X speed", duration=0.4, color=Color.YELLOW)

        if ans == q["correct"]:
            anim_correct()
            _award_xp(100, "quickfire drill 2x")
            score += 1
            print(f"\n{Color.GREEN}{Color.BOLD}🎉 {q['praise']} (+100 XP){Color.RESET}\n")
        else:
            anim_wrong()
            _break_streak()
            print(f"\n{Color.RED}{Color.BOLD}❌ {q['roast']}{Color.RESET}")
            print(f"   {Color.YELLOW}Expected: ({q['correct']}){Color.RESET}\n")

        prompt_input(f"{Color.DIM}Press Enter for next question...{Color.RESET}")

    clear_screen()
    print(f"\n{Color.MAGENTA}{Color.BOLD}{'═'*72}{Color.RESET}")
    print(f"  ⚡ QUICK-FIRE DRILL RESULTS: {score}/5 Correct!")
    print(f"{Color.MAGENTA}{Color.BOLD}{'═'*72}{Color.RESET}\n")

    if score == 5:
        anim_correct()
        _unlock_badge("quickfire_ace")
        _award_xp(200, "perfect quickfire drill")
        typewrite("  👑 PERFECT 5/5! Incredible focus and clean code logic! 🌟", 0.015, Color.GREEN)
        print(f"  {Color.YELLOW}{Color.BOLD}+200 BONUS XP AWARDED!{Color.RESET}\n")
    elif score >= 3:
        typewrite(f"  🌟 Solid performance ({score}/5)! Keep practicing to hit 5/5!", 0.015, Color.YELLOW)
    else:
        typewrite(f"  💡 {score}/5 — Don't worry, hit the lab modes and try again!", 0.015, Color.CYAN)

    print()
    print(_xp_bar(_SESSION["xp"]))
    prompt_input(f"\n{Color.DIM}Press Enter to return to Main Arcade Menu...{Color.RESET}")

def main():
    _init_profile_dialog()
    while True:
        clear_screen()
        print(BANNER)

        if _SESSION["xp"] > 0:
            print(f"  {Color.GREEN}💾 Active Profile: {_SESSION['xp']} XP · Level {_SESSION['xp']//100} ({_get_rank(_SESSION['xp'])}) · {len(_SESSION['badges'])} Badges Unlocked{Color.RESET}\n")

        # Funny time-of-day greeting
        hour = time.localtime().tm_hour
        if 5 <= hour < 12:
            greeting = "Good morning! Time to malloc() some knowledge ☕"
        elif 12 <= hour < 17:
            greeting = "Good afternoon! Pointers won't fix themselves 🌞"
        elif 17 <= hour < 21:
            greeting = "Good evening! One more experiment before dinner? 🍕"
        else:
            greeting = "Late night grind! Your laptop is judging you 🌙"
        print(f"  {Color.YELLOW}{greeting}{Color.RESET}")
        _show_session_header()

        print(f"{Color.BOLD}MAIN ARCADE SELECTION:{Color.RESET}")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 🐙  {Color.BOLD}Git Mastery & Survival Arcade{Color.RESET}  {Color.DIM}(9 Stages · Disaster Drills · Boss Battle){Color.RESET}")
        print(f"      {Color.DIM}↳ Learn git add, commit, branch, merge, rebase, cherry-pick, stash, conflict resolution{Color.RESET}")

        print(f"\n  {Color.GREEN}[2]{Color.RESET} 🌳  {Color.BOLD}DSA Lab Studio{Color.RESET}  {Color.DIM}(1BCSL306 · 12 Experiments · VTU 2025 Scheme){Color.RESET}")
        print(f"      {Color.DIM}↳ Visualizers (Stack & Linked List), Block Logic, Code Challenges, Disaster Recovery, Viva{Color.RESET}")

        print(f"\n  {Color.CYAN}[3]{Color.RESET} ☕  {Color.BOLD}Java OOP Lab Studio{Color.RESET}  {Color.DIM}(1BCS302 · 10 Experiments · VTU 2025 Scheme){Color.RESET}")
        print(f"      {Color.DIM}↳ Polymorphism & Thread Visualizers, Block Logic, Code Challenges, Disaster Recovery, Viva{Color.RESET}")

        print(f"\n  {Color.MAGENTA}[4]{Color.RESET} ⚡  {Color.BOLD}Quick Reference & In-Terminal Code Vault{Color.RESET}")
        print(f"      {Color.DIM}↳ Instant in-terminal access to all 22 verified C & Java source files{Color.RESET}")

        print(f"\n  {Color.YELLOW}[Q]{Color.RESET} ⚡  {Color.BOLD}Quick-Fire 5-Question Drill{Color.RESET}  {Color.RED}(🔥 2X DOUBLE XP SPEED RUN!){Color.RESET}")
        print(f"      {Color.DIM}↳ Mixed questions from Git, DSA, and Java — high speed, high reward!{Color.RESET}")

        print(f"\n  {Color.MAGENTA}[T]{Color.RESET} 🏆  {Color.BOLD}Trophy Case & Achievements{Color.RESET}  {Color.DIM}({len(_SESSION['badges'])}/{len(_BADGES)} Unlocked){Color.RESET}")

        print(f"\n  {Color.DIM}[R]{Color.RESET} 🔄  {Color.DIM}Start Fresh / Reset Local Progress{Color.RESET}")
        print(f"  {Color.DIM}[5]{Color.RESET} 🏃  Exit to Terminal  {Color.DIM}(choose whether to save progress){Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Enter your choice [1 - 5, Q, T, R]: {Color.RESET}").strip().upper()

        if choice == "1":
            mode_git_arcade()
        elif choice == "2":
            mode_dsa_studio()
        elif choice == "3":
            mode_java_studio()
        elif choice == "4":
            _show_code_vault()
        elif choice == "Q":
            mode_quickfire_gauntlet()
        elif choice == "T":
            _show_trophy_case()
        elif choice == "R":
            clear_screen()
            print(f"\n{Color.YELLOW}{Color.BOLD}🔄 START FRESH / RESET LOCAL SAVE{Color.RESET}\n")
            print("  This will clear your saved XP, streaks, and badges on this device so you can start over from scratch.\n")
            confirm = prompt_input(f"  {Color.RED}Are you sure you want to reset to Level 0? [y/N]: {Color.RESET}").strip().upper()
            if confirm in ("Y", "YES"):
                _clear_local_db()
                print(f"\n  {Color.GREEN}✔ Save cleared! Starting completely fresh from Level 0! 🫡{Color.RESET}\n")
            else:
                print(f"\n  {Color.CYAN}Reset cancelled. Your saved progress is safe!{Color.RESET}\n")
            time.sleep(1.0)
        elif choice in ("5", "0", "EXIT"):
            _end_of_session_summary()
            break

if __name__ == "__main__":
    _configure_console()
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Game exited. Bye soldier! 🫡{Color.RESET}\n")
    except Exception as e:
        print(f"\n{Color.RED}Something went wrong: {e}{Color.RESET}\n")
        import traceback
        traceback.print_exc()
        prompt_input("\nPress Enter to exit...")
