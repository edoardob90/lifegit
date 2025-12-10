# Life.git - Learn Git Through Life Decisions

## Project Philosophy

**Core Concept:** An interactive terminal-based tutorial that teaches git by framing operations as life decisions, inspired by Derek Sivers' philosophy on commitment and the parallel between `git commit` and making irreversible life choices.

**Key Insight:** Git's irreversibility (commits are permanent in history) mirrors life decisions—the *act* of deciding is irreversible, even when the outcome can be changed. This emotional weight makes git operations meaningful rather than arbitrary, helping students understand *why* git works the way it does, not just *how*.

**Target Audience:** Programming beginners learning git fundamentals, but broadly applicable to anyone learning version control.

## Educational Approach

### The Derek Sivers Parallel

From Sivers: "To go one direction means you're not going other directions." When we commit, we cut off options and gain clarity.

**Git mirrors this:**
- Uncommitted changes = option paralysis (anxiety)
- `git commit` = making the decision (relief, clarity)
- `git branch` = exploring alternatives safely
- `git merge` = integrating different paths
- `git revert` = acknowledging mistakes while moving forward
- `git rebase` = reframing your narrative
- `git reflog` = your actual lived memory
- `git gc` = genuine forgetting/letting go

### Narrative Structure: Five Acts

Each act introduces git concepts through life stages with appropriate emotional weight and complexity.

#### **Act 1: The First Decision** (Commits & Working Directory)
**Life Stage:** Age 18—leaving home, first major decision  
**Git Concepts:** `git init`, `git add`, `git commit`, `git status`, `git log`  
**Theme:** The relief of committing vs. the anxiety of uncommitted changes  
**Exercise:** Create decision.txt, commit first major life choice  
**Learning Goal:** Understand that commits create clarity and forward momentum

#### **Act 2: What If?** (Branching)
**Life Stage:** Mid-20s—exploring alternatives without losing your main path  
**Git Concepts:** `git branch`, `git checkout`/`git switch`, parallel timelines  
**Theme:** Safe exploration before commitment  
**Exercise:** Create branches for "what if I'd chosen differently?"  
**Learning Goal:** Branches let you explore without destroying your main narrative

#### **Act 3: Integration** (Merging)
**Life Stage:** Late 20s—bringing different life aspects together  
**Git Concepts:** `git merge`, fast-forward vs. three-way merge  
**Theme:** Career + family + hobbies must coexist  
**Exercise:** Merge career branch with personal-life branch  
**Learning Goal:** Integration creates a richer story than a single linear path

#### **Act 4: Conflict** (Merge Conflicts)
**Life Stage:** 30s—when values clash and require active resolution  
**Git Concepts:** Merge conflicts, conflict markers, resolution strategies  
**Theme:** Some life paths are incompatible; you must choose  
**Exercise:** Resolve conflicts between work-abroad and family-local branches  
**Learning Goal:** Conflicts aren't failures—they're opportunities for conscious choice

#### **Act 5: Rewriting History** (Rebase, Reset, Reflog)
**Life Stage:** 40s—reframing your narrative, learning from mistakes  
**Git Concepts:** `git rebase -i`, `git reset`, `git reflog`, `git gc`  
**Theme:** You can change how you tell your story, but the reflog remembers  
**Exercise:** Use interactive rebase to reframe a messy period; use reflog to see what really happened  
**Learning Goal:** History is mutable in presentation but immutable in fact

## Technical Architecture

### Stack

```toml
[project]
name = "lifegit"
version = "0.1.0"
description = "Learn git through life decisions"
requires-python = ">=3.11"
dependencies = [
    "gitpython>=3.1.40",
    "typer>=0.9.0",
    "rich>=13.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
]
```

**Rationale:**
- **GitPython:** Mature, stable, mirrors git CLI (maintenance mode acceptable for educational use)
- **Typer:** Beautiful CLI with minimal code, great help system
- **Rich:** Gorgeous terminal output (panels, markdown, syntax highlighting, progress)
- **uv:** Fast dependency management for students

### Installation

Install `lifegit` as a global command using uv:

