import tkinter as tk

# Create a function to handle button clicks
def button_click(event):
    current = entry.get()
    text = event.widget.cget("text")

    if text == "=":
        try:
            result = eval(current)
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")

    elif text == "C":
        entry.delete(0, tk.END)

    else:
        entry.insert(tk.END, text)

# Create the main window
window = tk.Tk()
window.title("Calculator")

# Create an entry widget for input/output
entry = tk.Entry(window, font=("Helvetica", 20))
entry.grid(row=0, column=0, columnspan=4)

# Define the button labels
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

# Create and place the buttons on the calculator
row_val = 1
col_val = 0

for button_text in buttons:
    button = tk.Button(window, text=button_text, padx=20, pady=20, font=("Helvetica", 20))
    button.grid(row=row_val, column=col_val)
    button.bind("<Button-1>", button_click)

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Start the main loop
window.mainloop()
