"""
arcade.git.studio — Git Lab Studio (1BCSL307A — 12 Experiments, VTU 2025 Scheme).
Strictly experiment-grounded engineering lab companion, command library & viva hub.
"""
import os
import time
import random

from arcade.core import (
    Color, clear_screen, prompt_input, spinner,
    print_slow, anim_correct, anim_wrong,
)
from arcade.session import (
    _SESSION, _record_concept_mastered, _unlock_badge,
    _save_to_local_db, _show_session_header, BANNER,
)
from arcade.git.sandbox import mode_git_command_sandbox

# ==============================================================================
# 12 VTU GIT LAB EXPERIMENTS (1BCSL307A)
# ==============================================================================

GIT_EXPERIMENTS = [
    {
        "num": 1,
        "part": "A",
        "title": "Repository Setup, Config & Basic Commits",
        "concept": "Git is a content-addressable distributed version control system. Every commit represents an immutable snapshot of the entire project timeline stored in the hidden .git directory.",
        "problem": "Initialize a new repository using 'git init', configure user identity (name, email), create a sample file, stage it via 'git add', and commit it using 'git commit -m'. Verify the commit with 'git log'.",
        "commands": """# 1. Initialize local repository
git init

# 2. Configure user identity (Author details)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Create content & verify working directory
echo "VTU Git Lab 1BCSL307A" > readme.txt
git status

# 4. Stage changes to Index
git add readme.txt

# 5. Commit snapshot to history
git commit -m "docs: initialize repository with readme"

# 6. Verify commit history
git log --oneline""",
        "blocks": [
            {
                "title": "Initialization & Identity Configuration",
                "code": "git init\ngit config user.name \"Student Name\"\ngit config user.email \"student@college.edu\"",
                "purpose": "Creates the repository skeleton (.git directory) and establishes the author identity attached to all future commits.",
                "inside": [
                    "`git init`: Creates the hidden `.git/` folder containing object stores (objects/), reference pointers (refs/), and HEAD.",
                    "`git config user.name / email`: Writes identity into `.git/config` (or `~/.gitconfig` if `--global` is used). Every Git commit object cryptographically records this author string."
                ],
                "flow": [
                    "Step 1: Empty directory contains 0 version control metadata.",
                    "Step 2: `git init` generates `.git/` structure initialized on default branch (`main`).",
                    "Step 3: Identity configured so commits are attributed properly."
                ]
            },
            {
                "title": "The 3-Tier Workflow: Working Directory -> Staging Area -> Commit",
                "code": "echo \"VTU Git Lab\" > readme.txt\ngit status\ngit add readme.txt\ngit commit -m \"feat: add lab readme\"",
                "purpose": "Moves file modifications across Git's three physical zones: Working Tree to Index (Staging), and Index to permanent Repository history.",
                "inside": [
                    "`git status`: Queries working tree against index; reports untracked files in red.",
                    "`git add readme.txt`: Hashes file content into a Blob object (SHA-1/SHA-256) inside `.git/objects` and stages it in `.git/index`.",
                    "`git commit -m`: Writes a Tree object representing directory layout, creates a Commit object pointing to author, timestamp, parent commit, and tree."
                ],
                "flow": [
                    "Step 1: File created in Working Directory (Untracked).",
                    "Step 2: `git add` calculates SHA hash, writes blob to `.git/objects/`, updates `.git/index` (Staged).",
                    "Step 3: `git commit` creates immutable snapshot and advances branch HEAD pointer."
                ]
            }
        ],
        "challenge": {
            "prompt": "If you delete the hidden '.git' directory inside your project folder, what happens?",
            "opts": [
                "A) Your files are deleted, but commit history remains safely in RAM.",
                "B) You permanently destroy the repository, all commit history, and branches on this machine.",
                "C) Git automatically restores the history from GitHub cloud.",
                "D) The operating system throws a segmentation fault."
            ],
            "correct_opt": "B",
            "hint": "The .git folder IS the entire repository. Deleting it leaves only raw, unversioned working files.",
            "praise": "Exactly right! Everything Git knows lives strictly inside the .git directory.",
            "roast": "Incorrect! The .git folder IS the repository. Without it, all version history is lost."
        }
    },
    {
        "num": 2,
        "part": "A",
        "title": "Creating, Switching & Merging Branches",
        "concept": "In Git, a branch is not a copy of files; it is simply a 41-byte pointer file containing the 40-character SHA hash of its tip commit. Creating and switching branches is instantaneous.",
        "problem": "Create a new branch named 'feature-branch', switch to it, make and commit changes in isolation, switch back to 'main' / 'master', and merge 'feature-branch' using fast-forward merge.",
        "commands": """# 1. Create and switch to new branch
git checkout -b feature-branch
# (Alternative modern syntax: git switch -c feature-branch)

# 2. Modify files on branch
echo "New feature logic" >> feature.txt
git add feature.txt
git commit -m "feat: implement initial feature logic"

# 3. Switch back to main branch
git checkout main
# (Alternative: git switch main)

# 4. Merge feature branch into main
git merge feature-branch

# 5. Clean up merged branch
git branch -d feature-branch""",
        "blocks": [
            {
                "title": "Branch Creation & HEAD Repointing",
                "code": "git checkout -b feature-branch\n# Modern syntax:\ngit switch -c feature-branch",
                "purpose": "Creates a new lightweight branch reference pointer and points the symbolic HEAD reference to it.",
                "inside": [
                    "`-b` / `-c`: Tells Git to create the branch file in `.git/refs/heads/<name>` before checking it out.",
                    "`HEAD`: Symbolically points to `refs/heads/feature-branch`. Any subsequent commit advances `feature-branch`, leaving `main` untouched."
                ],
                "flow": [
                    "Step 1: `feature-branch` pointer created pointing to the current commit SHA.",
                    "Step 2: HEAD updated to point to `refs/heads/feature-branch`.",
                    "Step 3: Working directory reflects `feature-branch` state."
                ]
            },
            {
                "title": "Fast-Forward Merge Mechanism",
                "code": "git checkout main\ngit merge feature-branch",
                "purpose": "Integrates the isolated commits from `feature-branch` into `main` without creating a superfluous merge commit when history is linear.",
                "inside": [
                    "`git checkout main`: Moves HEAD back to `refs/heads/main`.",
                    "`git merge feature-branch`: Git checks if `main` has diverged. If no new commits were made on `main`, it simply moves the `main` pointer forward to match `feature-branch` (Fast-Forward)."
                ],
                "flow": [
                    "Step 1: Check merge-base ancestor of `main` and `feature-branch`.",
                    "Step 2: Since ancestor equals `main`, Git performs Fast-Forward: pointer slides forward.",
                    "Step 3: No merge commit is created; linear history preserved."
                ]
            }
        ],
        "challenge": {
            "prompt": "What does a Fast-Forward merge do internally?",
            "opts": [
                "A) Creates a new 3-way merge commit with two parents.",
                "B) Compresses all commits on the branch into a single zip archive.",
                "C) Simply slides the target branch pointer forward to the tip of the merged branch without creating a new commit.",
                "D) Copies each commit onto a remote server."
            ],
            "correct_opt": "C",
            "hint": "When no commits exist on main since the branch split, Git only needs to update the pointer.",
            "praise": "Spot on! Fast-Forward is a simple pointer advance — O(1) time complexity.",
            "roast": "Not quite. Fast-forward creates NO new commit; it simply advances the branch pointer."
        }
    },
    {
        "num": 3,
        "part": "A",
        "title": "Stashing Work in Progress",
        "concept": "Stashing takes your uncommitted modifications (staged and unstaged) and saves them onto a dirty working directory stack, reverting your working tree to clean HEAD state.",
        "problem": "Modify tracked files while working on a feature, save unfinished work to the stash stack using 'git stash push -m', verify working tree is clean, inspect stash with 'git stash list', and restore changes using 'git stash pop'.",
        "commands": """# 1. Modify working files
echo "Incomplete draft" >> draft.txt

# 2. Stash unfinished work with a clear label
git stash push -m "WIP: draft calculations"

# 3. Verify clean working directory
git status

# 4. Inspect stash stack
git stash list

# 5. Restore work and drop from stash stack
git stash pop""",
        "blocks": [
            {
                "title": "Stash Creation & State Preservation",
                "code": "git stash push -m \"WIP: unfinished feature logic\"\ngit status",
                "purpose": "Temporarily shelves local modifications without polluting repository commit history with broken code.",
                "inside": [
                    "`git stash push -m`: Generates special commit objects in `.git/refs/stash` that capture both the index state and working directory modifications.",
                    "`git status`: Verifies that the working tree is clean (matching HEAD), allowing branch switches or pulling upstream changes safely."
                ],
                "flow": [
                    "Step 1: Uncommitted diffs calculated against HEAD.",
                    "Step 2: Diffs serialized into commit object pushed onto stash stack (`stash@{0}`).",
                    "Step 3: Working directory reset to HEAD."
                ]
            },
            {
                "title": "Stash Retrieval: Pop vs Apply",
                "code": "git stash list\ngit stash pop\n# Alternative to keep stash copy:\n# git stash apply",
                "purpose": "Re-applies saved diffs back onto the current working directory.",
                "inside": [
                    "`git stash list`: Displays all stashed snapshots (`stash@{0}`, `stash@{1}`).",
                    "`git stash pop`: Re-applies changes from `stash@{0}` AND removes it from the stash stack.",
                    "`git stash apply`: Re-applies changes but retains the entry in the stash stack."
                ],
                "flow": [
                    "Step 1: Target stash entry diff retrieved.",
                    "Step 2: Diff merged back into current working tree.",
                    "Step 3: If `pop` was invoked, `stash@{0}` is dropped from stack."
                ]
            }
        ],
        "challenge": {
            "prompt": "What is the critical difference between 'git stash pop' and 'git stash apply'?",
            "opts": [
                "A) pop deletes the repository; apply saves it.",
                "B) pop restores changes AND removes the stash from the stack; apply restores changes while keeping the stash on the stack.",
                "C) pop works only on main; apply works on any branch.",
                "D) apply requires internet connection; pop is local."
            ],
            "correct_opt": "B",
            "hint": "Think of standard stack data structures: pop removes the top element.",
            "praise": "BINGO! Pop applies and removes; Apply applies and retains.",
            "roast": "Remember your DSA stack rules! Pop removes the item from the stack; apply leaves it there."
        }
    },
    {
        "num": 4,
        "part": "A",
        "title": "Cloning Remote Repositories & Tracking",
        "concept": "Cloning creates a full local replica of a remote repository, including its entire commit history, all branches, tags, and automatically sets up remote tracking branches under 'origin/'.",
        "problem": "Clone an existing remote repository from GitHub/GitLab using 'git clone', inspect configured remotes with 'git remote -v', and check tracking branches with 'git branch -a'.",
        "commands": """# 1. Clone remote repository
git clone https://github.com/torvalds/subsurface-for-dirk.git my-repo

# 2. Enter cloned repository
cd my-repo

# 3. Inspect remote connections
git remote -v

# 4. View all local and remote-tracking branches
git branch -a

# 5. Inspect remote tracking details
git remote show origin""",
        "blocks": [
            {
                "title": "Remote Cloning & Object Transfer",
                "code": "git clone <url> <directory>\ncd <directory>",
                "purpose": "Copies all Git packfiles, trees, commits, and refs from a remote server to initialize a fully autonomous local repository.",
                "inside": [
                    "`git clone`: Performs 4 tasks automatically: 1) `git init`, 2) `git remote add origin <url>`, 3) `git fetch origin`, 4) `git checkout -b main origin/main`.",
                    "Result: You possess the entire project history offline on your machine."
                ],
                "flow": [
                    "Step 1: Remote server contacted, refs negotiated.",
                    "Step 2: Packfile downloaded into `.git/objects/pack`.",
                    "Step 3: Remote tracking branch `origin/main` created.",
                    "Step 4: Default branch checked out into working directory."
                ]
            },
            {
                "title": "Inspecting Remote Connections & Tracking",
                "code": "git remote -v\ngit branch -a",
                "purpose": "Validates the URLs used for fetching and pushing, and lists both local branches and read-only remote references.",
                "inside": [
                    "`git remote -v`: Shows fetch and push URLs for `origin`.",
                    "`git branch -a`: Lists local branches in green, and remote-tracking references (`remotes/origin/...`) in red."
                ],
                "flow": [
                    "Step 1: `.git/config` inspected for `[remote \"origin\"]` section.",
                    "Step 2: Prints fetch URL and push URL.",
                    "Step 3: Scans `refs/heads` (local) and `refs/remotes` (remote)."
                ]
            }
        ],
        "challenge": {
            "prompt": "Can you commit new code directly onto a remote tracking branch like 'origin/main'?",
            "opts": [
                "A) Yes, origin/main behaves exactly like any local branch.",
                "B) No, remote tracking branches (origin/*) are read-only bookmarks updated only by 'git fetch' or 'git pull'.",
                "C) Yes, if you use git commit -f.",
                "D) Only if you are logged in as root."
            ],
            "correct_opt": "B",
            "hint": "origin/main reflects the state of the server at the last fetch. You commit locally on main, then push.",
            "praise": "Excellent! origin/main is an immutable local bookmark of the remote state.",
            "roast": "Incorrect! origin/* branches are strictly read-only mirrors of the remote server."
        }
    },
    {
        "num": 5,
        "part": "A",
        "title": "Fetch & Rebase vs Merge",
        "concept": "Rebase rewrites project history by taking commits from your branch and re-applying them one-by-one on top of the upstream base branch, producing a completely linear timeline without merge bubbles.",
        "problem": "Fetch the latest changes from origin using 'git fetch origin', switch to your feature branch, rebase your commits onto 'origin/main' with 'git rebase origin/main', and understand linear history.",
        "commands": """# 1. Download remote commits without merging
git fetch origin

# 2. Switch to working branch
git checkout feature-branch

# 3. Re-apply feature commits on top of origin/main
git rebase origin/main

# 4. View resulting linear history
git log --oneline --graph""",
        "blocks": [
            {
                "title": "Fetching Remote Updates Safely",
                "code": "git fetch origin\ngit log HEAD..origin/main --oneline",
                "purpose": "Updates remote tracking branches (`origin/main`) without modifying any local working files or moving local branch pointers.",
                "inside": [
                    "`git fetch`: Contacts remote repository, downloads new commit objects into `.git/objects/`, updates pointer `.git/refs/remotes/origin/main`.",
                    "`HEAD..origin/main`: Shows commits present on the remote but not yet in your local branch."
                ],
                "flow": [
                    "Step 1: Network handshake with remote.",
                    "Step 2: New commit objects downloaded into object store.",
                    "Step 3: `origin/main` pointer advanced; local working tree remains 100% untouched."
                ]
            },
            {
                "title": "Rebase: Linear History Re-application",
                "code": "git checkout feature-branch\ngit rebase origin/main",
                "purpose": "Re-parents your branch commits on top of the newest commit of `origin/main`, avoiding non-linear merge commits.",
                "inside": [
                    "`git rebase`: Temporarily saves feature branch commits as patches, resets branch pointer to `origin/main`, and applies each patch sequentially.",
                    "Notice: The newly created commits receive NEW SHA hashes because their parent has changed!"
                ],
                "flow": [
                    "Step 1: Common ancestor identified.",
                    "Step 2: Commits on `feature-branch` saved to temporary patch storage.",
                    "Step 3: `feature-branch` pointer reset to `origin/main`.",
                    "Step 4: Commits replayed one-by-one with new parent SHAs."
                ]
            }
        ],
        "challenge": {
            "prompt": "Why do commits receive brand new SHA hashes when rebased?",
            "opts": [
                "A) Because the Git server generates random hashes every 24 hours.",
                "B) Because a commit's SHA hash is calculated from its content, author, timestamp, AND its PARENT commit hash. Changing the base changes the parent, producing a new hash.",
                "C) Git renames commits during rebase to save memory.",
                "D) The operating system modifies file inodes."
            ],
            "correct_opt": "B",
            "hint": "Git is content-addressable: if any property (including parent pointer) changes, the cryptographic hash changes.",
            "praise": "Brilliant! You understand Git's cryptographic Merkle DAG structure.",
            "roast": "Remember: Git SHAs include the parent pointer hash. Change the parent, and the hash changes completely!"
        }
    },
    {
        "num": 6,
        "part": "A",
        "title": "Merge with Custom Commit Message & No-Fast-Forward",
        "concept": "A 3-way merge integrates two divergent branches by computing a common ancestor, combining changes, and creating a new commit with TWO parents, recording the exact integration moment.",
        "problem": "Create divergent histories on 'main' and a feature branch, merge the feature branch using 'git merge --no-ff -m \"Merge feature module\"', and verify the 2-parent merge commit.",
        "commands": """# 1. Switch to main
git checkout main

# 2. Perform 3-way merge forcing a merge commit
git merge --no-ff feature-branch -m "merge: integrate user authentication module"

# 3. Verify two parent hashes in log
git log -n 1
git log --graph --oneline""",
        "blocks": [
            {
                "title": "Explicit Integration via --no-ff",
                "code": "git checkout main\ngit merge --no-ff feature-branch -m \"merge: integrate module\"",
                "purpose": "Forces Git to create an explicit merge commit even if a Fast-Forward merge was possible, preserving the historical group identity of the branch.",
                "inside": [
                    "`--no-ff`: Disables fast-forward pointer movement.",
                    "`-m`: Supplies custom commit message for the merge commit.",
                    "Merge Commit: Has two parent pointers (`Parent 1`: previous tip of main, `Parent 2`: tip of feature branch)."
                ],
                "flow": [
                    "Step 1: Check merge-base ancestor.",
                    "Step 2: Combine tree states into single merged tree.",
                    "Step 3: Create special commit object with two `parent` headers.",
                    "Step 4: Move `main` pointer to the new merge commit."
                ]
            }
        ],
        "challenge": {
            "prompt": "How many parent commit hashes does a standard merge commit have?",
            "opts": [
                "A) Zero parents (it is a root commit).",
                "B) Exactly 1 parent.",
                "C) At least 2 parents (one for each merged branch tip).",
                "D) Infinite parents."
            ],
            "correct_opt": "C",
            "hint": "A merge commit unites divergent branches, so it points back to both branch tips.",
            "praise": "Correct! Merge commits have 2 (or more in octopus merges) parent pointers.",
            "roast": "Merge commits connect two histories, meaning they must point backwards to 2 parents!"
        }
    },
    {
        "num": 7,
        "part": "B",
        "title": "Git Tags & Releases",
        "concept": "Tags are permanent, human-readable bookmarks pointing to specific commit SHAs. Unlike branches, tags never move when new commits are created.",
        "problem": "Create a lightweight tag using 'git tag v1.0', create an annotated tag with release notes using 'git tag -a v1.1 -m \"Release 1.1\"', inspect tag details with 'git show', and list all tags.",
        "commands": """# 1. Create lightweight tag
git tag v1.0

# 2. Create annotated tag with cryptographic metadata & message
git tag -a v1.1 -m "Release v1.1: Production verified build"

# 3. List all tags
git tag -l

# 4. Inspect annotated tag object
git show v1.1""",
        "blocks": [
            {
                "title": "Lightweight vs Annotated Tags",
                "code": "git tag v1.0\ngit tag -a v1.1 -m \"Release 1.1 with verified builds\"\ngit show v1.1",
                "purpose": "Labels release milestones in project history for production deployments and versioning.",
                "inside": [
                    "Lightweight Tag: Simply a file in `.git/refs/tags/` containing a commit SHA (no extra metadata).",
                    "Annotated Tag: Stored as a full object in `.git/objects/` with its own tagger name, email, date, message, and optional GPG signature.",
                    "`git show v1.1`: Dumps the annotated tag object followed by the commit it points to."
                ],
                "flow": [
                    "Step 1: Current HEAD commit identified.",
                    "Step 2: Annotated tag object created in object database.",
                    "Step 3: Reference pointer placed in `.git/refs/tags/v1.1`."
                ]
            }
        ],
        "challenge": {
            "prompt": "When you run 'git commit', what happens to existing tags?",
            "opts": [
                "A) Tags move automatically to the new commit.",
                "B) Tags are deleted.",
                "C) Tags stay frozen on the specific commit they were created on — they never move.",
                "D) Tags are renamed to v-next."
            ],
            "correct_opt": "C",
            "hint": "Branches are pointers that move on commit; tags are static bookmarks that never move.",
            "praise": "Precisely! Tags are immutable milestone pins in the project timeline.",
            "roast": "Incorrect! Branches move; tags remain permanently attached to their target commit."
        }
    },
    {
        "num": 8,
        "part": "B",
        "title": "Cherry-Picking Specific Commits",
        "concept": "Cherry-pick selects a specific commit from one branch and applies its exact changes as a brand new commit on your current branch, without merging the entire branch.",
        "problem": "Identify a critical bugfix commit on 'dev-branch', switch to 'main', and cherry-pick that isolated commit onto main using 'git cherry-pick <commit-sha>'.",
        "commands": """# 1. Locate bugfix commit on another branch
git log dev-branch --oneline -n 3

# 2. Switch to main
git checkout main

# 3. Apply isolated commit to main
git cherry-pick a1b2c3d

# 4. Or cherry-pick a range of commits:
# git cherry-pick start_commit^..end_commit""",
        "blocks": [
            {
                "title": "Isolated Commit Replay",
                "code": "git checkout main\ngit cherry-pick <commit-sha>",
                "purpose": "Transfers a single bugfix or feature commit across branches without pulling in unwanted work.",
                "inside": [
                    "`git cherry-pick`: Computes the diff introduced by `<commit-sha>` (by comparing it with its parent), and applies that diff onto the current HEAD.",
                    "Creates a brand new commit on `main` with its own unique SHA."
                ],
                "flow": [
                    "Step 1: Diff of `<commit-sha>` extracted (`commit` vs `commit~1`).",
                    "Step 2: Diff patched onto current HEAD.",
                    "Step 3: New commit recorded on `main` with identical commit message."
                ]
            }
        ],
        "challenge": {
            "prompt": "When would you prefer 'git cherry-pick' over 'git merge'?",
            "opts": [
                "A) When you want to combine every single commit from a branch.",
                "B) When you need only ONE specific hotfix commit from an unfinished experimental branch without bringing in the rest of the unstable code.",
                "C) When working without an internet connection.",
                "D) To delete commits."
            ],
            "correct_opt": "B",
            "hint": "Cherry-pick = surgical extraction of one specific commit.",
            "praise": "Exact! Cherry-picking allows surgical application of isolated hotfixes.",
            "roast": "Cherry-pick is used for surgical extraction of individual commits, not entire branches!"
        }
    },
    {
        "num": 9,
        "part": "B",
        "title": "Deep Commit Inspection (Show & Cat-File)",
        "concept": "Git is an object database. Every commit, tree, and blob can be inspected down to the byte level using porcelain commands ('git show') and plumbing commands ('git cat-file').",
        "problem": "Inspect the most recent commit metadata and diff with 'git show HEAD', inspect file content at a past commit with 'git show <sha>:filename', and examine object types with 'git cat-file -t'.",
        "commands": """# 1. Inspect latest commit details and diff
git show HEAD

# 2. Inspect a specific commit by hash
git show a1b2c3d

# 3. View a file's content at a past commit without checking it out
git show a1b2c3d:readme.txt

# 4. Plumbing: check object type and raw content
git cat-file -t a1b2c3d
git cat-file -p a1b2c3d""",
        "blocks": [
            {
                "title": "Inspecting Commits & File Historical Views",
                "code": "git show HEAD\ngit show HEAD~2:src/app.c",
                "purpose": "Enables instant inspection of commit authors, log messages, and unified diffs without switching branches.",
                "inside": [
                    "`git show HEAD`: Displays author, date, commit message, and full colored diff of all files modified in the commit.",
                    "`git show <sha>:<path>`: Directly reads the file blob from the Git object store at that point in history."
                ],
                "flow": [
                    "Step 1: HEAD reference resolved to commit SHA.",
                    "Step 2: Commit object parsed for metadata.",
                    "Step 3: Root Tree diffed against Parent Tree to generate diff display."
                ]
            }
        ],
        "challenge": {
            "prompt": "What Git command pretty-prints the raw contents of ANY object in the .git database?",
            "opts": [
                "A) git print-all",
                "B) git cat-file -p <object-sha>",
                "C) git view-database",
                "D) git unpack"
            ],
            "correct_opt": "B",
            "hint": "The '-p' flag stands for pretty-print in the core Git plumbing tools.",
            "praise": "Spot on! 'git cat-file -p' is the master plumbing inspection tool.",
            "roast": "The standard plumbing tool is 'git cat-file -p <sha>'!"
        }
    },
    {
        "num": 10,
        "part": "B",
        "title": "Filtering Commit History by Author, Date & Path",
        "concept": "Large codebases contain thousands of commits. Git provides powerful filtering flags to isolate work by author, time window, or specific modified files.",
        "problem": "Filter project commit log by author name using '--author', specify a calendar range using '--since' and '--until', and filter by file path using '-- <path>'.",
        "commands": """# 1. Filter by author name or email
git log --author="Prajwal" --oneline

# 2. Filter by date window
git log --since="2026-01-01" --until="2026-11-14" --oneline

# 3. Filter commits that touched a specific file
git log --oneline -- dsa-lab/programs/lab03_stack_operations.c

# 4. Search commit messages by keyword (grep)
git log --grep="bugfix" --oneline""",
        "blocks": [
            {
                "title": "Historical Querying & Filtering Flags",
                "code": "git log --author=\"Prajwal\" --since=\"2 weeks ago\" --stat",
                "purpose": "Enables rapid forensic analysis of commit history during code reviews, audits, and exams.",
                "inside": [
                    "`--author`: Regex filter matched against commit Author header.",
                    "`--since` / `--until`: Human-friendly dates ('yesterday', '2026-01-01', '3 weeks ago').",
                    "`--stat`: Appends file modification counts and line insertions/deletions."
                ],
                "flow": [
                    "Step 1: Traverse commit DAG backwards from HEAD.",
                    "Step 2: Apply filter predicates to commit headers.",
                    "Step 3: Format and render matching commit entries."
                ]
            }
        ],
        "challenge": {
            "prompt": "Which flag displays a visual ASCII branch topology graph in 'git log'?",
            "opts": [
                "A) --ascii-art",
                "B) --graph",
                "C) --branches-draw",
                "D) --tree-view"
            ],
            "correct_opt": "B",
            "hint": "Used in the famous alias 'git log --oneline --graph --decorate --all'.",
            "praise": "Correct! --graph draws ASCII branch merges directly in the console.",
            "roast": "The flag is '--graph'!"
        }
    },
    {
        "num": 11,
        "part": "B",
        "title": "Commit History Formatting & Formats",
        "concept": "Git logs can be formatted into custom compact strings, one-line representations, and decorated graphs showing where all branch pointers and tags currently rest.",
        "problem": "Display the last 5 commits using 'git log -n 5 --oneline', and inspect branch tips with 'git log --graph --oneline --decorate --all'.",
        "commands": """# 1. Display last 5 commits in compact one-line format
git log -n 5 --oneline

# 2. Display all branches with decoration tags and ASCII graph
git log --graph --oneline --decorate --all

# 3. Custom pretty format with commit hash, author, relative date
git log --pretty=format:"%h - %an, %ar : %s" -n 5""",
        "blocks": [
            {
                "title": "Compact Formatting & Decorate Tags",
                "code": "git log -n 5 --oneline\ngit log --graph --oneline --decorate --all",
                "purpose": "Provides clear, high-density visualization of repository history and branch pointers.",
                "inside": [
                    "`-n 5`: Limits traversal depth to 5 commits.",
                    "`--oneline`: Shorthand for `--pretty=oneline --abbrev-commit` (7-char SHA + subject).",
                    "`--decorate`: Prints ref names (HEAD -> main, tag: v1.0, origin/main) next to commits."
                ],
                "flow": [
                    "Step 1: Limit traversal counter to N.",
                    "Step 2: Abbreviate SHA to minimum unique hex characters.",
                    "Step 3: Attach color-coded ref badges."
                ]
            }
        ],
        "challenge": {
            "prompt": "What does 'git log --oneline' output for each commit?",
            "opts": [
                "A) The complete diff of every file.",
                "B) The 7-character abbreviated SHA hash and the first line of the commit message.",
                "C) Only the author's email address.",
                "D) The full 40-character SHA hash with timestamp."
            ],
            "correct_opt": "B",
            "hint": "7-character SHA prefix + commit summary.",
            "praise": "Spot on! Compact and readable.",
            "roast": "It outputs the 7-character abbreviated hash and the commit subject line!"
        }
    },
    {
        "num": 12,
        "part": "B",
        "title": "Undoing Changes Safely (Revert vs Reset)",
        "concept": "Git provides multiple strategies to undo mistakes. Revert is public and safe (creates an inverted patch commit); Reset is local and rewrites history (moves the branch pointer backwards).",
        "problem": "Safely undo a published commit using 'git revert <commit-sha>', and understand the difference between 'reset --soft', 'reset --mixed', and 'reset --hard'.",
        "commands": """# 1. Safely undo a published commit (creates new inverse commit)
git revert <commit-sha> --no-edit

# 2. Local undo: keep changes in Staging Area
git reset --soft HEAD~1

# 3. Local undo: keep changes in Working Directory (Default)
git reset --mixed HEAD~1

# 4. Local undo: DISCARD all changes (Dangerous!)
git reset --hard HEAD~1

# 5. Undo uncommitted edits in working directory
git restore <file>""",
        "blocks": [
            {
                "title": "Public Undo: git revert",
                "code": "git revert <commit-sha> --no-edit",
                "purpose": "Undoes the changes of a past commit without rewriting history, safe for shared/pushed branches.",
                "inside": [
                    "`git revert`: Inverts the patch of `<commit-sha>` (additions become deletions, deletions become additions) and records a new commit.",
                    "Because history is not rewritten, team members do not experience merge conflicts on pull."
                ],
                "flow": [
                    "Step 1: Calculate inverted diff of target commit.",
                    "Step 2: Apply inverse diff to working tree.",
                    "Step 3: Automatically commit with message 'Revert \"<original message>\"'."
                ]
            },
            {
                "title": "The 3 Modes of git reset",
                "code": "git reset --soft HEAD~1   # Index & Working Tree kept\ngit reset --mixed HEAD~1  # Working Tree kept, Index cleared\ngit reset --hard HEAD~1   # EVERYTHING WIPED OUT!",
                "purpose": "Moves the current branch HEAD backwards, used for local unpushed cleanups.",
                "inside": [
                    "`--soft`: Moves HEAD pointer back; all modified files remain in Staging Area (ready to re-commit).",
                    "`--mixed` (Default): Moves HEAD back; files are unstaged but kept in Working Directory.",
                    "`--hard`: Moves HEAD back and overwrites working tree with old state. Any uncommitted work is PERMANENTLY lost!"
                ],
                "flow": [
                    "Step 1: Target commit resolved (`HEAD~1`).",
                    "Step 2: Current branch pointer updated to target.",
                    "Step 3: Staging area and working directory adjusted according to flag."
                ]
            }
        ],
        "challenge": {
            "prompt": "You already pushed a commit to the remote GitHub team repo. Which command MUST you use to undo it safely without breaking teammates' clones?",
            "opts": [
                "A) git reset --hard HEAD~1 && git push --force",
                "B) git revert <commit-id>",
                "C) git clean -fd",
                "D) rm -rf .git"
            ],
            "correct_opt": "B",
            "hint": "Revert appends a new commit that cancels the bug; it does NOT rewrite shared history.",
            "praise": "Golden rule of Git! Never force-push history rewrites on shared branches; always use revert.",
            "roast": "On shared branches, always use 'git revert' to avoid breaking everyone else's repository!"
        }
    }
]


