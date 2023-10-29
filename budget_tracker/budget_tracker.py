import tkinter as tk

# Add an income or expense
def add_transaction():
    global balance
    description = description_entry.get()
    amount = float(amount_entry.get())
    
    if transaction_type.get() == "Income":
        balance += amount
    else:
        balance -= amount

    balance_label.config(
        text=f"Balance: ${balance:.2f}")
    
    transaction_history.insert(
        "end", f"{transaction_type.get()}: "
        f"{description} - ${amount:.2f}\n")
    
    # Clear input fields
    description_entry.delete(0, "end")
    amount_entry.delete(0, "end")

# Create main window
window = tk.Tk()
window.title("Budget Tracker")

font = ('Helvetica', 12)

transaction_type = tk.StringVar(value="Income")

income_radio = tk.Radiobutton(
    window, text="Income", variable=transaction_type, 
    value="Income", font=font)
expense_radio = tk.Radiobutton(
    window, text="Expense", variable=transaction_type, 
    value="Expense", font=font)

description_label = tk.Label(
    window, text="Description:", font=font)
description_entry = tk.Entry(window, font=font)

amount_label = tk.Label(
    window, text="Amount ($):", font=font)
amount_entry = tk.Entry(window, font=font)

add_button = tk.Button(
    window, text="Add Transaction", 
    command=add_transaction, font=font)

balance_label = tk.Label(
    window, text="Balance: $0.00", font=font)

transaction_history = tk.Text(
    window, height=10, width=40, font=font)

income_radio.grid(row=0, column=0)
expense_radio.grid(row=0, column=1)

description_label.grid(row=1, column=0)
description_entry.grid(row=1, column=1)

amount_label.grid(row=2, column=0)
amount_entry.grid(row=2, column=1)

add_button.grid(row=3, column=0, columnspan=2)

balance_label.grid(row=4, column=0, columnspan=2)

transaction_history.grid(row=5, column=0, columnspan=2)

# Initialize balance
balance = 0.0

window.mainloop()
