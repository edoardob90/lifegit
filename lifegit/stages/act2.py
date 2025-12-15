"""Act 2: What If? - Introduction to branching"""

from rich.panel import Panel
from rich.text import Text

from ..content import content
from ..validator import StageValidator
from .base import BaseStage, MenuOption


class Act2(BaseStage):
    """What If? - exploring branches"""

    act_number = 2
    title = "What If?"

    def introduction(self):
        """Display the opening narrative"""
        self.console.print()
        self.console.print(
            Panel(
                Text(content.act2.narrative.introduction),
                title="[bold]Act 2: What If?[/bold]",
                subtitle="[dim]Mid-20s — Exploring Alternatives[/dim]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

    def run_exercise(self):
        """Run the interactive exercise"""
        if self.advanced:
            self._run_advanced()
        else:
            self._run_simple()

    def _run_simple(self):
        """Menu-driven flow for beginners"""
        prefix = content.act2.prompts.branch_prefix

        # Step 1: Think about a "what if" and create a branch
        self.console.print()
        self.console.print(
            Panel(
                "Think of a path you didn't take. A 'what if?' that still crosses your mind.\n\n"
                "What if you'd traveled instead? Started that company? Moved abroad?\n"
                "Stayed home? Taken that other job?",
                border_style="yellow",
            )
        )

        branch_name = self.ask_for_input(
            f"Name your alternate timeline (will be prefixed with '{prefix}')",
            default="travel",
        )
        full_branch_name = f"{prefix}{branch_name}"

        # Create and checkout the branch
        branch_created = False
        while not branch_created:
            action = self.show_menu(
                [
                    MenuOption("1", f"git branch {full_branch_name}", "Create the alternate timeline", "branch"),
                    MenuOption("2", "git branch", "See existing branches", "list"),
                ],
                "Ready to create your 'what if' timeline?",
            )

            if action == "branch":
                self.repo.create_branch(full_branch_name)
                self.show_command_result(
                    f"git branch {full_branch_name}",
                    True,
                    f"Branch '{full_branch_name}' created",
                )
                branch_created = True
            elif action == "list":
                self._show_branches()

        # Step 2: Switch to the branch
        self.console.print()
        self.console.print(
            "[dim]The branch exists, but you're still on your main timeline. "
            "Let's step into the alternate reality.[/dim]"
        )

        switched = False
        while not switched:
            action = self.show_menu(
                [
                    MenuOption("1", f"git checkout {full_branch_name}", "Step into the alternate timeline", "checkout"),
                    MenuOption("2", "git branch", "See where you are", "list"),
                ],
                "Ready to explore the road not taken?",
            )

            if action == "checkout":
                self.repo.checkout(full_branch_name)
                self.show_command_result(
                    f"git checkout {full_branch_name}",
                    True,
                    f"Switched to branch '{full_branch_name}'",
                )
                switched = True
            elif action == "list":
                self._show_branches()

        # Step 3: Create a file describing this alternate life
        alt_filename = f"{branch_name}-life.txt"
        self.wait_for_file(
            alt_filename,
            f"Create a file called [bold]{alt_filename}[/bold] describing this alternate life.\n\n"
            "What would your life look like if you'd taken this path?\n"
            "Write a few lines about this alternate version of yourself.",
        )

        # Step 4: Stage and commit on the branch
        self.console.print()
        self.console.print("[dim]Time to commit this alternate reality to its own timeline.[/dim]")

        staged = False
        while not staged:
            action = self.show_menu(
                [
                    MenuOption("1", f"git add {alt_filename}", "Stage your alternate life", "add"),
                    MenuOption("2", "git status", "See current state", "status"),
                ],
                "Stage your changes?",
            )

            if action == "add":
                self.repo.stage_files([alt_filename])
                self.show_command_result(f"git add {alt_filename}", True)
                staged = True
            elif action == "status":
                self._show_status()

        committed = False
        while not committed:
            action = self.show_menu(
                [
                    MenuOption("1", "git commit", "Save this alternate timeline", "commit"),
                    MenuOption("2", "git status", "See what's staged", "status"),
                ],
                "Commit to this alternate reality?",
            )

            if action == "commit":
                message = self.ask_for_input(
                    "Describe this alternate path",
                    default=f"What if I'd chosen {branch_name}?",
                )
                self.repo.commit(message)
                self.show_command_result(f'git commit -m "{message}"', True)
                committed = True
            elif action == "status":
                self._show_status()

        # Step 5: Return to main
        self.console.print()
        self.console.print(
            "[dim]You've explored the alternate timeline. "
            "Now let's return to your actual path—your main branch.[/dim]"
        )

        main_branch = "main" if "main" in self.repo.list_branches() else "master"
        returned = False
        while not returned:
            action = self.show_menu(
                [
                    MenuOption("1", f"git checkout {main_branch}", "Return to your actual timeline", "checkout_main"),
                    MenuOption("2", "git branch", "See all timelines", "list"),
                ],
                "Ready to return to reality?",
            )

            if action == "checkout_main":
                self.repo.checkout(main_branch)
                self.show_command_result(
                    f"git checkout {main_branch}",
                    True,
                    f"Switched to branch '{main_branch}'",
                )
                returned = True
            elif action == "list":
                self._show_branches()

    def _run_advanced(self):
        """Traditional flow - student types commands manually"""
        self.console.print(
            Panel(
                content.act2.prompts.instructions,
                title="[bold yellow]Your Task[/bold yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
        )
        self.console.print()
        self.console.print(
            "[dim]Press Enter when you've created a branch, committed to it, and returned to main...[/dim]"
        )

        prefix = content.act2.prompts.branch_prefix

        # Wait for completion
        while not self.validate():
            response = input("").strip().lower()
            if response == "hint":
                self._show_hint(prefix)

    def _show_branches(self):
        """Show branches in a friendly way"""
        self.console.print()
        self.console.print("[green]$ git branch[/green]")

        branches = self.repo.list_branches()
        current = self.repo.current_branch()

        for branch in branches:
            marker = "*" if branch == current else " "
            style = "green" if branch == current else "white"
            self.console.print(f"  [{style}]{marker} {branch}[/{style}]")

    def _show_status(self):
        """Show git status in a friendly way"""
        self.console.print()
        self.console.print("[green]$ git status[/green]")
        self.console.print(f"[dim]On branch {self.repo.current_branch()}[/dim]")

        if self.repo.untracked_files:
            self.console.print("[red]Untracked files:[/red]")
            for f in self.repo.untracked_files:
                self.console.print(f"  [red]{f}[/red]")

        if self.repo.staged_files:
            self.console.print("[green]Staged files:[/green]")
            for f in self.repo.staged_files:
                self.console.print(f"  [green]{f}[/green]")

    def _show_hint(self, prefix: str):
        """Provide progressive hints for advanced mode"""
        branches = self.repo.list_branches()
        whatif_branches = [b for b in branches if b.startswith(prefix)]

        if not whatif_branches:
            self.console.print(f"\n[cyan]Hint:[/cyan] Create a 'what-if' branch first")
            self.console.print(f"  [dim]git branch {prefix}travel[/dim]")
            self.console.print(f"  [dim]git checkout {prefix}travel[/dim]")
            return

        current = self.repo.current_branch()
        if current.startswith(prefix):
            if self.repo.count_commits() <= self.initial_state["commits"]:
                self.console.print("\n[cyan]Hint:[/cyan] Create a file and commit on this branch")
                self.console.print("  [dim]echo 'In this timeline...' > alternate.txt[/dim]")
                self.console.print("  [dim]git add alternate.txt && git commit -m 'What if...'[/dim]")
            else:
                self.console.print("\n[cyan]Hint:[/cyan] Return to your main timeline")
                self.console.print("  [dim]git checkout main[/dim]")
            return

        self.console.print("\n[cyan]Hint:[/cyan] Looks good! Make sure you committed on your what-if branch.")

    def validate(self) -> bool:
        """Check if the exercise is complete"""
        prefix = content.act2.prompts.branch_prefix

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

        return True

    def conclusion(self):
        """Wrap up and explain the git concepts"""
        branches = self.repo.list_branches()

        self.console.print()
        self.console.print(
            Panel(
                Text(content.act2.narrative.conclusion),
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
