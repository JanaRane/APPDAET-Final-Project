import utils
from rich.console import Console
from rich.panel import Panel
from rich import box
from modules import income, expenses, bills, budget_plans, reports

console = Console()


def main(user_id):
    while True:
        utils.clear()
        dashboard_menu = (
            " [cyan][1][/cyan] Income Management\n"
            " [cyan][2][/cyan] Expense Tracker\n"
            " [cyan][3][/cyan] Bills & Subscriptions\n"
            " [cyan][4][/cyan] Financial Targets & Planning\n"
            " [cyan][5][/cyan] Generate Account Statement\n"
            " [red][6][/red] Logout"
        )
        console.print(Panel(
            dashboard_menu,
            title=f"[bold white]MAIN DASHBOARD // ACCOUNT #{int(user_id):04d}[/bold white]",
            border_style="blue",
            expand=False,
            padding=(1, 4),
            box=box.ROUNDED
        ))
        option = console.input("\n[bold yellow]Select Option: [/bold yellow]").strip()

        match option:
            case "1":
                income.main(user_id)
            case "2":
                expenses.main(user_id)
            case "3":
                bills.main(user_id)
            case "4":
                budget_plans.main(user_id)
            case "5":
                reports.main(user_id)
            case "6":
                break
            case _:
                utils.print_error("Invalid selection.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    import login_page
    login_page.start()