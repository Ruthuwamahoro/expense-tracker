import tkinter as tk
import sqlite3
from winotify import Notification, audio

toast = Notification(
    app_id="Expense Tracker",
    title="Expense Alert!",
    msg="Be careful!You are using a lot of money",
    duration="short",
)


# Database Functions
def create_database():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS expenses(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   description TEXT,
                   Amount INTEGER,
                   date DATETIME
    )"""
    )
    conn.commit()
    conn.close()


create_database()


def add_expense(description, amount, date):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses(description, Amount, date) VALUES(?,?,?)",
        (description, amount, date),
    )
    conn.commit()
    conn.close()


def view_expense():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return expenses


def remove_expense(description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE description=?", (description,))
    conn.commit()
    conn.close()


# GUI Functions
def clear_input_fields():
    entry_description.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_date.delete(0, tk.END)


def show_add_expense():
    clear_input_fields()
    entry_description_label.grid(row=1, column=0, sticky="w")
    entry_description.grid(row=1, column=1)
    entry_amount_label.grid(row=2, column=0, sticky="w")
    entry_amount.grid(row=2, column=1)
    entry_date_label.grid(row=3, column=0, sticky="w")
    entry_date.grid(row=3, column=1)
    add_button.grid(row=4, column=0, columnspan=2)


def show_view_expenses():
    clear_input_fields()
    listbox.delete(0, tk.END)
    expenses = view_expense()
    if not expenses:
        listbox.insert(tk.END, "No expenses recorded.")
    else:
        for expense in expenses:
            description, amount, date = expense[1], expense[2], expense[3]
            listbox.insert(
                tk.END,
                f"Description: {description} || Amount: {amount} || Date: {date}",
            )
        listbox.insert(tk.END, "-----------------------------")


def show_remove_expense():
    clear_input_fields()
    entry_description_label.grid(row=1, column=0, sticky="w")
    entry_description.grid(row=1, column=1)
    remove_button.grid(row=2, column=0, columnspan=2)


def on_add_expense():
    description = entry_description.get()
    amount = entry_amount.get()
    date = entry_date.get()
    if description and amount and date:
        add_expense(description, amount, date)
        clear_input_fields()
        show_view_expenses()  # Update the list after adding an expense


def on_remove_expense():
    description = entry_description.get()
    if description:
        remove_expense(description)
        clear_input_fields()
        show_view_expenses()  # Update the list after removing an expense


def calculate_total_expenses():
    expenses = view_expense()
    total = sum(expense[2] for expense in expenses) if expenses else 0
    valueOf_start = int(set_goal_start_up_entry.get())
    valueOf_saving = int(set_goal_saving_entry.get())
    if valueOf_start - total == valueOf_saving:
        total_label.config(text=f"Total Expenses: {total}")
        msg = Notification(
            app_id="Expense Tracker",
            title="Expense Alert!",
            msg="Congratulation!!you have your saving.Don't touch it",
            duration="short",
        )
        msg.set_audio(audio.LoopingCall, loop=True)
        msg.add_actions(label="Click Me", launch="https://www.youtube.com/")
        msg.show()

    elif valueOf_start - total > valueOf_saving:
        total_label.config(text=f"Total Expenses: {total}")
        toast.set_audio(audio.LoopingCall, loop=True)
        toast.add_actions(label="Click Me", launch="https://www.youtube.com/")
        toast.show()
    else:
        total_label.config(text=f"Total Expenses: {total}")
        msg = Notification(
            app_id="Expense Tracker",
            title="Expense Alert!",
            msg="still have your saving",
            duration="short",
        )
        msg.set_audio(audio.LoopingCall, loop=True)
        msg.add_actions(label="Click Me", launch="https://www.youtube.com/")
        msg.show()


# Main GUI
root = tk.Tk()
root.title("Expense Tracker")

# Labels and Entry Widgets
label = tk.Label(
    root, text="Expense Tracker App", font=("Helvetica", 25, "bold"), fg="blue"
)
label.grid(row=0, column=0, columnspan=2)

entry_description_label = tk.Label(root, text="Enter description of your expense: ")
entry_description = tk.Entry(root)
entry_amount_label = tk.Label(root, text="Enter amount: ")
entry_amount = tk.Entry(root)
entry_date_label = tk.Label(root, text="Enter date of your transaction (YYYY-MM-DD): ")
entry_date = tk.Entry(root)


# Buttons for Add, View, and Remove Expenses
def on_add_expense_and_show_view():
    show_add_expense()
    on_add_expense()


def set_goal():
    set_goal_start_up.grid(row=8, column=0, sticky="w")
    set_goal_start_up_entry.grid(row=8, column=1)
    set_goal_saving.grid(row=9, column=0, sticky="w")
    set_goal_saving_entry.grid(row=9, column=1)


set_goal_button = tk.Button(root, text="set your goal", command=set_goal)
set_goal_button.grid(row=7, column=0)
set_goal_start_up = tk.Label(root, text="Amount you have: ")
set_goal_start_up_entry = tk.Entry(root)
set_goal_saving = tk.Label(root, text="Amount you want to save: ")
set_goal_saving_entry = tk.Entry(root)
submit_button = tk.Button(root, text="Submit")


add_expense_button = tk.Button(
    root, text="Add Expense", command=on_add_expense_and_show_view
)
view_expenses_button = tk.Button(root, text="View Expenses", command=show_view_expenses)
remove_expense_button = tk.Button(
    root, text="Remove Expense", command=show_remove_expense
)
total_expenses_button = tk.Button(
    root, text="Total Expenses", command=calculate_total_expenses
)

add_expense_button.grid(row=5, column=0)
view_expenses_button.grid(row=5, column=1)
remove_expense_button.grid(row=5, column=2)
total_expenses_button.grid(row=5, column=3)


# Listbox for displaying expenses
listbox = tk.Listbox(root, width=50)
listbox.grid(row=6, column=0, columnspan=3)

# Add and Remove Buttons
add_button = tk.Button(root, text="Add", command=on_add_expense)
remove_button = tk.Button(root, text="Remove", command=on_remove_expense)
total_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"))
total_label.grid(row=6, column=0, columnspan=3)


root.mainloop()
