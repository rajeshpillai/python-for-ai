import npyscreen
import datetime
import pickle
import os
from pathlib import Path

# File to store expenses
EXPENSE_FILE = "expenses.dat"

# Ensure file exists
if not Path(EXPENSE_FILE).exists():
    with open(EXPENSE_FILE, "wb") as f:
        pickle.dump([], f)


# Expense Model
class Expense:
    def __init__(self, title, amount, date, description):
        self.title = title
        self.amount = amount
        self.date = date
        self.description = description

    def __str__(self):
        return f"{self.title} - ${self.amount} on {self.date}"


# Main App Class
class ExpenseApp(npyscreen.NPSAppManaged):
    def onStart(self):
        # Main screens of the application
        self.addForm("MAIN", MainMenu, name="Expense Tracker")
        self.addForm("ADD", AddExpenseForm, name="Add New Expense")
        self.addForm("EDIT", EditExpenseForm, name="Edit Expense")
        self.addForm("VIEW", ViewExpenseForm, name="View Expense")
        self.addForm("SEARCH", SearchExpenseForm, name="Search Expenses")


# Main Menu
class MainMenu(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.FixedText, value="Expense Tracker", editable=False, color="STANDOUT", rely=1, relx=30)
        self.expense_list = self.add(
            npyscreen.TitleMultiSelect,
            name="Expenses",
            max_height=10,
            scroll_exit=True,
            relx=2,
            rely=3,
        )
        self.add_button = self.add(npyscreen.ButtonPress, name="Add Expense", relx=50, rely=5)
        self.edit_button = self.add(npyscreen.ButtonPress, name="Edit Expense", relx=50, rely=7)
        self.delete_button = self.add(npyscreen.ButtonPress, name="Delete Expense", relx=50, rely=9)
        self.search_button = self.add(npyscreen.ButtonPress, name="Search Expenses", relx=50, rely=11)
        self.refresh_button = self.add(npyscreen.ButtonPress, name="Refresh List", relx=50, rely=13)
        self.quit_button = self.add(npyscreen.ButtonPress, name="Quit", relx=50, rely=15)

        # Assign button actions
        self.add_button.whenPressed = self.add_expense
        self.edit_button.whenPressed = self.edit_expense
        self.delete_button.whenPressed = self.delete_expense
        self.search_button.whenPressed = self.search_expenses
        self.refresh_button.whenPressed = self.refresh_list
        self.quit_button.whenPressed = self.quit_app

        self.refresh_list()

    def add_expense(self):
        self.parentApp.switchForm("ADD")

    def edit_expense(self):
        if self.expense_list.value:
            selected_index = self.expense_list.value[0]
            self.parentApp.getForm("EDIT").load_expense(selected_index)
            self.parentApp.switchForm("EDIT")
        else:
            npyscreen.notify_confirm("No expense selected. Please select an expense to edit.", title="Error")

    def delete_expense(self):
        if self.expense_list.value:
            selected_index = self.expense_list.value[0]
            confirm = npyscreen.notify_yes_no("Are you sure you want to delete this expense?", title="Confirm Delete")
            if confirm:
                self.remove_expense(selected_index)
                npyscreen.notify_confirm("Expense deleted successfully.", title="Success")
                self.refresh_list()
        else:
            npyscreen.notify_confirm("No expense selected. Please select an expense to delete.", title="Error")

    def remove_expense(self, index):
        with open(EXPENSE_FILE, "rb+") as f:
            expenses = pickle.load(f)
            del expenses[index]
            f.seek(0)
            f.truncate()
            pickle.dump(expenses, f)

    def search_expenses(self):
        self.parentApp.switchForm("SEARCH")

    def refresh_list(self):
        self.expense_list.values = self.get_expense_titles()
        self.display()

    def quit_app(self):
        confirm = npyscreen.notify_yes_no("Are you sure you want to quit?", title="Confirm Quit")
        if confirm:
            self.parentApp.setNextForm(None)
            self.parentApp.switchFormNow()

    def get_expense_titles(self):
        with open(EXPENSE_FILE, "rb") as f:
            expenses = pickle.load(f)
        return [str(expense) for expense in expenses]


