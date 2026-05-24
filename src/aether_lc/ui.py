from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@contextmanager
def loading(message: str) -> Iterator[None]:
    with console.status(message, spinner="dots"):
        yield


def success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")


def warning(message: str) -> None:
    console.print(f"[bold yellow]{message}[/bold yellow]")


def error(message: str) -> None:
    console.print(f"[bold red]{message}[/bold red]")


def render_profile(profile: dict[str, Any]) -> None:
    solved = profile["solved"]
    total = profile["total"]

    table = Table(title="LeetCode CN Profile")
    table.add_column("Item", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Username", str(profile.get("username") or "-"))
    table.add_row("Real Name", str(profile.get("real_name") or "-"))
    table.add_row("Premium", "Yes" if profile.get("is_premium") else "No")
    table.add_row("Solved", f"All {solved['All']} | Easy {solved['Easy']} | Medium {solved['Medium']} | Hard {solved['Hard']}")
    table.add_row("Total", f"All {total['All']} | Easy {total['Easy']} | Medium {total['Medium']} | Hard {total['Hard']}")

    console.print(Panel(table, border_style="green"))