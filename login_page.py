import json
import os
import pwinput
import utils
import main
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()
USERS_FILE = "users.json"
DATA_FILE = "data.json"


def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def login():
    utils.print_banner("USER AUTHENTICATION", "Secure Access Gateway")
    users = load_json(USERS_FILE)

    username = console.input("[bold cyan]Username:[/bold cyan] ").strip()
    password = pwinput.pwinput("Password: ", mask="•").strip()

    for user_id, info in users.items():
        if info.get("username") == username and info.get("password") == password:
            main.main(user_id)
            return

    utils.print_error("Authentication failed. Invalid username or password.")
    input("\nPress Enter to return...")


def register():
    utils.print_banner("PROFILE REGISTRATION", "Create New User Profile")
    users = load_json(USERS_FILE)
    data = load_json(DATA_FILE)

    username = console.input("[bold cyan]Enter Username:[/bold cyan] ").strip()
    if not username:
        utils.print_error("Username cannot be left blank.")
        input("\nPress Enter to return...")
        return

    for info in users.values():
        if info.get("username") == username:
            utils.print_error("Username already registered in system.")
            input("\nPress Enter to return...")
            return

    password = pwinput.pwinput("Enter Password: ", mask="•").strip()
    if not password:
        utils.print_error("Password cannot be left blank.")
        input("\nPress Enter to return...")
        return

    user_id = str(len(users) + 1)
    users[user_id] = {"username": username, "password": password}

    data[user_id] = {
        "incomes": [],
        "expenses": [],
        "bills_and_subscriptions": [],
        "budget_plans": {"income": 0.0, "expenses": 0.0, "bills": 0.0}
    }

    save_json(USERS_FILE, users)
    save_json(DATA_FILE, data)

    utils.print_success("User profile successfully registered.")
    input("\nPress Enter to log in...")
    main.main(user_id)


def start():
    while True:
        utils.clear()
        menu_text = (
            " [cyan][1][/cyan] Account Login\n"
            " [cyan][2][/cyan] Register Profile\n"
            " [red][3][/red] Exit System"
        )
        console.print(Panel(
            menu_text,
            title="[bold white]BUDGETBUDDY FINANCIAL MANAGER[/bold white]",
            subtitle="[dim white]v1.0.0[/dim white]",
            border_style="blue",
            expand=False,
            padding=(1, 4),
            box=box.ROUNDED
        ))
        option = console.input("\n[bold yellow]Select Option: [/bold yellow]").strip()

        match option:
            case "1":
                login()
            case "2":
                register()
            case "3":
                console.print("\n[bold dim]Session terminated.[/bold dim]")
                break
            case _:
                utils.print_error("Invalid selection.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    start()