# Add Expense Form
class AddExpenseForm(npyscreen.ActionForm):
    def create(self):
        self.title = self.add(npyscreen.TitleText, name="Title:")
        self.amount = self.add(npyscreen.TitleText, name="Amount:")
        self.date = self.add(npyscreen.TitleDateCombo, name="Date:")
        self.description = self.add(npyscreen.TitleText, name="Description:")

    def on_ok(self):
        title = self.title.value
        amount = float(self.amount.value)
        date = self.date.value.strftime("%Y-%m-%d")
        description = self.description.value

        new_expense = Expense(title, amount, date, description)
        with open(EXPENSE_FILE, "rb+") as f:
            expenses = pickle.load(f)
            expenses.append(new_expense)
            f.seek(0)
            pickle.dump(expenses, f)

        npyscreen.notify_confirm("Expense Added Successfully!", title="Success")
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


# Edit Expense Form
class EditExpenseForm(npyscreen.ActionForm):
    def create(self):
        self.title = self.add(npyscreen.TitleText, name="Title:")
        self.amount = self.add(npyscreen.TitleText, name="Amount:")
        self.date = self.add(npyscreen.TitleDateCombo, name="Date:")
        self.description = self.add(npyscreen.TitleText, name="Description:")
        self.index = None

    def load_expense(self, index):
        self.index = index
        with open(EXPENSE_FILE, "rb") as f:
            expenses = pickle.load(f)
            expense = expenses[index]
        self.title.value = expense.title
        self.amount.value = str(expense.amount)
        self.date.value = datetime.datetime.strptime(expense.date, "%Y-%m-%d")
        self.description.value = expense.description

    def on_ok(self):
        with open(EXPENSE_FILE, "rb+") as f:
            expenses = pickle.load(f)
            expenses[self.index] = Expense(
                title=self.title.value,
                amount=float(self.amount.value),
                date=self.date.value.strftime("%Y-%m-%d"),
                description=self.description.value,
            )
            f.seek(0)
            f.truncate()
            pickle.dump(expenses, f)

        npyscreen.notify_confirm("Expense Edited Successfully!", title="Success")
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


# View Expense Form
class ViewExpenseForm(npyscreen.ActionForm):
    def create(self):
        self.expense_details = self.add(npyscreen.MultiLineEdit, editable=False)

    def load_expense(self, index):
        with open(EXPENSE_FILE, "rb") as f:
            expenses = pickle.load(f)
        self.expense_details.value = (
            f"Title: {expenses[index].title}\n"
            f"Amount: ${expenses[index].amount}\n"
            f"Date: {expenses[index].date}\n"
            f"Description: {expenses[index].description}"
        )
        self.display()

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


# Search Expenses Form
class SearchExpenseForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.FixedText, value="Search Expenses by Date", editable=False, relx=15)
        self.year = self.add(npyscreen.TitleText, name="Year:")
        self.month = self.add(npyscreen.TitleText, name="Month:")
        self.week = self.add(npyscreen.TitleText, name="Week (1-52):")
        self.results = self.add(npyscreen.MultiLineEdit, editable=False, max_height=10, relx=5)

    def on_ok(self):
        year = self.year.value
        month = self.month.value
        week = self.week.value

        with open(EXPENSE_FILE, "rb") as f:
            expenses = pickle.load(f)

        filtered_expenses = []
        for expense in expenses:
            expense_date = datetime.datetime.strptime(expense.date, "%Y-%m-%d")
            if (year and expense_date.year == int(year)) or \
               (month and expense_date.month == int(month)) or \
               (week and expense_date.isocalendar()[1] == int(week)):
                filtered_expenses.append(str(expense))

        self.results.value = "\n".join(filtered_expenses) or "No expenses found."
        self.display()

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


# Run the App
if __name__ == "__main__":
    app = ExpenseApp()
    app.run()
