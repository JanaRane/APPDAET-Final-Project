import os
import json
import hashlib
import main
import utils

USERS_FILE = "users.json"
DATA_FILE = "data.json"

if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
    with open(USERS_FILE, "w") as f:
        json.dump({"users": []}, f, indent=4)

if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
    with open(DATA_FILE, "w") as f:
        json.dump({}, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    while True:
        utils.clear()
        print("""BudgetBuddy\n
        1. Login
        2. Register
        3. Close Program\n""")

        option = input("Enter a number: ")

        match option:
            case "1":
                login()
            case "2":
                register()
            case "3":
                print("\nThank you for using BudgetBuddy!")
                print("Closing Program...")
                break
            case _:
                print("\nPlease enter a valid option.\n")

def register():
    utils.clear()
    print("\nRegister a new account\n")
    username = input("Enter your username: ").strip()

    if not username:
        print("\nPlease enter a valid username.\n")
        return

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    for user in users["users"]:
        if user["username"] == username:
            print("\nUsername already exists.\n")
            return

    password = input("Enter your password: ")

    if not password:
        print("\nPlease enter a password.\n")
        return

    hashed_password = hash_password(password)

    if users["users"]:
        next_id = max(user["id"] for user in users["users"]) + 1
    else:
        next_id = 1

    users["users"].append({
        "id": next_id,
        "username": username,
        "password": hashed_password,
    })

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    data[str(next_id)] = {
        "incomes": [],
        "expenses": [],
        "bills_and_subscriptions": [],
        "budget_plans": []
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("\nYou have successfully registered to BudgetBuddy!\n")
    main.main(next_id)

def login():
    utils.clear()
    print("\nLogin to BudgetBuddy\n")
    username = input("Enter your username: ").strip()
    if not username:
        print("\nPlease enter a valid username.\n")
        return

    password = input("Enter your password: ")
    if not password:
        print("\nPlease enter a password.\n")
        return

    hashed_password = hash_password(password)

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    for user in users["users"]:
        if (
            user["username"] == username and
            user["password"] == hashed_password
        ):
            print(f"\nWelcome, {username}!\n")
            main.main(user["id"])
            return True

    print("\nInvalid username or password.\n")
    return False

if __name__ == "__main__":
    login_page()