```bash
git clone <repo>
cd life.git
uv tool install .
```

After installation, `lifegit` is available from anywhere:

```bash
lifegit start my-life    # Start tutorial in new directory
cd my-life
lifegit status           # Check progress
lifegit validate 1       # Validate Act 1
```

**For development:** `lifegit.py` at repo root provides a local entry point (`./lifegit.py start`) that works from the project directory.

### Project Structure

```
life.git/
├── lifegit.py                   # Entry script (./lifegit.py start)
├── pyproject.toml
├── CLAUDE.md                    # This file
├── uv.lock
├── lifegit/                     # Main package
│   ├── __init__.py
│   ├── cli.py                   # Typer app entry point
│   ├── git_wrapper.py           # LifeRepo abstraction
│   ├── validator.py             # Exercise validation logic
│   ├── stages/
│   │   ├── __init__.py
│   │   ├── base.py              # BaseStage ABC + MenuOption
│   │   ├── act1.py              # The First Decision
│   │   └── act2.py              # What If?
│   └── content/
│       ├── __init__.py
│       ├── narratives.py        # Story text for each act
│       └── prompts.py           # Student prompts and hints
└── tests/                       # (planned)
```

### Core Classes

#### `LifeRepo` (git_wrapper.py)

Abstraction over GitPython that provides:
- Clean interface for git operations (no direct GitPython access needed in stages)
- Lazy initialization (repo can be uninitialized until `init()` is called)
- Validation methods for exercises
- State inspection (commits, branches, status)

```python
class LifeRepo:
    """Wrapper around GitPython for Life.git tutorial"""

    def __init__(self, path: Path = Path.cwd(), auto_init: bool = False):
        self.path = Path(path)
        self._repo: Repo | None = None
        # Only auto-init if requested; otherwise wait for explicit init()

    # Initialization
    def is_git_repo(self) -> bool:
        """Check if this path is a git repository"""

    def init(self) -> "LifeRepo":
        """Initialize a new git repository"""

    # Core operations
    def commit(self, message: str, files: list[str] | None = None):
        """Commit with optional file staging"""

    def stage_files(self, files: list[str]):
        """Stage files for commit"""

    def create_branch(self, name: str):
        """Create a new branch"""

    def checkout(self, branch: str):
        """Switch to a branch"""

    # Properties for status display
    @property
    def untracked_files(self) -> list[str]:
        """List of untracked files"""

    @property
    def staged_files(self) -> list[str]:
        """List of staged files"""

    # Validation helpers
    def count_commits(self, branch: str | None = None) -> int
    def is_initialized(self) -> bool  # has at least one commit
    def has_uncommitted_changes(self) -> bool
    def has_untracked_files(self) -> bool
    def current_branch(self) -> str
    def list_branches(self) -> list[str]
    def file_in_last_commit(self, filename: str) -> bool
```

#### `BaseStage` (stages/base.py)

Abstract base class for all acts with menu infrastructure:

```python
@dataclass
class MenuOption:
    """A single menu option"""
    key: str          # e.g., "1", "a"
    command: str      # e.g., "git add decision.txt"
    description: str  # e.g., "Stage your file for commit"
    action: str       # internal action identifier

class BaseStage(ABC):
    """Base class for all tutorial stages"""

    def __init__(self, repo: LifeRepo, console: Console, advanced: bool = False):
        self.repo = repo
        self.console = console
        self.advanced = advanced  # Menu mode vs manual git commands
        self.initial_state = self._capture_state()

    # Menu system for simple mode
    def show_menu(self, options: list[MenuOption], prompt: str) -> str:
        """Display a menu and return the selected action identifier"""

    def show_command_result(self, command: str, success: bool, message: str = ""):
        """Show the result of executing a git command"""

    def wait_for_file(self, filename: str, prompt_message: str | None = None):
        """Wait for a file to be created by the student"""

    def ask_for_input(self, prompt: str, default: str | None = None) -> str:
        """Ask student for text input (e.g., commit message)"""

    # Abstract methods
    @abstractmethod
    def introduction(self): pass

    @abstractmethod
    def run_exercise(self): pass  # Implements _run_simple() and _run_advanced()

    @abstractmethod
    def validate(self) -> bool: pass

    @abstractmethod
    def conclusion(self): pass

    def run(self):
        """Main execution flow: intro → exercise → validate → conclusion"""
```

