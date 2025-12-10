# Life.git
### Learn Git Through Life Decisions

An interactive terminal-based tutorial that teaches git by framing operations as life decisions, inspired by [Derek Sivers' philosophy on commitment](https://sive.rs/htl02) and the parallel between `git commit` and making irreversible life choices.

From Sivers:

> To go one direction means you're not going other directions.
> When we commit, we cut off options and gain clarity.

Git mirrors this beautifully:

- Uncommitted changes = option paralysis (anxiety)
- `git commit` = making the decision (relief, clarity)
- `git branch` = exploring alternatives safely
- `git merge` = integrating different paths
- `git revert` = acknowledging mistakes while moving forward
- `git rebase` = reframing your narrative
- `git reflog` = your lived memory
- `git gc` = forgetting/letting go

## Flow

### Setup

```bash
# Student receives starter instructions
git clone <tutorial-repo-url>
cd lifegit

# Install with uv
uv sync

# Start tutorial
uv run lifegit start
```

### Gameplay

TODO

## Technical Architecture

### Stack

```toml
[project]
name = "lifegit"
version = "0.1.0"
description = "Learn git through life decisions"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "gitpython>=3.1.45",
    "rich>=14.2.0",
    "typer>=0.20.0",
]

[project.scripts]
lifegit = "lifegit.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Packages:

- **GitPython:** Mature, stable, mirrors git CLI (maintenance mode acceptable for educational use)
- **Typer:** Beautiful CLI with minimal code, great help system
- **Rich:** Gorgeous terminal output (panels, markdown, syntax highlighting, progress)
- **uv:** Fast dependency management for students

### Project Structure

```
lifegit/
├── pyproject.toml
├── README.md
├── uv.lock
├── lifegit/
│   ├── __init__.py
│   ├── cli.py               # Typer app entry point
│   ├── git_wrapper.py       # LifeRepo abstraction
│   ├── validator.py         # Exercise validation logic
│   ├── stages/
│   │   ├── __init__.py
│   │   ├── base.py          # BaseStage abstract class
│   │   ├── act1.py          # The First Decision
│   │   ├── act2.py          # What If?
│   │   ├── act3.py          # Integration
│   │   ├── act4.py          # Conflict
│   │   └── act5.py          # Rewriting History
│   └── content/
│       ├── __init__.py
│       ├── narratives.py    # Story text for each act
│       └── prompts.py       # Student prompts and hints
├── tests/
│   ├── test_git_wrapper.py
│   ├── test_validator.py
│   └── test_stages.py
└── examples/
    └── sample_life_repo/        # Example completed repo for reference
```
