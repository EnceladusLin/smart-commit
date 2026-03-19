"""CLI for SmartCommit."""
import sys
import os
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax

from smart_commit.config import Config
from smart_commit.git_utils import GitAnalyzer
from smart_commit.ai_provider import get_provider


console = Console()


def init_config(config_path: Path = None) -> Config:
    """Initialize configuration."""
    cfg = Config(config_path)
    cfg.load()
    return cfg


@click.command()
@click.option("--provider", "-p", default=None, help="AI provider: openai, anthropic, ollama")
@click.option("--style", "-s", default=None, help="Commit style: conventional, short, detailed, emoji")
@click.option("--dry-run", "-d", is_flag=True, help="Show message without committing")
@click.option("--edit", "-e", is_flag=True, help="Edit message before committing")
@click.option("--auto-stage", is_flag=True, help="Auto-stage all changes before generating")
@click.option("--model", "-m", default=None, help="AI model to use")
def main(provider, style, dry_run, edit, auto_stage, model):
    """SmartCommit - AI-powered git commit messages."""
    try:
        # Load config
        cfg = init_config()

        # Override with CLI options
        if provider:
            cfg.set("ai.provider", provider)
        if style:
            cfg.set("commit.style", style)
        if model:
            cfg.set("ai.model", model)

        # Check for API key
        if not cfg.ensure_api_key():
            console.print("[red]No API key configured![/red]")
            console.print("Please set one of:")
            console.print("  OPENAI_API_KEY=sk-...     (OpenAI)")
            console.print("  ANTHROPIC_API_KEY=sk-...  (Claude)")
            console.print("  OLLAMA_HOST=http://...    (Local)")
            sys.exit(1)

        # Auto-stage if requested
        if auto_stage:
            os.system("git add .")

        # Initialize git
        try:
            git = GitAnalyzer()
        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(1)

        # Check for staged changes
        staged_files = git.get_staged_files()
        if not staged_files:
            console.print("[yellow]No staged changes found.[/yellow]")
            console.print("Run: git add <files>")
            sys.exit(0)

        # Get diff and summary
        diff = git.get_staged_diff()
        file_summary = git.get_file_summary()

        # Show analysis
        console.print("\n[bold cyan]Analyzing staged changes...[/bold cyan]")
        for f in file_summary:
            color = "[green]" if f["additions"] > 0 else "[red]"
            console.print(f"  {color}{f['file']}[/color] (+{f['additions']} -{f['deletions']})")

        # Get AI provider
        ai_provider = cfg.get("ai.provider", "openai")
        ai_model = cfg.get("ai.model", "gpt-4o-mini" if ai_provider == "openai" else "claude-sonnet-4-6")
        ai_temp = cfg.get("ai.temperature", 0.7)

        console.print(f"\n[dim]Using {ai_provider} / {ai_model}[/dim]")

        # Generate message
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating commit message...", total=None)

            try:
                prov = get_provider(ai_provider, model=ai_model, temperature=ai_temp)
                message = prov.generate_commit_message(
                    diff=diff,
                    file_summary=file_summary,
                    style=cfg.get("commit.style", "conventional"),
                )
            except Exception as e:
                console.print(f"\n[red]AI Error:[/red] {e}")
                sys.exit(1)

        # Display message
        console.print()
        console.print(Panel(
            message.strip(),
            title="Suggested commit message",
            border_style="cyan",
            padding=(1, 2),
        ))

        if dry_run:
            console.print("\n[yellow]Dry run - no commit created[/yellow]")
            return

        # Prompt user
        console.print("\n[dim][y] Accept  [e] Edit  [r] Regenerate  [a] Abort[/dim]")
        choice = console.input("> ").strip().lower()

        if choice == "a":
            console.print("[yellow]Aborted.[/yellow]")
            return
        elif choice == "r":
            main.callback(provider=provider, style=style, dry_run=False, edit=False, auto_stage=False, model=model)
            return
        elif choice == "e":
            message = console.input("\nEdit message:\n> ", default=message)
        elif choice != "y" and choice != "":
            console.print("[yellow]Invalid choice, aborting.[/yellow]")
            return

        # Commit
        git.commit(message.strip())
        console.print(f"\n[green]✓ Committed successfully![/green]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        sys.exit(130)


if __name__ == "__main__":
    main()