# ==============================================================================
# CATEGORIZED GIT COMMAND LIBRARY (Basic & Advanced)
# ==============================================================================

GIT_COMMAND_LIBRARY = {
    "basic": [
        {
            "cmd": "git init",
            "syntax": "git init [directory]",
            "summary": "Initializes a brand new, empty Git repository in the specified directory.",
            "explanation": "Creates the hidden `.git/` directory containing the internal object database, ref stores, and configuration files. Without this folder, version control does not exist.",
            "exam_tip": "Common viva question: What is inside .git? Answer: objects (blobs, trees, commits, tags), refs (heads, tags, remotes), HEAD file, config, and index."
        },
        {
            "cmd": "git status",
            "syntax": "git status [-s]",
            "summary": "Displays the working tree status comparing Working Directory, Index, and HEAD.",
            "explanation": "Shows tracked, modified, and untracked files. Files in red are modified but unstaged; files in green are staged in the Index ready to be committed.",
            "exam_tip": "Short status flag `-s` outputs `M` (modified), `A` (added), `??` (untracked) in column format."
        },
        {
            "cmd": "git add",
            "syntax": "git add <pathspec>  |  git add .",
            "summary": "Stages file modifications into the Index, preparing them for the next commit.",
            "explanation": "Calculates the SHA-1/SHA-256 hash of file contents, writes a new Blob object into `.git/objects/`, and records the path and hash in `.git/index`.",
            "exam_tip": "Does `git add` create Git objects immediately? YES! It creates Blob objects in the database even before you commit."
        },
        {
            "cmd": "git commit",
            "syntax": "git commit -m \"<message>\"  |  git commit -am \"<message>\"",
            "summary": "Records a permanent, immutable snapshot of the staged files in project history.",
            "explanation": "Generates a Tree object representing directory layout, creates a Commit object linking author, timestamp, parent commit SHA, and tree, and advances the current branch pointer.",
            "exam_tip": "Commits are immutable. You cannot edit a past commit — you can only create a new commit or rewrite history with new SHAs."
        },
        {
            "cmd": "git branch",
            "syntax": "git branch [-a] [-d <name>] [<new-branch>]",
            "summary": "Lists, creates, or deletes branch reference pointers.",
            "explanation": "A Git branch is simply a 41-byte text file inside `.git/refs/heads/` storing the 40-character commit SHA of the branch tip. Creating a branch takes O(1) time and 0 extra disk space.",
            "exam_tip": "Viva question: Why is Git branching so much faster than SVN? In SVN, branching copies all files; in Git, branching just creates a 41-byte text file pointer."
        },
        {
            "cmd": "git switch / checkout",
            "syntax": "git switch <branch>  |  git switch -c <new-branch>",
            "summary": "Switches branches or restores working tree files.",
            "explanation": "Updates the `HEAD` reference to point to the desired branch and updates files in the working directory to match the commit recorded at the branch tip.",
            "exam_tip": "Git 2.23 introduced `git switch` (for branches) and `git restore` (for files) to separate the overloaded roles of `git checkout`."
        },
        {
            "cmd": "git log",
            "syntax": "git log [--oneline] [--graph] [--decorate]",
            "summary": "Displays the commit history starting backwards from HEAD.",
            "explanation": "Walks the Directed Acyclic Graph (DAG) backwards following parent commit pointers, outputting commit SHAs, authors, dates, and log messages.",
            "exam_tip": "Know the universal visualization command: `git log --oneline --graph --decorate --all`."
        },
        {
            "cmd": "git merge",
            "syntax": "git merge [--no-ff] <branch>",
            "summary": "Joins two or more development histories together.",
            "explanation": "Performs either a Fast-Forward (pointer advance) if history is linear, or a 3-way merge using common ancestor commit to create a merge commit with 2 parents.",
            "exam_tip": "If conflicting changes exist in the same line of a file, Git halts the merge and inserts conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)."
        }
    ],
    "advanced": [
        {
            "cmd": "git rebase",
            "syntax": "git rebase [-i] <upstream>",
            "summary": "Re-applies commits on top of another base tip to achieve a completely linear history.",
            "explanation": "Saves your branch commits as temporary patches, resets the branch pointer to the upstream target, and replays each patch sequentially with new parent SHAs.",
            "exam_tip": "Golden Rule of Rebase: NEVER rebase commits that have already been pushed to a public/shared repository, as it rewrites SHA hashes."
        },
        {
            "cmd": "git cherry-pick",
            "syntax": "git cherry-pick <commit-sha> [start^..end]",
            "summary": "Applies the changes introduced by some existing commits onto the current branch.",
            "explanation": "Extracts the exact diff of `<commit-sha>` compared to its parent, and commits that diff directly onto the current HEAD with a new SHA.",
            "exam_tip": "Ideal for backporting a single bugfix from a development branch into production without bringing along incomplete features."
        },
        {
            "cmd": "git stash",
            "syntax": "git stash [push -m \"msg\"]  |  git stash list  |  git stash pop",
            "summary": "Stashes the changes in a dirty working directory away onto a temporary stack.",
            "explanation": "Creates special commit objects in `.git/refs/stash` capturing working tree and index diffs, and resets the working tree to HEAD.",
            "exam_tip": "`stash pop` applies the stash and removes it from the stash stack. `stash apply` applies the stash but keeps it in the stack."
        },
        {
            "cmd": "git reset",
            "syntax": "git reset [--soft | --mixed | --hard] <commit>",
            "summary": "Resets current HEAD to the specified state.",
            "explanation": "--soft moves HEAD pointer only; --mixed (default) moves HEAD and updates Index; --hard moves HEAD, updates Index, AND overwrites Working Directory.",
            "exam_tip": "Viva trap: 'Can git reset --hard delete uncommitted work permanently?' YES. If changes were never committed or stashed, they cannot be recovered."
        },
        {
            "cmd": "git revert",
            "syntax": "git revert <commit-sha> [--no-edit]",
            "summary": "Records a new commit that reverses the effects of an earlier commit.",
            "explanation": "Computes the exact inverse diff of the target commit and records it as a new forward-moving commit, preserving history integrity for shared branches.",
            "exam_tip": "Always use `revert` instead of `reset` when undoing changes already pushed to GitHub."
        },
        {
            "cmd": "git reflog",
            "syntax": "git reflog [show] [<ref>]",
            "summary": "Manages reflog information, recording every position HEAD has ever occupied locally.",
            "explanation": "Git's safety net: even if you run `git reset --hard` or delete a branch, the lost commit SHAs remain recorded in `.git/logs/HEAD` for up to 90 days before garbage collection.",
            "exam_tip": "To rescue a lost commit after accidental hard reset: run `git reflog`, identify the SHA before the reset, and run `git reset --hard HEAD@{1}`."
        },
        {
            "cmd": "git cat-file",
            "syntax": "git cat-file (-t | -p | -s) <object-sha>",
            "summary": "Plumbing command to inspect object type (-t), content (-p), or size (-s).",
            "explanation": "Allows direct examination of raw compressed zlib objects inside `.git/objects/`. Confirms Git's 4 core types: blob, tree, commit, tag.",
            "exam_tip": "Plumbing vs Porcelain: Porcelain commands (add, commit, status) are for users; Plumbing commands (cat-file, hash-object, write-tree) are low-level tools."
        }
    ]
}


