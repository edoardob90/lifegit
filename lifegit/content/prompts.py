"""Instructions, hints, and prompts for exercises"""

ACT1_PROMPTS = {
    "instructions": """Create a file called 'decision.txt' and write your decision inside.

What did you choose? University? Work? Travel? Something else entirely?
Write it down. Be specific. This is your decision to make.

Then commit it to history:

    git add decision.txt
    git commit -m "My first decision"

(Feel free to write your own commit message—make it meaningful to you.)""",
    "hints": [
        "First, create the file: touch decision.txt (or use your editor)",
        "Write your decision inside the file",
        "Stage it: git add decision.txt",
        "Commit it: git commit -m 'your message here'",
        "Use 'git status' to see where you are in the process",
    ],
    "file_name": "decision.txt",
}

ACT2_PROMPTS = {
    "instructions": """Think of a path you didn't take. A "what if?" that still crosses your mind.

Create a branch for that alternate timeline:

    git branch what-if-<your-alternate-path>
    git checkout what-if-<your-alternate-path>

For example:
  - git branch what-if-travel
  - git branch what-if-startup
  - git branch what-if-stayed-home

Then, on that branch, create a file describing what that life might look like.
Commit it to that branch.

Finally, switch back to your main branch:

    git checkout main

Your alternate timeline exists now, but you're back on your actual path.""",
    "hints": [
        "Create a branch: git branch what-if-something",
        "Switch to it: git checkout what-if-something (or: git switch what-if-something)",
        "Create a file describing that alternate life",
        "Commit it: git add <file> && git commit -m 'message'",
        "Return to main: git checkout main",
        "See your branches: git branch",
    ],
    "branch_prefix": "what-if-",
}
