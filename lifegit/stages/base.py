"""Base class for all tutorial stages"""

from abc import ABC, abstractmethod

from rich.console import Console

from ..git_wrapper import LifeRepo


class BaseStage(ABC):
    """Abstract base class for tutorial acts"""

    # Subclasses should define these
    act_number: int = 0
    title: str = ""

    def __init__(self, repo: LifeRepo, console: Console):
        self.repo = repo
        self.console = console
        self.initial_state = self._capture_state()

    def _capture_state(self) -> dict:
        """Capture repo state at stage start for validation comparison"""
        return {
            "commits": self.repo.count_commits(),
            "branches": self.repo.list_branches(),
            "current_branch": self.repo.current_branch() if self.repo.is_initialized() else None,
        }

    @abstractmethod
    def introduction(self):
        """Display act introduction and narrative"""
        pass

    @abstractmethod
    def instructions(self):
        """Give student clear instructions for the exercise"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Check if the exercise is complete"""
        pass

    @abstractmethod
    def conclusion(self):
        """Wrap up the act and connect to git concepts"""
        pass

    def hint(self):
        """Provide a hint if student is stuck (optional override)"""
        self.console.print("\n[dim]No hints available for this stage.[/dim]")

    def run(self):
        """Main execution flow for a stage"""
        self.introduction()
        self.instructions()

        # Wait for completion with retry loop
        while not self.validate():
            self.console.print("\n[yellow]Not quite there yet. Try again![/yellow]")
            response = input("Press Enter to check again (or 'hint' for help)... ").strip().lower()
            if response == "hint":
                self.hint()

        self.conclusion()