# ==============================================================================
# SOCRATIC VIVA HUB (1BCSL307A)
# ==============================================================================

GIT_VIVA_BANK = [
    {
        "q": "What is the fundamental architectural difference between Git and centralized VCS like SVN?",
        "options": [
            "A) SVN requires internet connection only on Fridays.",
            "B) Centralized VCS stores full history on a single central server; Git is distributed, meaning every cloned copy contains the COMPLETE project history and database locally.",
            "C) Git only works with Python programs.",
            "D) SVN uses SHA hashing while Git uses MD5."
        ],
        "ans": "B",
        "tip": "Think about what happens if your network goes down: with Git, you can still commit, branch, view logs, and diff offline.",
        "praise": "Precisely! Distributed means full autonomous offline capability with complete repository history on every developer machine.",
        "roast": "Remember: In Git (distributed), every clone is a full repository backup with complete history, unlike centralized VCS where history lives only on the central server."
    },
    {
        "q": "What exactly is stored inside a Git 'Blob' object?",
        "options": [
            "A) Filename, directory permissions, and file content.",
            "B) ONLY raw compressed file content — filenames and directory structures are stored in Tree objects, not in Blobs.",
            "C) Commit messages and author emails.",
            "D) Branch pointers."
        ],
        "ans": "B",
        "tip": "Blobs are content-addressable by their data alone. Two identical files with different names share the exact same Blob in Git!",
        "praise": "Examiner favorite! Blobs hold ONLY file bytes. File names and permissions belong to Trees.",
        "roast": "Careful! A common viva trap: Blobs store ONLY file content. File names, modes, and folder structures are stored in Tree objects!"
    },
    {
        "q": "What is the meaning of a 'Detached HEAD' state in Git?",
        "options": [
            "A) The computer screen disconnected from the CPU.",
            "B) HEAD points directly to a specific commit SHA rather than to a branch reference.",
            "C) The .git folder was accidentally deleted.",
            "D) You pushed code without commit privileges."
        ],
        "ans": "B",
        "tip": "Normally HEAD points to a branch ref (like refs/heads/main). In detached HEAD, HEAD points directly to a raw commit hash.",
        "praise": "Spot on! Detached HEAD is harmless for inspecting history, but new commits won't belong to any branch unless you create one.",
        "roast": "Detached HEAD simply means HEAD points directly to a commit hash instead of a branch pointer name."
    },
    {
        "q": "What is the difference between 'git fetch' and 'git pull'?",
        "options": [
            "A) They are identical synonyms.",
            "B) 'git fetch' downloads remote objects and updates remote tracking branches without touching local files; 'git pull' executes 'git fetch' followed immediately by 'git merge'.",
            "C) git fetch works on GitHub; git pull works only on GitLab.",
            "D) git pull never causes merge conflicts."
        ],
        "ans": "B",
        "tip": "git fetch is safe and non-intrusive. git pull modifies your active working files by merging downloaded commits.",
        "praise": "Mastered! Understanding fetch vs pull prevents unexpected merge conflicts during code pulls.",
        "roast": "Remember: `git pull = git fetch + git merge`. Fetch downloads; pull downloads AND merges."
    },
    {
        "q": "How does Git calculate the 40-character hexadecimal SHA identifier for a commit?",
        "options": [
            "A) It generates a random UUID.",
            "B) It hashes the file sizes added together.",
            "C) It cryptographically hashes the commit header, tree SHA, parent commit SHA(s), author name/timestamp, committer name/timestamp, and commit message.",
            "D) It takes the current Unix time multiplied by 100."
        ],
        "ans": "C",
        "tip": "Git is a Merkle DAG. Every single attribute of the commit, including its parent pointer, is part of the hash computation.",
        "praise": "Pure computer science elegance! This cryptographic linkage makes Git history immutable and tamper-evident.",
        "roast": "Git SHA hashes are generated by cryptographically hashing the commit tree, parent SHA, author, timestamp, and message."
    },
    {
        "q": "What is the purpose of the 'git reflog' command?",
        "options": [
            "A) To submit a bug report to the Git development team.",
            "B) To view a local chronological log of every change to the HEAD pointer, allowing recovery of deleted commits and branches.",
            "C) To format Python code according to PEP 8.",
            "D) To print network connection speeds."
        ],
        "ans": "B",
        "tip": "Reflog is your local safety net. Even if a commit is lost after a hard reset, its SHA remains in reflog.",
        "praise": "Exam lifesaver! Reflog allows you to recover from almost any catastrophic git command.",
        "roast": "Reflog is Git's ultimate undo mechanism, recording every movement of HEAD on your local machine."
    }
]


