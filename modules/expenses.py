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


def display_expenses(user_id):
    data = load_data()
    user_exp = data.get(str(user_id), {}).get("expenses", [])

    if not user_exp:
        console.print("[dim white]No expense records found.[/dim white]")
        return

    columns = [
        {"name": "ID", "justify": "center"},
        {"name": "Category / Description", "justify": "left"},
        {"name": "Amount", "justify": "right"},
        {"name": "Date", "justify": "center"},
    ]

    rows = []
    for idx, e in enumerate(user_exp, 1):
        item_name = e.get('item') or e.get('description') or e.get('source') or 'N/A'
        amount = e.get('amount', 0.0)
        date = e.get('date', 'N/A')

        rows.append([idx, item_name, f"₱{amount:,.2f}", date])

    utils.render_table("Logged Expenses", columns, rows)


def add_expense(user_id):
    utils.print_banner("RECORD EXPENSE", "Log new spending transaction")
    item = utils.get_item("Category / Description: ")
    amount = utils.get_amount("Amount (PHP): ₱")
    date = utils.get_date("Date (YYYY-MM-DD): ")

    data = load_data()
    str_user = str(user_id)
    if str_user not in data:
        data[str_user] = {"incomes": [], "expenses": [], "bills_and_subscriptions": [], "budget_plans": {}}

    data[str_user]["expenses"].append({"item": item, "amount": amount, "date": date})
    save_data(data)
    utils.print_success("Expense transaction successfully recorded.")
    input("\nPress Enter to return...")


def edit_expense(user_id):
    utils.print_banner("UPDATE EXPENSE", "Modify recorded transaction")
    display_expenses(user_id)
    data = load_data()
    user_exp = data.get(str(user_id), {}).get("expenses", [])

    if not user_exp:
        input("\nPress Enter to return...")
        return

    rec_id = utils.get_record_id("Select Record ID to Update: ")
    if rec_id and 1 <= rec_id <= len(user_exp):
        target = user_exp[rec_id - 1]
        console.print(f"\n[dim white]Press Enter to maintain existing values.[/dim white]")

        curr_item = target.get('item') or target.get('description') or target.get('source') or 'N/A'
        curr_amt = target.get('amount', 0.0)
        curr_dt = target.get('date', 'N/A')

        new_item = utils.get_item(f"Description [{curr_item}]: ", allow_blank=True)
        new_amt = utils.get_amount(f"Amount [₱{curr_amt:,.2f}]: ", allow_blank=True)
        new_dt = utils.get_date(f"Date [{curr_dt}]: ", allow_blank=True)

        target['item'] = new_item if new_item else curr_item
        target['amount'] = new_amt if new_amt is not None else curr_amt
        target['date'] = new_dt if new_dt else curr_dt

        save_data(data)
        utils.print_success("Expense record updated.")
    else:
        utils.print_error("Selected ID was not found.")
    input("\nPress Enter to return...")


def delete_expense(user_id):
    utils.print_banner("REMOVE EXPENSE", "Delete recorded transaction")
    display_expenses(user_id)
    data = load_data()
    user_exp = data.get(str(user_id), {}).get("expenses", [])

    if not user_exp:
        input("\nPress Enter to return...")
        return

    rec_id = utils.get_record_id("Select Record ID to Remove: ")
    if rec_id and 1 <= rec_id <= len(user_exp):
        if utils.confirm("Confirm deletion of this record"):
            user_exp.pop(rec_id - 1)
            save_data(data)
            utils.print_success("Expense record removed.")
    else:
        utils.print_error("Selected ID was not found.")
    input("\nPress Enter to return...")


def main(user_id):
    while True:
        utils.print_banner("EXPENSE MANAGEMENT", "Track and Manage Expenditures")
        display_expenses(user_id)

        menu = (
            " [cyan][1][/cyan] Record Expense\n"
            " [cyan][2][/cyan] Update Record\n"
            " [cyan][3][/cyan] Delete Record\n"
            " [red][4][/red] Return to Dashboard"
        )
        console.print(Panel(menu, border_style="blue", box=box.ROUNDED, expand=False))
        opt = console.input("\n[bold yellow]Select Option: [/bold yellow]").strip()

        match opt:
            case "1": add_expense(user_id)
            case "2": edit_expense(user_id)
            case "3": delete_expense(user_id)
            case "4": break
            case _:
                utils.print_error("Invalid selection.")
                input("\nPress Enter to try again...")