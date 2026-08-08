import json
import os
from datetime import datetime
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


def main(user_id):
    utils.clear()
    data = load_data().get(str(user_id), {})

    incomes = data.get("incomes", [])
    expenses = data.get("expenses", [])
    bills = data.get("bills_and_subscriptions", [])
    plans = data.get("budget_plans", {"income": 0.0, "expenses": 0.0, "bills": 0.0})

    # Calculations with defensive lookups
    tot_act_inc = sum(i.get("amount", 0.0) for i in incomes)
    tot_act_exp = sum(e.get("amount", 0.0) for e in expenses)
    tot_act_bill = sum(b.get("amount", 0.0) for b in bills if b.get("status") == "Paid")

    tot_tgt_inc = plans.get("income", 0.0)
    tot_tgt_exp = plans.get("expenses", 0.0)
    tot_tgt_bill = plans.get("bills", 0.0)

    tot_budget = tot_tgt_inc - tot_tgt_exp - tot_tgt_bill
    tot_actual = tot_act_inc - tot_act_exp - tot_act_bill
    tot_diff = tot_actual - tot_budget

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    if tot_diff > 0:
        diff_status = f"[bold green]+₱{tot_diff:,.2f} (SURPLUS)[/bold green]"
        txt_diff_status = f"+₱{tot_diff:,.2f} (SURPLUS)"
    elif tot_diff < 0:
        diff_status = f"[bold red]-₱{abs(tot_diff):,.2f} (DEFICIT)[/bold red]"
        txt_diff_status = f"-₱{abs(tot_diff):,.2f} (DEFICIT)"
    else:
        diff_status = f"[bold yellow]₱{tot_diff:,.2f} (BALANCED)[/bold yellow]"
        txt_diff_status = f"₱{tot_diff:,.2f} (BALANCED)"

    statement_text = (
        "[bold white]BUDGETBUDDY FINANCIAL MANAGEMENT SYSTEM[/bold white]\n"
        "[bold white]MONTHLY FINANCIAL SUMMARY STATEMENT[/bold white]\n"
        "[dim white]" + "─" * 52 + "[/dim white]\n"
        f" [bold white]STATEMENT DATE:[/bold white] {date_str}   [bold white]TIME:[/bold white] {time_str}\n"
        f" [bold white]ACCOUNT ID:[/bold white] #{int(user_id):04d}            [bold white]STATUS:[/bold white] [green]VERIFIED[/green]\n"
        "[dim white]" + "─" * 52 + "[/dim white]\n\n"

        " [bold cyan]I. REVENUE ANALYSIS[/bold cyan]\n"
        f"   Target Goal .................... ₱{tot_tgt_inc:>12,.2f}\n"
        f"   Actual Earned .................. [bold green]₱{tot_act_inc:>12,.2f}[/bold green]\n\n"

        " [bold cyan]II. OPERATING EXPENDITURES[/bold cyan]\n"
        f"   Target Cap ..................... ₱{tot_tgt_exp:>12,.2f}\n"
        f"   Actual Spent ................... [bold red]₱{tot_act_exp:>12,.2f}[/bold red]\n\n"

        " [bold cyan]III. RECURRING OBLIGATIONS[/bold cyan]\n"
        f"   Target Allocation .............. ₱{tot_tgt_bill:>12,.2f}\n"
        f"   Actual Paid .................... [bold yellow]₱{tot_act_bill:>12,.2f}[/bold yellow]\n"
        "[dim white]" + "─" * 52 + "[/dim white]\n\n"

        " [bold cyan]IV. CASH FLOW OVERVIEW[/bold cyan]\n"
        f"   Planned Net Cash Flow .......... ₱{tot_budget:>12,.2f}\n"
        f"   Actual Net Reserve ............. ₱{tot_actual:>12,.2f}\n"
        "[dim white]" + "═" * 52 + "[/dim white]\n"
        f" [bold white]VARIANCE ANALYSIS:[/bold white] {diff_status}\n"
        "[dim white]" + "═" * 52 + "[/dim white]\n\n"
        f" [dim white]REFERENCE CODE: REF-BB-{date_str.replace('-', '')}-{user_id}[/dim white]\n"
        " [dim white]OFFICIAL ACCOUNT STATEMENT — CONFIDENTIAL[/dim white]"
    )

    console.print(
        Panel(
            statement_text,
            title="[bold white]ACCOUNT STATEMENT[/bold white]",
            subtitle="[dim white]BudgetBuddy Financial Core[/dim white]",
            border_style="blue",
            expand=False,
            padding=(1, 3),
            box=box.ROUNDED
        )
    )

    if utils.confirm("Export statement to a text file"):
        filename = f"statement_account_{user_id}_{date_str}.txt"
        plain_statement = (
            "=====================================================\n"
            "      BUDGETBUDDY FINANCIAL MANAGEMENT SYSTEM        \n"
            "        MONTHLY FINANCIAL SUMMARY STATEMENT          \n"
            "-----------------------------------------------------\n"
            f"STATEMENT DATE: {date_str}   TIME: {time_str}\n"
            f"ACCOUNT ID: #{int(user_id):04d}            STATUS: VERIFIED\n"
            "-----------------------------------------------------\n\n"
            "I. REVENUE ANALYSIS\n"
            f"   Target Goal .................... ₱{tot_tgt_inc:>12,.2f}\n"
            f"   Actual Earned .................. ₱{tot_act_inc:>12,.2f}\n\n"
            "II. OPERATING EXPENDITURES\n"
            f"   Target Cap ..................... ₱{tot_tgt_exp:>12,.2f}\n"
            f"   Actual Spent ................... ₱{tot_act_exp:>12,.2f}\n\n"
            "III. RECURRING OBLIGATIONS\n"
            f"   Target Allocation .............. ₱{tot_tgt_bill:>12,.2f}\n"
            f"   Actual Paid .................... ₱{tot_act_bill:>12,.2f}\n"
            "-----------------------------------------------------\n\n"
            "IV. CASH FLOW OVERVIEW\n"
            f"   Planned Net Cash Flow .......... ₱{tot_budget:>12,.2f}\n"
            f"   Actual Net Reserve ............. ₱{tot_actual:>12,.2f}\n"
            "=====================================================\n"
            f"VARIANCE ANALYSIS: {txt_diff_status}\n"
            "=====================================================\n"
            f"REFERENCE CODE: REF-BB-{date_str.replace('-', '')}-{user_id}\n"
            "OFFICIAL ACCOUNT STATEMENT — CONFIDENTIAL\n"
            "=====================================================\n"
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(plain_statement)
        utils.print_success(f"Statement exported to '{filename}'.")

    input("\nPress Enter to return...")


if __name__ == "__main__":
    main("1")