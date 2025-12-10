"""CLI entry point for Life.git tutorial"""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from .git_wrapper import LifeRepo
from .stages import Act1, Act2

app = typer.Typer(
    name="lifegit",
    help="Learn git through life decisions",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


@app.command()
def start(
    path: Path = typer.Option(
        Path.cwd(),
        "--path",
        "-p",
        help="Path to tutorial repository (defaults to current directory)",
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
    console.print()

    # Initialize repository
    repo = LifeRepo(path)

    # Run through acts
    acts = [Act1, Act2]
    for i, ActClass in enumerate(acts, 1):
        console.print(f"\n[bold yellow]{'═' * 40}[/bold yellow]")
        console.print(
            f"[bold yellow]   ACT {i}: {ActClass.title.upper()}[/bold yellow]"
        )
        console.print(f"[bold yellow]{'═' * 40}[/bold yellow]\n")

        act = ActClass(repo, console)
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
        stage.instructions()


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
