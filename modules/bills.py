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


def display_bills(user_id):
    data = load_data()
    user_bills = data.get(str(user_id), {}).get("bills_and_subscriptions", [])

    if not user_bills:
        console.print("[dim white]No recurring liabilities or subscriptions found.[/dim white]")
        return

    columns = [
        {"name": "ID", "justify": "center"},
        {"name": "Payee / Service", "justify": "left"},
        {"name": "Amount", "justify": "right"},
        {"name": "Due Date", "justify": "center"},
        {"name": "Payment Status", "justify": "center"},
    ]

    rows = []
    for idx, b in enumerate(user_bills, 1):
        bill_name = b.get('name') or b.get('item') or 'N/A'
        amount = b.get('amount', 0.0)
        due_date = b.get('due_date', 'N/A')
        status = b.get('status', 'Unpaid')

        status_fmt = "[bold green]PAID[/bold green]" if status == "Paid" else "[bold red]UNPAID[/bold red]"
        rows.append([idx, bill_name, f"₱{amount:,.2f}", due_date, status_fmt])

    utils.render_table("Recurring Obligations & Bills", columns, rows)


def add_bill(user_id):
    utils.print_banner("ADD RECURRING OBLIGATION", "Register Bill or Subscription")
    name = utils.get_item("Payee / Service Name: ")
    amount = utils.get_amount("Amount (PHP): ₱")
    due_date = utils.get_date("Due Date (YYYY-MM-DD): ")

    data = load_data()
    str_user = str(user_id)
    if str_user not in data:
        data[str_user] = {"incomes": [], "expenses": [], "bills_and_subscriptions": [], "budget_plans": {}}

    data[str_user]["bills_and_subscriptions"].append({
        "name": name,
        "amount": amount,
        "due_date": due_date,
        "status": "Unpaid"
    })
    save_data(data)
    utils.print_success("Recurring obligation successfully added.")
    input("\nPress Enter to return...")


def toggle_status(user_id):
    utils.print_banner("UPDATE PAYMENT STATUS", "Toggle Paid / Unpaid Status")
    display_bills(user_id)
    data = load_data()
    user_bills = data.get(str(user_id), {}).get("bills_and_subscriptions", [])

    if not user_bills:
        input("\nPress Enter to return...")
        return

    rec_id = utils.get_record_id("Select Record ID to Toggle: ")
    if rec_id and 1 <= rec_id <= len(user_bills):
        curr = user_bills[rec_id - 1].get("status", "Unpaid")
        new_status = "Unpaid" if curr == "Paid" else "Paid"
        user_bills[rec_id - 1]["status"] = new_status
        save_data(data)
        utils.print_success(f"Payment status updated to '{new_status}'.")
    else:
        utils.print_error("Selected ID was not found.")
    input("\nPress Enter to return...")


def delete_bill(user_id):
    utils.print_banner("REMOVE OBLIGATION", "Delete Bill Entry")
    display_bills(user_id)
    data = load_data()
    user_bills = data.get(str(user_id), {}).get("bills_and_subscriptions", [])

    if not user_bills:
        input("\nPress Enter to return...")
        return

    rec_id = utils.get_record_id("Select Record ID to Remove: ")
    if rec_id and 1 <= rec_id <= len(user_bills):
        if utils.confirm("Confirm deletion of this record"):
            user_bills.pop(rec_id - 1)
            save_data(data)
            utils.print_success("Obligation record removed.")
    else:
        utils.print_error("Selected ID was not found.")
    input("\nPress Enter to return...")


def main(user_id):
    while True:
        utils.print_banner("BILLS & SUBSCRIPTIONS", "Manage Recurring Liabilities")
        display_bills(user_id)

        menu = (
            " [cyan][1][/cyan] Add Obligation\n"
            " [cyan][2][/cyan] Toggle Payment Status\n"
            " [cyan][3][/cyan] Delete Obligation\n"
            " [red][4][/red] Return to Dashboard"
        )
        console.print(Panel(menu, border_style="blue", box=box.ROUNDED, expand=False))
        opt = console.input("\n[bold yellow]Select Option: [/bold yellow]").strip()

        match opt:
            case "1": add_bill(user_id)
            case "2": toggle_status(user_id)
            case "3": delete_bill(user_id)
            case "4": break
            case _:
                utils.print_error("Invalid selection.")
                input("\nPress Enter to try again...")