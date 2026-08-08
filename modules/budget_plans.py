import json
import os
import utils
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()
DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def set_budget(user_id):
    utils.print_banner("CONFIGURE TARGETS", "Set Financial Goals and Spending Caps")
    data = load_data()
    str_user = str(user_id)

    if str_user not in data:
        data[str_user] = {"incomes": [], "expenses": [], "bills_and_subscriptions": [], "budget_plans": {}}

    inc_target = utils.get_amount("Target Monthly Income: ₱")
    exp_target = utils.get_amount("Maximum Expense Allocation: ₱")
    bill_target = utils.get_amount("Maximum Bill Allocation: ₱")

    data[str_user]["budget_plans"] = {
        "income": inc_target,
        "expenses": exp_target,
        "bills": bill_target
    }

    save_data(data)
    utils.print_success("Financial targets successfully saved.")
    input("\nPress Enter to return...")


def view_budget(user_id):
    utils.print_banner("FINANCIAL TARGETS", "Current Target Allocations")
    data = load_data()
    plans = data.get(str(user_id), {}).get("budget_plans", {"income": 0.0, "expenses": 0.0, "bills": 0.0})

    columns = [
        {"name": "Allocation Category", "justify": "left"},
        {"name": "Target Cap (PHP)", "justify": "right"}
    ]
    rows = [
        ["Target Revenue Goal", f"₱{plans.get('income', 0.0):,.2f}"],
        ["Expense Limit Cap", f"₱{plans.get('expenses', 0.0):,.2f}"],
        ["Recurring Bills Allocation", f"₱{plans.get('bills', 0.0):,.2f}"]
    ]

    utils.render_table("Target Allocations Overview", columns, rows)
    input("\nPress Enter to return...")


def main(user_id):
    while True:
        utils.print_banner("FINANCIAL TARGETS & PLANNING", "Manage Budget Objectives")

        menu = (
            " [cyan][1][/cyan] Configure Targets\n"
            " [cyan][2][/cyan] View Active Targets\n"
            " [red][3][/red] Return to Dashboard"
        )
        console.print(Panel(menu, border_style="blue", box=box.ROUNDED, expand=False))
        opt = console.input("\n[bold yellow]Select Option: [/bold yellow]").strip()

        match opt:
            case "1": set_budget(user_id)
            case "2": view_budget(user_id)
            case "3": break
            case _:
                utils.print_error("Invalid selection.")
                input("\nPress Enter to try again...")