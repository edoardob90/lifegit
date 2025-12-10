"""Act 1: The First Decision - Introduction to commits"""

from rich.panel import Panel
from rich.text import Text

from ..content.narratives import ACT1_NARRATIVE
from ..content.prompts import ACT1_PROMPTS
from ..validator import StageValidator
from .base import BaseStage, MenuOption


class Act1(BaseStage):
    """The First Decision - commits and the working directory"""

    act_number = 1
    title = "The First Decision"

    def introduction(self):
        """Display the opening narrative"""
        self.console.print()
        self.console.print(
            Panel(
                Text(ACT1_NARRATIVE["introduction"]),
                title="[bold]Act 1: The First Decision[/bold]",
                subtitle="[dim]Age 18 — Leaving Home[/dim]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

    def run_exercise(self):
        """Run the interactive exercise"""
        filename = ACT1_PROMPTS["file_name"]

        if self.advanced:
            self._run_advanced(filename)
        else:
            self._run_simple(filename)

    def _run_simple(self, filename: str):
        """Menu-driven flow for beginners"""
        # Step 0: Initialize git repository if needed
        if not self.repo.is_git_repo():
            self.console.print()
            self.console.print(
                "[dim]Before you can track your life decisions, you need to create a repository.\n"
                "A repository is like a journal that remembers everything.[/dim]"
            )

            initialized = False
            while not initialized:
                action = self.show_menu(
                    [
                        MenuOption("1", "git init", "Create a new repository (start your journal)", "init"),
                    ],
                    "Ready to begin?",
                )

                if action == "init":
                    self.repo.init()
                    self.show_command_result(
                        "git init",
                        True,
                        "Initialized empty Git repository. Your journey begins here.",
                    )
                    initialized = True

        # Step 1: Wait for file creation
        self.wait_for_file(
            filename,
            "Create a file called [bold]decision.txt[/bold] and write your decision inside.\n\n"
            "What did you choose? University? Work? Travel? Something else?\n"
            "Write it down. Be specific. This is [italic]your[/italic] decision to make.",
        )

        # Step 2: Stage the file
        self.console.print()
        self.console.print(
            "[dim]Your file exists, but git doesn't know about it yet. "
            "It's 'untracked' - invisible to version control.[/dim]"
        )

        staged = False
        while not staged:
            action = self.show_menu(
                [
                    MenuOption("1", f"git add {filename}", "Stage your file (tell git to track it)", "add"),
                    MenuOption("2", "git status", "See what git currently knows", "status"),
                ],
                "Your file is ready. What next?",
            )

            if action == "add":
                self.repo.stage_files([filename])
                self.show_command_result(f"git add {filename}", True, f"'{filename}' is now staged for commit")
                staged = True
            elif action == "status":
                self._show_status()

        # Step 3: Commit
        self.console.print()
        self.console.print(
            "[dim]Your file is staged - git knows about it now. "
            "But it's not saved to history yet. Time to commit.[/dim]"
        )

        committed = False
        while not committed:
            action = self.show_menu(
                [
                    MenuOption("1", "git commit", "Save this moment to history", "commit"),
                    MenuOption("2", "git status", "See what's about to be committed", "status"),
                ],
                "Ready to make it permanent?",
            )

            if action == "commit":
                message = self.ask_for_input(
                    "Write your commit message (what are you deciding?)",
                    default="My first decision",
                )
                self.repo.commit(message)
                self.show_command_result(f'git commit -m "{message}"', True, "Decision committed to history")
                committed = True
            elif action == "status":
                self._show_status()

    def _run_advanced(self, filename: str):
        """Traditional flow - student types commands manually"""
        # Show git init instruction if needed
        if not self.repo.is_git_repo():
            self.console.print(
                Panel(
                    "First, initialize a git repository:\n\n"
                    "    git init\n\n"
                    "Then proceed with the exercise below.",
                    title="[bold yellow]Setup Required[/bold yellow]",
                    border_style="yellow",
                    padding=(1, 2),
                )
            )
            self.console.print()

        self.console.print(
            Panel(
                ACT1_PROMPTS["instructions"],
                title="[bold yellow]Your Task[/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
        )
        self.console.print()
        self.console.print("[dim]Press Enter when you've committed your decision (type 'hint' for help)...[/dim]")

        # Wait for completion
        while not self.validate():
            response = input("").strip().lower()
            if response == "hint":
                self._show_hint(filename)

    def _show_status(self):
        """Show git status in a friendly way"""
        self.console.print()
        self.console.print("[green]$ git status[/green]")

        if not self.repo.is_git_repo():
            self.console.print("[yellow]Not a git repository yet. Run 'git init' first.[/yellow]")
            return

        if not self.repo.is_initialized():
            self.console.print("[dim]No commits yet[/dim]")

        if self.repo.untracked_files:
            self.console.print("[red]Untracked files:[/red]")
            for f in self.repo.untracked_files:
                self.console.print(f"  [red]{f}[/red]")

        if self.repo.staged_files:
            self.console.print("[green]Changes to be committed:[/green]")
            for f in self.repo.staged_files:
                self.console.print(f"  [green]{f}[/green]")

    def _show_hint(self, filename: str):
        """Provide progressive hints for advanced mode"""
        if not self.repo.is_git_repo():
            self.console.print("\n[cyan]Hint:[/cyan] Initialize a git repository first")
            self.console.print("  [dim]git init[/dim]")
            return

        if not StageValidator.file_exists(filename, self.repo.path):
            self.console.print(f"\n[cyan]Hint:[/cyan] Create the file '{filename}'")
            self.console.print(f"  [dim]echo 'My decision: ...' > {filename}[/dim]")
            return

        if self.repo.has_untracked_files():
            self.console.print("\n[cyan]Hint:[/cyan] Your file exists but isn't staged yet")
            self.console.print(f"  [dim]git add {filename}[/dim]")
            return

        if self.repo.has_uncommitted_changes():
            self.console.print("\n[cyan]Hint:[/cyan] Your file is staged. Now commit it!")
            self.console.print("  [dim]git commit -m 'My first decision'[/dim]")
            return

        self.console.print("\n[cyan]Hint:[/cyan] Check your status with: git status")

    def validate(self) -> bool:
        """Check if the exercise is complete"""
        # Must have a git repository
        if not self.repo.is_git_repo():
            return False

        filename = ACT1_PROMPTS["file_name"]

        # Must have the file
        if not StageValidator.file_exists(filename, self.repo.path):
            return False

        # Must have at least one commit (more than initial state)
        initial_commits = self.initial_state.get("commits", 0) or 0
        if self.repo.count_commits() <= initial_commits:
            return False

        # File should be in the latest commit
        if not self.repo.file_in_last_commit(filename):
            return False

        return True

    def conclusion(self):
        """Wrap up and explain the git concepts"""
        self.console.print()
        self.console.print(
            Panel(
                Text(ACT1_NARRATIVE["conclusion"]),
                title="[bold green]Decision Made[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

        # Show what they did in git terms
        self.console.print()
        self.console.print("[bold]What you learned:[/bold]")
        self.console.print("  [cyan]git init[/cyan]   — create a repository (start tracking)")
        self.console.print("  [cyan]git add[/cyan]    — stage changes (consider your options)")
        self.console.print("  [cyan]git commit[/cyan] — make it permanent (decide)")
        self.console.print("  [cyan]git status[/cyan] — see where you are")
        self.console.print("  [cyan]git log[/cyan]    — review your history")
        self.console.print()
