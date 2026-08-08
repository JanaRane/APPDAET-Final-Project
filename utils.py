import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

if "TERM" not in os.environ:
    os.environ["TERM"] = "xterm-256color"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner(title: str, subtitle: str = ""):
    clear()
    content = f"[bold white]{title.upper()}[/bold white]"
    if subtitle:
        content += f"\n[dim white]{subtitle}[/dim white]"
    console.print(Panel(content, border_style="blue", expand=False, padding=(0, 2), box=box.ROUNDED))


def print_error(msg: str):
    console.print(f"\n[bold red]ERROR:[/bold red] [red]{msg}[/red]")


def print_success(msg: str):
    console.print(f"\n[bold green]SUCCESS:[/bold green] [green]{msg}[/green]")


def render_table(title: str, columns: list, rows: list):
    table = Table(
        title=f"[bold white]{title.upper()}[/bold white]",
        border_style="blue",
        header_style="bold cyan",
        show_lines=True,
        box=box.ROUNDED
    )
    for col in columns:
        table.add_column(col["name"], justify=col.get("justify", "left"))

    for row in rows:
        table.add_row(*[str(item) for item in row])

    console.print(table)


def get_record_id(prompt):
    while True:
        value = console.input(f"[bold cyan]{prompt}[/bold cyan]").strip()
        if value == '':
            return None
        try:
            return int(value)
        except ValueError:
            print_error("Please enter a valid numeric ID.")


def get_item(prompt, allow_blank=False):
    while True:
        value = console.input(f"[bold cyan]{prompt}[/bold cyan]").strip()
        if allow_blank and value == '':
            return None
        if value:
            return value
        print_error("Input cannot be empty.")


def get_amount(prompt, allow_blank=False):
    while True:
        value = console.input(f"[bold cyan]{prompt}[/bold cyan]").strip()
        if allow_blank and value == '':
            return None
        try:
            amount = float(value)
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print_error("Please enter a valid positive numerical amount.")


def get_date(prompt, allow_blank=False):
    while True:
        value = console.input(f"[bold cyan]{prompt}[/bold cyan]").strip()
        if allow_blank and value == '':
            return None
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print_error("Invalid date format. Use YYYY-MM-DD.")


def confirm(prompt):
    while True:
        option = console.input(f"\n[bold yellow]{prompt}? (y/n): [/bold yellow]").strip().lower()
        if option in ("y", "yes"):
            return True
        elif option in ("n", "no"):
            return False
        else:
            print_error("Please enter 'y' for yes or 'n' for no.")