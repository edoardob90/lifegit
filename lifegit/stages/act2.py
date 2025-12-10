"""Act 2: What If? - Introduction to branching"""

from rich.panel import Panel
from rich.text import Text

from ..content.narratives import ACT2_NARRATIVE
from ..content.prompts import ACT2_PROMPTS
from ..validator import StageValidator
from .base import BaseStage


class Act2(BaseStage):
    """What If? - exploring branches"""

    act_number = 2
    title = "What If?"

    def introduction(self):
        """Display the opening narrative"""
        self.console.print()
        self.console.print(
            Panel(
                Text(ACT2_NARRATIVE["introduction"]),
                title="[bold]Act 2: What If?[/bold]",
                subtitle="[dim]Mid-20s — Exploring Alternatives[/dim]",
                border_style="cyan",
                padding=(1, 2),
            )
        )
        self.console.print()

    def instructions(self):
        """Give the student their task"""
        self.console.print(
            Panel(
                ACT2_PROMPTS["instructions"],
                title="[bold yellow]Your Task[/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
        )
        self.console.print()
        self.console.print(
            "[dim]Press Enter when you've created a branch, committed to it, and returned to main...[/dim]"
        )

    def validate(self) -> bool:
        """Check if the exercise is complete"""
        prefix = ACT2_PROMPTS["branch_prefix"]

        # Must have created at least one "what-if-" branch
        branches = self.repo.list_branches()
        whatif_branches = [b for b in branches if b.startswith(prefix)]

        if not whatif_branches:
            return False

        # Must have more commits than when we started
        if self.repo.count_commits() <= self.initial_state["commits"]:
            return False

        # Must be back on main (or master)
        current = self.repo.current_branch()
        if current not in ("main", "master"):
            return False

        # At least one what-if branch should have commits beyond main
        main_commits = self.repo.count_commits()
        for branch in whatif_branches:
            branch_commits = self.repo.count_commits(branch)
            if branch_commits > main_commits:
                return True

        # If what-if branch has same commits as main, check if it has unique files
        # (this handles the case where student committed on the branch)
        return len(whatif_branches) > 0 and self.repo.count_commits() > self.initial_state["commits"]

    def hint(self):
        """Provide progressive hints"""
        prefix = ACT2_PROMPTS["branch_prefix"]
        branches = self.repo.list_branches()
        whatif_branches = [b for b in branches if b.startswith(prefix)]

        if not whatif_branches:
            self.console.print(f"\n[cyan]Hint:[/cyan] Create a 'what-if' branch first")
            self.console.print(f"  [dim]git branch {prefix}travel[/dim]")
            self.console.print(f"  [dim]git checkout {prefix}travel[/dim]")
            return

        current = self.repo.current_branch()
        if current.startswith(prefix):
            # They're on a what-if branch
            if not self.repo.has_uncommitted_changes() and self.repo.count_commits() <= self.initial_state["commits"]:
                self.console.print("\n[cyan]Hint:[/cyan] Create a file describing this alternate path")
                self.console.print("  [dim]echo 'In this timeline...' > alternate-life.txt[/dim]")
                self.console.print("  [dim]git add alternate-life.txt && git commit -m 'What if...'[/dim]")
            elif self.repo.has_uncommitted_changes():
                self.console.print("\n[cyan]Hint:[/cyan] Commit your changes on this branch")
                self.console.print("  [dim]git add . && git commit -m 'Exploring what if...'[/dim]")
            else:
                self.console.print("\n[cyan]Hint:[/cyan] Now return to your main timeline")
                self.console.print("  [dim]git checkout main[/dim]")
            return

        # They're on main but have what-if branches
        self.console.print("\n[cyan]Hint:[/cyan] Check if you committed something on your what-if branch")
        self.console.print(f"  [dim]git log {whatif_branches[0]} --oneline[/dim]")

    def conclusion(self):
        """Wrap up and explain the git concepts"""
        branches = self.repo.list_branches()
        whatif_branches = [b for b in branches if b.startswith(ACT2_PROMPTS["branch_prefix"])]

        self.console.print()
        self.console.print(
            Panel(
                Text(ACT2_NARRATIVE["conclusion"]),
                title="[bold green]Alternate Timelines Created[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )

        # Show their branches
        self.console.print()
        self.console.print("[bold]Your branches:[/bold]")
        for branch in branches:
            marker = "*" if branch == self.repo.current_branch() else " "
            style = "green" if branch == self.repo.current_branch() else "white"
            self.console.print(f"  [{style}]{marker} {branch}[/{style}]")

        self.console.print()
        self.console.print("[bold]What you learned:[/bold]")
        self.console.print("  [cyan]git branch <name>[/cyan]   — create an alternate timeline")
        self.console.print("  [cyan]git checkout <name>[/cyan] — step into that timeline")
        self.console.print("  [cyan]git branch[/cyan]          — see all your timelines")
        self.console.print("  [cyan]git switch <name>[/cyan]   — modern way to switch branches")
        self.console.print()
