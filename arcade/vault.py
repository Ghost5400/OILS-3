"""
arcade.vault — In-Terminal Code Vault and source file viewer.
Instant access to all verified source files, experiments, and commands across Git, DSA, and Java.
"""
import os

from arcade.core import PROJECT_ROOT, Color, clear_screen, prompt_input
from arcade.session import _unlock_badge, _SESSION, _save_to_local_db
from arcade.git.story import LAB_EXPERIMENTS

def _view_source_file(file_path, title):
    clear_screen()
    _unlock_badge("vault_dweller")
    print(f"\n{Color.CYAN}{Color.BOLD}================================================================================{Color.RESET}")
    print(f"  📄 CODE VIEWER: {title}")
    print(f"  Path: {file_path}")
    print(f"{Color.CYAN}{Color.BOLD}================================================================================{Color.RESET}\n")

    if not os.path.isfile(file_path):
        print(f"{Color.RED}File not found at: {file_path}{Color.RESET}\n")
        prompt_input("Press Enter to return...")
        return

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    for idx, l in enumerate(lines, 1):
        print(f"{Color.DIM}{idx:3d} |{Color.RESET} {l}", end="")

    print(f"\n{Color.CYAN}{Color.BOLD}================================================================================{Color.RESET}")
    print(f"  Total lines: {len(lines)} | Clean, verified code to explore and learn at your own pace!")
    prompt_input("\nPress Enter to return to Code Vault...")

def _view_git_experiment(step_code, name, code, step_num=None):
    clear_screen()
    _unlock_badge("vault_dweller")
    if step_num:
        exp_id = f"GIT-{step_num}"
        if exp_id not in _SESSION["experiments_done"]:
            _SESSION["experiments_done"].append(exp_id)
            _save_to_local_db()

    print(f"\n{Color.YELLOW}{Color.BOLD}================================================================================{Color.RESET}")
    print(f"  🐙 GIT LAB EXPERIMENT: {step_code} — {name}")
    print(f"{Color.YELLOW}{Color.BOLD}================================================================================{Color.RESET}\n")
    print(f"{Color.WHITE}{code}{Color.RESET}\n")
    print(f"{Color.YELLOW}{Color.BOLD}================================================================================{Color.RESET}")
    print("  Ready-to-run verified Git workflow commands. Progress saved! ❤️")
    prompt_input("\nPress Enter to return to Code Vault...")

def _show_code_vault():
    while True:
        clear_screen()
        print(f"\n{Color.MAGENTA}{Color.BOLD}================================================================================{Color.RESET}")
        print("  ⚡ QUICK REFERENCE & CODE VAULT — Full In-Terminal Program Viewer")
        print(f"  {Color.YELLOW}Welcome buddy , don't worry I am there for u ❤️ ; we will face it together...{Color.RESET}")
        print(f"{Color.MAGENTA}{Color.BOLD}================================================================================{Color.RESET}\n")

        base = PROJECT_ROOT
        dsa_dir = os.path.join(base, "dsa-lab", "programs")
        java_dir = os.path.join(base, "java-lab", "programs")

        print(f"  {Color.GREEN}{Color.BOLD}🌳 DSA Lab Programs (C — 1BCSL306 · 12 Programs):{Color.RESET}")
        dsa_files = sorted(f for f in os.listdir(dsa_dir) if f.endswith(".c")) if os.path.isdir(dsa_dir) else []
        for i, f in enumerate(dsa_files, 1):
            print(f"    {Color.CYAN}[D{i:02d}]{Color.RESET} {f}")

        print(f"\n  {Color.BLUE}{Color.BOLD}☕ Java Lab Programs (Java — 1BCS302 · 10 Programs):{Color.RESET}")
        java_files = sorted(f for f in os.listdir(java_dir) if f.endswith(".java")) if os.path.isdir(java_dir) else []
        for i, f in enumerate(java_files, 1):
            print(f"    {Color.CYAN}[J{i:02d}]{Color.RESET} {f}")

        print(f"\n  {Color.YELLOW}{Color.BOLD}🐙 Git Lab Experiments (1BCSL307A · 12 Experiments):{Color.RESET}")
        for i, (step_code, name, _) in enumerate(LAB_EXPERIMENTS, 1):
            print(f"    {Color.CYAN}[G{i:02d}]{Color.RESET} {step_code}: {name}")

        print(f"\n  {Color.MAGENTA}[DOC1]{Color.RESET} GIT_FOR_HUMANS.md — Zero-jargon visual guide")
        print(f"  {Color.MAGENTA}[DOC2]{Color.RESET} GIT_COMMANDS.md  — Complete Git cheatsheet")

        print(f"\n  {Color.DIM}[0]  ⬅️   Back to Master Hub{Color.RESET}\n")

        choice = prompt_input("Select code to view in terminal [D01-D12 / J01-J10 / G01-G12 / DOC1-DOC2 / 0]: ").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice.startswith("D") and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            if 0 <= idx < len(dsa_files):
                _view_source_file(os.path.join(dsa_dir, dsa_files[idx]), dsa_files[idx])
        elif choice.startswith("J") and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            if 0 <= idx < len(java_files):
                _view_source_file(os.path.join(java_dir, java_files[idx]), java_files[idx])
        elif choice.startswith("G") and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            if 0 <= idx < len(LAB_EXPERIMENTS):
                step_code, name, code = LAB_EXPERIMENTS[idx]
                _view_git_experiment(step_code, name, code, idx + 1)
        elif choice in ("DOC1", "G1"):
            _view_source_file(os.path.join(base, 'GIT_FOR_HUMANS.md'), "Git for Humans Handbook")
        elif choice in ("DOC2", "G2"):
            _view_source_file(os.path.join(base, 'GIT_COMMANDS.md'), "Git Commands Ninja Cheatsheet")

# ==============================================================================
# 🐙 GIT ARCADE SUB-MENU (Option 1)
# ==============================================================================

