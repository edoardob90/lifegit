"""CLI entry point for Life.git tutorial"""

import os
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .git_wrapper import LifeRepo
from .stages import Act1, Act2

app = typer.Typer(
    name="lifegit",
    help="Learn git through life decisions",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


def _is_app_root() -> bool:
    """Check if running from the life.git root directory"""
    app_root = Path(__file__).parent.parent.resolve()
    return Path.cwd().resolve() == app_root


def _find_or_create_repo_dir(directory: str | None) -> Path:
    """Determine the repository directory based on argument and current state"""
    cwd = Path.cwd()

    # Check if running from the app root without specifying a directory
    if _is_app_root():
        if directory is None:
            console.print()
            console.print("[yellow]You're in the Life.git app directory[/yellow]")
            console.print(
                "[dim]Your journey needs its own folder to avoid mixing with the app files.[/dim]"
            )
            console.print()
            directory = Prompt.ask(
                "What would you like to name your life journey?",
                default="my-life",
            )
            repo_path = cwd / directory
            if not repo_path.exists():
                repo_path.mkdir(parents=True)
                console.print(f"[green]Created directory: {directory}/[/green]")
            return repo_path

    # If directory argument provided, use it
    if directory:
        repo_path = cwd / directory
        if not repo_path.exists():
            repo_path.mkdir(parents=True)
            console.print(f"[green]Created directory: {directory}/[/green]")
        return repo_path

    # No directory provided and no existing repo - ask for a name
    console.print()
    name = Prompt.ask(
        "What would you like to name your life journey?",
        default="my-life",
    )

    repo_path = cwd / name
    if repo_path.exists():
        console.print(f"[yellow]Directory '{name}' already exists, using it[/yellow]")
    else:
        repo_path.mkdir(parents=True)
        console.print(f"[green]Created directory: {name}/[/green]")

    return repo_path


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

    # Welcome banner
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Life.git[/bold cyan]\n\n"
            "Learn git by living a life in commits\n\n"
            "[dim]Inspired by Derek Sivers on commitment[/dim]",
            border_style="cyan",
        )
    )

    if advanced:
        console.print(
            "[dim]Running in advanced mode - you'll type git commands directly[/dim]"
        )

    # Determine repository directory
    repo_path = _find_or_create_repo_dir(directory)

    # Change to repo directory so file operations work correctly
    os.chdir(repo_path)
    console.print(f"[dim]Working in: {repo_path}[/dim]")
    console.print()

    # Create repo wrapper (don't auto-init - Act 1 will guide this)
    repo = LifeRepo(repo_path, auto_init=False)

    # Run through acts
    acts = [Act1, Act2]
    for i, ActClass in enumerate(acts, 1):
        console.print(f"\n[bold yellow]{'═' * 40}[/bold yellow]")
        console.print(
            f"[bold yellow]   ACT {i}: {ActClass.title.upper()}[/bold yellow]"
        )
        console.print(f"[bold yellow]{'═' * 40}[/bold yellow]\n")

        act = ActClass(repo, console, advanced=advanced)
        act.run()

        if i < len(acts):
            console.print()
            if not typer.confirm("Ready for the next act?", default=True):
                console.print(
                    "\n[dim]Take your time. Run 'lifegit start' when you're ready to continue.[/dim]"
                )
                raise typer.Exit()

    # Completion
    console.print()
    console.print(
        Panel(
            "[bold green]Tutorial Complete![/bold green]\n\n"
            "You've learned git by living a life.\n"
            "Your repository now tells a story—your story.\n\n"
            "[dim]Continue exploring with Acts 3-5 (coming soon):[/dim]\n"
            "  Act 3: Integration (merging)\n"
            "  Act 4: Conflict (merge conflicts)\n"
            "  Act 5: Rewriting History (rebase, reflog)",
            border_style="green",
        )
    )


@app.command()
def validate(
    act: int = typer.Argument(..., help="Act number to validate (1-2)"),
    path: Path = typer.Option(Path.cwd(), "--path", "-p", help="Path to repository"),
):
    """Validate your current exercise"""
    repo = LifeRepo(path)

    acts = {1: Act1, 2: Act2}

    if act not in acts:
        console.print("[red]Act must be 1 or 2 (Acts 3-5 coming soon)[/red]")
        raise typer.Exit(1)

    stage = acts[act](repo, console)

    if stage.validate():
        console.print(f"[green]✓ Act {act} complete![/green]")
    else:
        console.print(f"[red]✗ Act {act} not complete yet[/red]")
        console.print()
        console.print("[dim]Run 'lifegit start' to continue the tutorial.[/dim]")


@app.command()
def status(
    path: Path = typer.Option(Path.cwd(), "--path", "-p", help="Path to repository"),
):
    """Show your progress through the tutorial"""
    repo = LifeRepo(path)

    if not repo.is_initialized():
        console.print(
            Panel(
                "[yellow]No commits yet[/yellow]\n\n"
                "Run [cyan]lifegit start[/cyan] to begin your journey.",
                title="Your Life.git Status",
                border_style="yellow",
            )
        )
        return

    branches = repo.list_branches()
    whatif_branches = [b for b in branches if b.startswith("what-if-")]

    console.print(
        Panel(
            f"[cyan]Current branch:[/cyan] {repo.current_branch()}\n"
            f"[cyan]Total commits:[/cyan] {repo.count_commits()}\n"
            f"[cyan]Branches:[/cyan] {', '.join(branches)}\n"
            f"[cyan]What-if branches:[/cyan] {len(whatif_branches)}",
            title="Your Life.git Status",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    app()
