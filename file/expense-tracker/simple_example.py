import struct
import os

# Define file and record format
EXPENSE_FILE = "exp_txt.dat"
RECORD_FORMAT = "50s10s10s100s"  # Title, Amount, Date, Description
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)


# Utility Functions
def pack_expense(title, amount, date, description):
    """Pack an expense into binary format."""
    return struct.pack(RECORD_FORMAT, title.encode(), amount.encode(), date.encode(), description.encode())


def unpack_expense(record):
    """Unpack a binary record into readable format."""
    title, amount, date, description = struct.unpack(RECORD_FORMAT, record)
    return title.decode().strip(), amount.decode().strip(), date.decode().strip(), description.decode().strip()


# Functions for CRUD Operations
def add_expense():
    """Add a new expense."""
    title = input("Enter title (max 50 chars): ").ljust(50)
    amount = input("Enter amount (max 10 chars): ").ljust(10)
    date = input("Enter date (YYYY-MM-DD): ").ljust(10)
    description = input("Enter description (max 100 chars): ").ljust(100)
    with open(EXPENSE_FILE, "ab") as f:
        f.write(pack_expense(title, amount, date, description))
    print("Expense added successfully!")


def list_expenses():
    """List all expenses."""
    if not os.path.exists(EXPENSE_FILE) or os.path.getsize(EXPENSE_FILE) == 0:
        print("No expenses found.")
        return

    with open(EXPENSE_FILE, "rb") as f:
        print(f"\n{'ID':<5}{'Title':<50}{'Amount':<10}{'Date':<10}{'Description':<100}")
        print("-" * 180)
        index = 0
        while chunk := f.read(RECORD_SIZE):
            title, amount, date, description = unpack_expense(chunk)
            print(f"{index:<5}{title:<50}{amount:<10}{date:<10}{description:<100}")
            index += 1


def edit_expense():
    """Edit an expense."""
    list_expenses()
    if not os.path.exists(EXPENSE_FILE) or os.path.getsize(EXPENSE_FILE) == 0:
        return

    expense_id = int(input("\nEnter the ID of the expense to edit: "))
    with open(EXPENSE_FILE, "r+b") as f:
        f.seek(expense_id * RECORD_SIZE)
        record = f.read(RECORD_SIZE)
        if not record:
            print("Invalid ID!")
            return
        title, amount, date, description = unpack_expense(record)
        print(f"Editing Expense: {title.strip()} - {amount.strip()} - {date.strip()} - {description.strip()}")
        new_title = input(f"Enter new title (leave blank to keep '{title.strip()}'): ").ljust(50) or title
        new_amount = input(f"Enter new amount (leave blank to keep '{amount.strip()}'): ").ljust(10) or amount
        new_date = input(f"Enter new date (leave blank to keep '{date.strip()}'): ").ljust(10) or date
        new_description = input(f"Enter new description (leave blank to keep '{description.strip()}'): ").ljust(100) or description
        f.seek(expense_id * RECORD_SIZE)
        f.write(pack_expense(new_title, new_amount, new_date, new_description))
        print("Expense updated successfully!")


def delete_expense():
    """Delete an expense."""
    list_expenses()
    if not os.path.exists(EXPENSE_FILE) or os.path.getsize(EXPENSE_FILE) == 0:
        return

    expense_id = int(input("\nEnter the ID of the expense to delete: "))
    with open(EXPENSE_FILE, "rb") as f:
        records = f.readlines()
    if expense_id < 0 or expense_id >= len(records):
        print("Invalid ID!")
        return
    del records[expense_id]
    with open(EXPENSE_FILE, "wb") as f:
        f.writelines(records)
    print("Expense deleted successfully!")


# Main Menu
def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. List Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            edit_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
