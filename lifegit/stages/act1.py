"""Act 1: The First Decision - Introduction to commits"""

from rich.panel import Panel
from rich.text import Text

from ..content.narratives import ACT1_NARRATIVE
from ..content.prompts import ACT1_PROMPTS
from ..validator import StageValidator
from .base import BaseStage


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
        self.console.print()

    def instructions(self):
        """Give the student their task"""
        self.console.print(
            Panel(
                ACT1_PROMPTS["instructions"],
                title="[bold yellow]Your Task[/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
        )
        self.console.print()
        self.console.print("[dim]Press Enter when you've committed your decision...[/dim]")

    def validate(self) -> bool:
        """Check if the exercise is complete"""
        filename = ACT1_PROMPTS["file_name"]

        # Must have the file
        if not StageValidator.file_exists(filename, self.repo.path):
            return False

        # Must have at least one commit (more than initial state)
        if self.repo.count_commits() <= self.initial_state["commits"]:
            return False

        # File should be in the latest commit
        if not self.repo.file_in_last_commit(filename):
            return False

        return True

    def hint(self):
        """Provide progressive hints"""
        filename = ACT1_PROMPTS["file_name"]

        if not StageValidator.file_exists(filename, self.repo.path):
            self.console.print(f"\n[cyan]Hint:[/cyan] First, create the file '{filename}'")
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
        self.console.print("  [cyan]git add[/cyan]    — stage changes (consider your options)")
        self.console.print("  [cyan]git commit[/cyan] — make it permanent (decide)")
        self.console.print("  [cyan]git status[/cyan] — see where you are")
        self.console.print("  [cyan]git log[/cyan]    — review your history")
        self.console.print()
