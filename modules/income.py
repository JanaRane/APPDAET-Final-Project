import json
import utils
from rich.console import Console
from rich.table import Table

DATA_FILE = "./data.json"

def main(user_id):
    while True:
        utils.clear()
        print("""Income\n
        1. Add new income
        2. Edit income
        3. Delete income
        4. List all incomes
        5. Back to dashboard\n""")
        option = input("Enter a number: ")

        match option:
            case "1":
                add_income(user_id)
            case "2":
                edit_income(user_id)
            case "3":
                delete_income(user_id)
            case "4":
                list_incomes(user_id)
            case "5":
                break
            case _:
                print("\nPlease enter a valid option.\n")

def display_table(user_id):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    incomes = data[str(user_id)]["incomes"]

    if not incomes:
        print("\nNo records found.\n")
        return

    t = Table(title="\nIncome Records")

    t.add_column("ID")
    t.add_column("Source")
    t.add_column("Amount")
    t.add_column("Date")

    for income in incomes:
        t.add_row(str(income["id"]), income["source"], f"₱{income["amount"]:.2F}", income["date"])

    c = Console()
    c.print(t)

def add_income(user_id):
    utils.clear()
    print("\nAdd new income\n")
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    uid = str(user_id)
    incomes = data[uid]["incomes"]

    source = utils.get_item("Source: ")
    amount = utils.get_amount("Amount: ₱")
    date = utils.get_date("Date (YYYY-MM-DD): ")

    if utils.confirm("Save"):
        next_id = 1 if not incomes else max(i["id"] for i in incomes) + 1

        incomes.append({
            "id": next_id,
            "source": source,
            "amount": amount,
            "date": date
        })

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("\nIncome added successfully!\n")

def edit_income(user_id):
    utils.clear()
    print("\nEdit income")

    display_table(user_id)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    incomes = data[str(user_id)]["incomes"]

    record_id = utils.get_record_id("\nEnter the ID to edit the record: ")

    if record_id is None:
        return

    for income in incomes:
        if income["id"] == record_id:
            print("\nLeave the field blank to keep its current value.\n")
            source = utils.get_item(f"Source [{income["source"]}]: ", allow_blank=True)
            if source is not None:
                income["source"] = source

            amount = utils.get_amount(f"Amount [₱{income["amount"]:.2F}]: ", allow_blank=True)
            if amount is not None:
                income["amount"] = amount

            date = utils.get_date(f"Date [{income["date"]}]: ", allow_blank=True)
            if date is not None:
                income["date"] = date

            if utils.confirm("Save"):
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f, indent=4)

                print("\nRecord edited successfully!\n")
                return
            else:
                return

    print("\nRecord not found.\n")

def delete_income(user_id):
    utils.clear()
    print("\nDelete income")

    display_table(user_id)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    incomes = data[str(user_id)]["incomes"]

    record_id = utils.get_record_id("\nEnter the ID to delete the record: ")

    if record_id is None:
        return

    for income in incomes:
        if income["id"] == record_id:
            if utils.confirm("Delete"):
                incomes.remove(income)
                with open(DATA_FILE, "w") as f:
                    json.dump(data, f, indent=4)

                print("\nRecord deleted successfully!\n")
                return
            else:
                return

    print("\nRecord not found.\n")

def list_incomes(user_id):
    utils.clear()
    display_table(user_id)
    input("\nPress enter to return...\n")