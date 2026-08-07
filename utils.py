import os
from datetime import datetime

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_record_id(prompt):
    while True:
        value = input(prompt).strip()
        if value == '':
            return None

        try:
            id = int(value)
            return id
        except ValueError:
            print("\nError: Invalid ID")

def get_item(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == '':
            return None

        if value:
            return value

        print("\nError: Invalid input\n")

def get_amount(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == '':
            return None

        try:
            amount = float(value)
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print("\nError: Invalid amount\n")

def get_date(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == '':
            return None

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("\nError: Invalid date\n")

def confirm(prompt):
    while True:
        option = input(f"\n{prompt}? (Y/N): ").strip().upper()
        if option in ("Y", "YES"):
            return True
        elif option in ("N", "NO"):
            return False
        else:
            print("\nInvalid option. Please try again.")