#### `StageValidator` (validator.py)

Reusable validation logic:

```python
from pathlib import Path
from .git_wrapper import LifeRepo

class StageValidator:
    """Validation helpers for exercises"""
    
    @staticmethod
    def file_exists_and_committed(repo: LifeRepo, filename: str) -> bool:
        """Check if file exists and is in latest commit"""
        if not Path(filename).exists():
            return False
        
        last_commit = repo.repo.head.commit
        return filename in last_commit.stats.files
    
    @staticmethod
    def branch_exists(repo: LifeRepo, branch_name: str) -> bool:
        """Check if a branch exists"""
        return branch_name in repo.list_branches()
    
    @staticmethod
    def branches_merged(repo: LifeRepo, source: str, target: str) -> bool:
        """Check if source branch is merged into target"""
        # Implementation: check if source's commits are in target's history
        pass
    
    @staticmethod
    def conflict_resolved(repo: LifeRepo) -> bool:
        """Check if merge conflicts are resolved"""
        return not repo.has_conflicts() and not repo.has_uncommitted_changes()
```

### CLI Interface (cli.py)

```python
@app.command()
def start(
    directory: str = typer.Argument(
        None,
        help="Name of directory for your life repository (created if doesn't exist)",
    ),
    advanced: bool = typer.Option(
        False,
        "--advanced",
        help="Advanced mode: type git commands manually instead of using menus",
    ),
):
    """Begin your Life.git journey"""
    # 1. Find or create repo directory
    # 2. Change to repo directory
    # 3. Create LifeRepo(auto_init=False) - let Act 1 teach git init
    # 4. Run through acts with advanced flag

@app.command()
def validate(act: int, path: Path = Path.cwd()):
    """Validate your current exercise"""

@app.command()
def status(path: Path = Path.cwd()):
    """Show your progress through the tutorial"""
```

**Directory handling logic:**
1. `lifegit start my-life` → creates `./my-life/`, cd into it
2. `lifegit start` (no arg, in app root) → warns, prompts for name, creates dir
3. `lifegit start` (no arg, in existing repo) → uses it

## Student Experience Flow

### Setup

```bash
# Clone and install (one time)
git clone <tutorial-repo-url>
cd life.git
uv tool install .

# Start tutorial from anywhere
lifegit start my-life
cd my-life
```

### Menu-Driven Mode (Default)

Students select git commands from a menu instead of typing them:

```
╭────────────────────────────────────╮
│ Life.git                           │
│                                    │
│ Learn git by living a life in      │
│ commits                            │
│                                    │
│ Inspired by Derek Sivers on        │
│ commitment                         │
╰────────────────────────────────────╯
Created directory: my-life/
Working in: my-life

════════════════════════════════════════
   ACT 1: THE FIRST DECISION
════════════════════════════════════════

[Narrative about being 18, first major decision...]

Before you can track your life decisions, you need
to create a repository. A repository is like a
journal that remembers everything.

Ready to begin?

  [1] git init - Create a new repository (start your journal)

Choose: 1

$ git init
Initialized empty Git repository. Your journey begins here.

╭─────────────────────────────────────╮
│ Create a file called decision.txt  │
│ and write your decision inside.    │
│                                    │
│ What did you choose? University?   │
│ Work? Travel? Something else?      │
╰─────────────────────────────────────╯

Waiting for you to create 'decision.txt'...
Found 'decision.txt'

Your file is ready. What next?

  [1] git add decision.txt - Stage your file (tell git to track it)
  [2] git status           - See what git currently knows

Choose: 1

$ git add decision.txt
'decision.txt' is now staged for commit

Ready to make it permanent?

  [1] git commit - Save this moment to history
  [2] git status - See what's about to be committed

Choose: 1

Write your commit message (what are you deciding?) [My first decision]:

$ git commit -m "My first decision"
Decision committed to history
```

### Advanced Mode

