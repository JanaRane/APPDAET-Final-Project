import utils
from modules import income

def main(user_id):
    while True:
        utils.clear()
        print("""BudgetBuddy Dashboard\n
        1. Income
        2. Expenses
        3. Bills & Subscriptions
        4. Budget Plans
        5. Reports
        6. Exit\n""")
        option = input("Enter a number: ")

        match option:
            case "1":
                income.main(user_id)
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case "6":
                print("\nLogging out.\n")
                break
            case _:
                print("\nPlease enter a valid option.\n")