# ==============================================================================
# DISASTER RECOVERY SCENARIOS (Exam Emergencies)
# ==============================================================================

GIT_DISASTERS = [
    {
        "title": "🚨 DISASTER 1: The Accidental 'git reset --hard' Panic",
        "story": "You had 3 critical commits with your exam code. You accidentally ran 'git reset --hard HEAD~3'.\nAll your commits vanished from 'git log' and your files disappeared from the folder! The examiner walks over in 2 minutes.",
        "prompt": "How do you instantly restore the lost commits?",
        "choices": [
            "Run 'git reflog' to find the SHA before the reset, then run 'git reset --hard HEAD@{1}' (or the specific SHA)!",
            "Re-type the entire program from memory.",
            "Delete the repository and re-clone.",
            "Restart your laptop."
        ],
        "ans_idx": 1,
        "reaction": "REFLOG SAVES THE DAY! Git does not immediately garbage-collect commits. Reflog records the exact commit hash before the reset."
    },
    {
        "title": "🚨 DISASTER 2: The Merge Conflict Marker Crash",
        "story": "You ran 'git merge feature-branch' and Git reported:\n  CONFLICT (content): Merge conflict in main.c\nWithout thinking, you tried to run 'gcc main.c -o main', and GCC spat out 50 syntax errors on '<<<<<<< HEAD'!",
        "prompt": "What must you do to fix the file before compiling?",
        "choices": [
            "Open main.c, locate conflict markers (<<<<<<<, =======, >>>>>>>), decide which code to keep, delete the marker lines, stage with 'git add main.c', and commit!",
            "Run 'git kill --force'.",
            "Ignore the file and rename it to main.cpp.",
            "Comment out the whole file."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY! Conflict markers are inserted into your source code by Git. You must manually resolve the differences and remove the markers."
    },
    {
        "title": "🚨 DISASTER 3: The Secret API Key Committed to History",
        "story": "You committed a file containing your private cloud API key. You made another commit on top of it. Now you must push to public GitHub, but the secret is in history!",
        "prompt": "Why is simply editing the file and committing 'removed API key' insufficient?",
        "choices": [
            "Because Git stores the full snapshot of past commits! Anyone can run 'git show' on the earlier commit and read the secret key.",
            "GitHub automatically rotates passwords.",
            "Git deletes old commits automatically.",
            "The compiler warns about API keys."
        ],
        "ans_idx": 1,
        "reaction": "BINGO! Version control remembers every past version forever. To remove secrets, you must revoke the key and rewrite history (or use tools like git-filter-repo)."
    }
]


# ==============================================================================
# EXPERIMENT RUNNER & PRESENTATION LOGIC
# ==============================================================================

def run_git_experiment_lab(exp):
    clear_screen()
    _show_session_header(subject="git")
    print(Color.CYAN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  🐙 GIT LAB EXPERIMENT {exp['num']:02d} ({exp['part']}): {exp['title']:<48} ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET)

    # Stage 1: Big Picture & Mental Model
    print(f"\n{Color.YELLOW}{Color.BOLD}[Stage 1/4] 💡 THE BIG PICTURE & MENTAL MODEL:{Color.RESET}\n")
    print_slow(f"  {exp['concept']}\n", 0.008, Color.WHITE)
    print(f"{Color.CYAN}{Color.BOLD}🎯 VTU Lab Syllabus Requirement:{Color.RESET}")
    print(f"  {exp['problem']}\n")
    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the exact Git commands...{Color.RESET}")

    # Stage 2: Verified Command Script
    clear_screen()
    print(Color.GREEN + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print(f"║  📄 [Stage 2/4] VERIFIED COMMAND SCRIPT — EXPERIMENT {exp['num']:02d}                    ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET + "\n")
    for line in exp["commands"].splitlines():
        if line.startswith("#"):
            print(f"  {Color.YELLOW}{line}{Color.RESET}")
        else:
            print(f"  {Color.GREEN}{Color.BOLD}$ {line}{Color.RESET}")
    print("\n" + Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter to inspect the 3-Part Block Logic Breakdown...{Color.RESET}")

    # Stage 3: Structured 3-Part Block Breakdown
    clear_screen()
    print(Color.MAGENTA + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🔍 [Stage 3/4] 3-PART STRUCTURED BLOCK LOGIC BREAKDOWN                      ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET + "\n")

    for idx, b in enumerate(exp["blocks"], 1):
        print(f"  {Color.YELLOW}{Color.BOLD}🧱 Block {idx}: {b['title']}{Color.RESET}")
        print("  " + Color.DIM + ("─" * 72) + Color.RESET)
        for l in b["code"].splitlines():
            print(f"    {Color.WHITE}{Color.BOLD}{l}{Color.RESET}")
        print("  " + Color.DIM + ("─" * 72) + Color.RESET)

        # 1. Purpose & Role
        print(f"  {Color.GREEN}{Color.BOLD}1. 🎯 Purpose & Role:{Color.RESET}")
        print(f"     {b['purpose']}\n")

        # 2. Inside the Block
        print(f"  {Color.CYAN}{Color.BOLD}2. 🔍 Inside the Block (Components & State Changes):{Color.RESET}")
        for item in b["inside"]:
            print(f"     • {item}")
        print()

        # 3. Execution Flow
        print(f"  {Color.YELLOW}{Color.BOLD}3. ⚙️ Step-by-Step Execution Flow:{Color.RESET}")
        for step in b["flow"]:
            print(f"     ↳ {step}")
        print()

        if idx < len(exp["blocks"]):
            prompt_input(f"  {Color.DIM}Press Enter for Block {idx+1}...{Color.RESET}\n")

    print(Color.DIM + ("─" * 80) + Color.RESET)
    prompt_input(f"{Color.GREEN}{Color.BOLD}👉 Press Enter for the Quick Understanding Challenge...{Color.RESET}")

    # Stage 4: Understanding Challenge
    clear_screen()
    ch = exp["challenge"]
    print(Color.YELLOW + Color.BOLD + "╔" + ("═" * 78) + "╗")
    print("║  🎮 [Stage 4/4] GUIDED UNDERSTANDING CHALLENGE                               ║")
    print("╚" + ("═" * 78) + "╝" + Color.RESET + "\n")
    print(f"{Color.BOLD}{Color.WHITE}{ch['prompt']}{Color.RESET}\n")

    for opt in ch["opts"]:
        print(f"  {Color.CYAN}{opt}{Color.RESET}")
    print()

    while True:
        ans = prompt_input(f"{Color.BOLD}Your Answer [A/B/C/D] (or 'H' for Hint): {Color.RESET}").strip().upper()
        if ans == "H":
            print(f"\n  {Color.YELLOW}💡 HINT: {ch['hint']}{Color.RESET}\n")
            continue
        if ans in ("A", "B", "C", "D"):
            break
        print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")

    if ans == ch["correct_opt"]:
        anim_correct()
        _record_concept_mastered("Git MCQ")
        print(f"\n{Color.GREEN}{Color.BOLD}✔ {ch['praise']}{Color.RESET}\n")
    else:
        anim_wrong()
        print(f"\n{Color.RED}{Color.BOLD}❌ {ch['roast']}{Color.RESET}")
        print(f"   {Color.YELLOW}Expected ({ch['correct_opt']}): {ch['hint']}{Color.RESET}\n")

    exp_id = f"GIT-{exp['num']}"
    if exp_id not in _SESSION["experiments_done"]:
        _SESSION["experiments_done"].append(exp_id)
        _save_to_local_db()

    prompt_input("Press Enter to return to Git Lab Studio...")


def mode_git_command_library():
    """Browse Basic vs Advanced Git commands with syntax, purpose, and exam tips."""
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   📚 GIT COMMAND LIBRARY — Categorized Command Reference & Syntax Guide       ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 📗  {Color.BOLD}Basic Everyday Commands{Color.RESET}   (init, status, add, commit, branch, checkout, log, merge)")
        print(f"  {Color.GREEN}[2]{Color.RESET} 🚀  {Color.BOLD}Advanced & Plumbing Tools{Color.RESET} (rebase, cherry-pick, stash, reset, revert, reflog, cat-file)")
        print(f"\n  {Color.DIM}[0]   ⬅️  Back to Git Lab Studio{Color.RESET}\n")

        ch = prompt_input(f"{Color.BOLD}Choose Category [1, 2, 0=Back]: {Color.RESET}").strip()
        if ch in ("0", "B", "BACK", "EXIT"):
            return
        elif ch in ("1", "2"):
            cat_key = "basic" if ch == "1" else "advanced"
            cat_name = "BASIC COMMANDS" if ch == "1" else "ADVANCED COMMANDS"
            cmd_list = GIT_COMMAND_LIBRARY[cat_key]

            while True:
                clear_screen()
                print(f"\n{Color.CYAN}{Color.BOLD}─── {cat_name} ({len(cmd_list)} Commands) ───{Color.RESET}\n")
                for i, item in enumerate(cmd_list, 1):
                    print(f"  {Color.YELLOW}[{i}]{Color.RESET} {Color.BOLD}{item['cmd']:<18}{Color.RESET} — {item['summary']}")
                print(f"\n  {Color.DIM}[0] ⬅️  Back to Categories{Color.RESET}\n")

                pick = prompt_input(f"{Color.BOLD}Select command [1 - {len(cmd_list)}, 0=Back]: {Color.RESET}").strip()
                if pick in ("0", "B", "BACK"):
                    break
                if pick.isdigit() and 1 <= int(pick) <= len(cmd_list):
                    cmd_obj = cmd_list[int(pick) - 1]
                    clear_screen()
                    print(f"\n{Color.GREEN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
                    print(f"║  📖 COMMAND: {cmd_obj['cmd']:<63} ║")
                    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
                    print(f"  {Color.YELLOW}{Color.BOLD}Syntax:{Color.RESET}       {Color.WHITE}{cmd_obj['syntax']}{Color.RESET}\n")
                    print(f"  {Color.CYAN}{Color.BOLD}Purpose:{Color.RESET}      {cmd_obj['summary']}\n")
                    print(f"  {Color.MAGENTA}{Color.BOLD}Explanation:{Color.RESET}  {cmd_obj['explanation']}\n")
                    print(f"  {Color.YELLOW}{Color.BOLD}💡 Exam Tip:{Color.RESET}   {cmd_obj['exam_tip']}\n")
                    prompt_input("Press Enter to return to list...")


def mode_git_viva():
    """Socratic Viva Gauntlet for Git Lab 1BCSL307A."""
    clear_screen()
    print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   🎓 GIT LAB SOCRATIC VIVA GAUNTLET (1BCSL307A — VTU Exam Drills)            ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
    print("  Practice examiner questions with Socratic hints and conceptual breakdowns.\n")

    score = 0
    questions = list(GIT_VIVA_BANK)
    random.shuffle(questions)

    for idx, q in enumerate(questions, 1):
        print(f"\n{Color.CYAN}{Color.BOLD}[Question {idx}/{len(questions)}]{Color.RESET}")
        print(f"{Color.BOLD}{q['q']}{Color.RESET}\n")
        for opt in q["options"]:
            print(f"  {opt}")

        attempt = 1
        solved = False
        while attempt <= 2 and not solved:
            prompt_str = "\nYour Answer [A / B / C / D] (or 'H' for Clue, 0 to Exit): " if attempt == 1 else "\nSecond Try [A / B / C / D]: "
            ans = prompt_input(prompt_str).strip().upper()

            if ans in ("0", "EXIT", "Q"):
                return
            if ans == "H":
                print(f"  {Color.YELLOW}💡 Clue: {q['tip']}{Color.RESET}")
                continue
            if ans not in ("A", "B", "C", "D"):
                print(f"{Color.RED}Please type A, B, C, or D!{Color.RESET}")
                continue

            if ans == q["ans"]:
                solved = True
                anim_correct()
                _record_concept_mastered("Git Viva")
                score += 1
                print(f"\n  {Color.GREEN}{Color.BOLD}✔ {q['praise']}{Color.RESET}")
            else:
                anim_wrong()
                if attempt == 1:
                    print(f"\n  {Color.YELLOW}🌱 {q['roast']}{Color.RESET}")
                    print(f"  {Color.YELLOW}💡 Clue: {q['tip']}{Color.RESET}")
                    attempt += 1
                else:
                    print(f"\n  {Color.MAGENTA}The correct answer is [{q['ans']}].{Color.RESET}")
                    attempt += 1

        print(f"\n  {Color.CYAN}💡 Examiner Expectation: {q['tip']}{Color.RESET}")
        prompt_input(f"\n{Color.DIM}Press Enter for next question...{Color.RESET}")

    print(f"\n{Color.CYAN}===================================================={Color.RESET}")
    print(f"  🎉 Git Viva Practice Complete! Mastered: {Color.BOLD}{score}/{len(questions)} Concepts{Color.RESET}")
    print(f"{Color.CYAN}===================================================={Color.RESET}\n")
    prompt_input("Press Enter to return...")


def mode_git_disaster():
    """Real-World Git Exam Emergency Scenarios."""
    clear_screen()
    print(f"\n{Color.RED}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║   🚨 GIT LAB DISASTER RECOVERY (3 Real Exam Emergencies)                     ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

    for idx, sc in enumerate(GIT_DISASTERS, 1):
        print(f"\n{Color.YELLOW}{Color.BOLD}{sc['title']}{Color.RESET}")
        print(f"{Color.WHITE}{sc['story']}{Color.RESET}\n")
        print(f"{Color.CYAN}{sc['prompt']}{Color.RESET}\n")
        for i, ch in enumerate(sc["choices"], 1):
            print(f"  [{i}] {ch}")

        while True:
            ans = prompt_input("\nYour Choice [1-4, 0=Exit]: ").strip()
            if ans == "0":
                return
            if ans.isdigit() and 1 <= int(ans) <= len(sc["choices"]):
                val = int(ans)
                if val == sc["ans_idx"]:
                    anim_correct()
                    print(f"\n{Color.GREEN}{Color.BOLD}✔ {sc['reaction']}{Color.RESET}\n")
                else:
                    anim_wrong()
                    print(f"\n{Color.RED}❌ That makes the disaster worse! Correct: Option [{sc['ans_idx']}]{Color.RESET}\n")
                    print(f"   {Color.YELLOW}{sc['reaction']}{Color.RESET}\n")
                prompt_input("Press Enter for next emergency...")
                break


def mode_git_studio():
    """Master Git Lab Studio Menu (1BCSL307A)."""
    while True:
        clear_screen()
        print(f"\n{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        print("  🐙 GIT LAB STUDIO: 1BCSL307A (VTU 2025 Scheme — 12 Experiments)")
        print(f"{Color.GREEN}{Color.BOLD}{'='*80}{Color.RESET}")
        _show_session_header(subject="git")

        print(f"  {Color.YELLOW}[CL]{Color.RESET} 📚  {Color.BOLD}Categorized Command Library{Color.RESET}  (Basic & Advanced Reference)")
        print(f"  {Color.GREEN}[SB]{Color.RESET} 🧪  {Color.BOLD}Interactive Command Sandbox{Color.RESET}  (Test Commands & Safety Check)")
        print(f"  {Color.RED}[DR]{Color.RESET} 🚨  {Color.BOLD}Disaster Recovery Scenarios{Color.RESET}  (Reflog, Conflict Resolution)")
        print(f"  {Color.MAGENTA}[VG]{Color.RESET} 🎓  {Color.BOLD}Socratic Viva Practice Hub{Color.RESET}   (Examiner Questions & Traps)")
        print(f"{Color.CYAN}{'─'*78}{Color.RESET}")

        print(f"  {Color.BOLD}PART A: CORE REPOSITORY & BRANCHING EXPERIMENTS{Color.RESET}")
        for i in range(6):
            exp = GIT_EXPERIMENTS[i]
            done = "✅" if f"GIT-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.BOLD}PART B: ADVANCED WORKFLOWS, TAGS & RECOVERY EXPERIMENTS{Color.RESET}")
        for i in range(6, 12):
            exp = GIT_EXPERIMENTS[i]
            done = "✅" if f"GIT-{exp['num']}" in _SESSION["experiments_done"] else "  "
            print(f"  {done} {Color.CYAN}[{exp['num']:02d}]{Color.RESET} {exp['title']}")

        print(f"\n  {Color.DIM}[0]  ⬅️  Back to Master OILS-3 Hub{Color.RESET}\n")

        choice = prompt_input(f"{Color.BOLD}Select [01 - 12, CL, SB, DR, VG, 0]: {Color.RESET}").strip().upper()

        if choice in ("0", "B", "EXIT"):
            break
        elif choice == "CL":
            mode_git_command_library()
        elif choice == "SB":
            mode_git_command_sandbox()
        elif choice == "DR":
            mode_git_disaster()
        elif choice == "VG":
            mode_git_viva()
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= 12:
                run_git_experiment_lab(GIT_EXPERIMENTS[val - 1])
            else:
                print(f"{Color.RED}Invalid experiment number!{Color.RESET}")
                time.sleep(0.6)
        else:
            time.sleep(0.3)
