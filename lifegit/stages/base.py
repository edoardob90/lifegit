"""Base class for all tutorial stages"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from ..git_wrapper import LifeRepo


@dataclass
class MenuOption:
    """A single menu option"""

    key: str  # e.g., "1", "a"
    command: str  # e.g., "git add decision.txt"
    description: str  # e.g., "Stage your file for commit"
    action: str  # internal action identifier


class BaseStage(ABC):
    """Abstract base class for tutorial acts"""

    # Subclasses should define these
    act_number: int = 0
    title: str = ""

    def __init__(self, repo: LifeRepo, console: Console, advanced: bool = False):
        self.repo = repo
        self.console = console
        self.advanced = advanced
        self.initial_state = self._capture_state()

    def _capture_state(self) -> dict:
        """Capture repo state at stage start for validation comparison"""
        if not self.repo.is_git_repo():
            return {
                "commits": 0,
                "branches": [],
                "current_branch": None,
            }
        return {
            "commits": self.repo.count_commits(),
            "branches": self.repo.list_branches(),
            "current_branch": self.repo.current_branch()
            if self.repo.is_initialized()
            else None,
        }

    # Menu system for simple mode

    def show_menu(
        self, options: list[MenuOption], prompt: str = "What would you like to do?"
    ) -> str:
        """Display a menu and return the selected action identifier"""
        self.console.print()
        self.console.print(f"[bold]{prompt}[/bold]")
        self.console.print()

        for opt in options:
            self.console.print(f"  [cyan][{opt.key}][/cyan] [bold]{opt.command}[/bold]")
            self.console.print(f"      [dim]{opt.description}[/dim]")

        self.console.print()
        valid_keys = [opt.key for opt in options]
        choice = Prompt.ask("Choose", choices=valid_keys, show_choices=False)

        # Find and return the action
        for opt in options:
            if opt.key == choice:
                return opt.action

        return options[0].action  # fallback

    def show_command_result(self, command: str, success: bool, message: str = ""):
        """Show the result of executing a git command"""
        self.console.print()
        if success:
            self.console.print(f"[green]$ {command}[/green]")
            if message:
                self.console.print(f"[dim]{message}[/dim]")
        else:
            self.console.print(f"[red]$ {command}[/red]")
            if message:
                self.console.print(f"[red]{message}[/red]")

    def wait_for_file(self, filename: str, prompt_message: str | None = None):
        """Wait for a file to be created by the student"""

        if prompt_message:
            self.console.print()
            self.console.print(Panel(prompt_message, border_style="yellow"))

        while not (self.repo.path / filename).exists():
            self.console.print()
            self.console.print(f"[dim]Waiting for you to create '{filename}'...[/dim]")
            input("Press Enter when ready...")

        self.console.print(f"[green]Found '{filename}'[/green]")

    def ask_for_input(self, prompt: str, default: str | None = None) -> str:
        """Ask student for text input (e.g., commit message, branch name)"""
        self.console.print()
        if default:
            return Prompt.ask(prompt, default=default)
        return Prompt.ask(prompt)

    # Abstract methods for subclasses

    @abstractmethod
    def introduction(self):
        """Display act introduction and narrative"""
        pass

    @abstractmethod
    def run_exercise(self):
        """Run the interactive exercise (simple or advanced mode)"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Check if the exercise is complete"""
        pass

    @abstractmethod
    def conclusion(self):
        """Wrap up the act and connect to git concepts"""
        pass

    def run(self):
        """Main execution flow for a stage"""
        self.introduction()
        self.run_exercise()

        # Final validation check
        if not self.validate():
            self.console.print(
                "\n[yellow]Something's not quite right. Let's check...[/yellow]"
            )
            while not self.validate():
                input("Press Enter to check again...")

        self.conclusion()