For students who want to type git commands directly:

```bash
lifegit start my-life --advanced
```

Shows instructions and hints, validates completion, but student types all git commands manually.

## Development Roadmap

### Phase 1: MVP (Core Tutorial) ✓ COMPLETE
- [x] Set up project structure with uv
- [x] Implement `LifeRepo` wrapper with lazy init
- [x] Create `BaseStage` abstract class with menu infrastructure
- [x] Implement Act 1 (git init, add, commit)
- [x] Implement Act 2 (branch, checkout)
- [x] Basic validation logic
- [x] CLI with `start`, `validate`, `status` commands
- [x] Menu-driven mode (default) and --advanced mode
- [x] Directory setup flow with `git init` as first taught command

### Phase 2: Complete Acts
- [ ] Implement Act 3 (merging)
- [ ] Implement Act 4 (conflicts)
- [ ] Implement Act 5 (rebase/reflog)

### Phase 3: Polish & Testing
- [ ] Write comprehensive tests
- [ ] Create example completed repository
- [ ] Write detailed README for students

### Phase 4: Extensions
- [ ] Optional "sandbox mode" for free exploration
- [ ] Achievement system (badges for advanced techniques)
- [ ] Export final repo as portfolio piece

## Git Concept Mapping Reference

Quick reference for which git operations map to which life analogies:

| Git Operation | Life Analogy | Act |
|--------------|--------------|-----|
| `git init` | Birth, starting fresh | 1 |
| `git add` | Considering options | 1 |
| `git commit` | Making an irreversible decision | 1 |
| `git status` | Self-reflection, checking state | 1 |
| `git log` | Reviewing your past | 1 |
| `git branch` | Exploring "what if" scenarios | 2 |
| `git checkout`/`switch` | Living in an alternative timeline | 2 |
| `git merge` | Integrating different life aspects | 3 |
| `git merge --no-ff` | Preserving the story of integration | 3 |
| Merge conflicts | Values that clash, require resolution | 4 |
| Conflict markers | The explicit choice points | 4 |
| `git rebase` | Reframing your narrative | 5 |
| `git rebase -i` | Curating your story | 5 |
| `git reset` | Attempting to undo (but reflog knows) | 5 |
| `git reflog` | Your actual lived memory | 5 |
| `git gc` | Genuine forgetting, letting go | 5 |
| `git stash` | Postponing a decision | Advanced |
| `git cherry-pick` | Taking lessons from one context to another | Advanced |
| `git tag` | Marking significant life moments | Advanced |
| Detached HEAD | Living without clear direction | Advanced |

## Testing Strategy

### Unit Tests
- Git wrapper methods work correctly
- Validation logic returns correct results
- Stage state capture/restore

### Integration Tests
- Full act completion flows
- State persistence between acts
- Error handling for invalid operations

### Student Experience Tests
- Mock terminal interactions
- Validation feedback clarity
- Hint system effectiveness

## Success Criteria

Students completing this tutorial should:
1. **Understand git emotionally**, not just mechanically
2. **Remember commands** because they're tied to meaningful decisions
3. **Internalize branching** as safe exploration, not scary complexity
4. **Embrace commits** as clarity, not permanent mistakes
5. **Use git confidently** in future projects

## Future Ideas

- **Collaborative mode:** Multiple students work on shared "family tree" repo
- **Historical figures:** Play through Einstein's, Curie's, or Jobs' life decisions
- **Tragedy mode:** Learn recovery commands (`reflog`, `fsck`) by "dying" and restoring
- **Speed mode:** Timed challenges for git fluency
- **Story export:** Generate a narrative PDF from their final repo

## Notes for Development

- Keep prose natural, avoid over-formatting (per your style preferences)
- Use Rich sparingly—clarity over flash
- Validate incrementally, not just at end
- Provide hints before showing answers
- Celebrate successes with appropriate gravitas (this is life, after all)
- Allow students to personalize their stories (don't prescribe specific decisions)

---

**Current Status:** Phase 1 complete. Acts 1-2 implemented with menu-driven and advanced modes. Ready for Phase 2 (Acts 3-5).
