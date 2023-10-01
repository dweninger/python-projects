import tkinter as tk

def convert():
    input_value = entry.get()
    try:
        if radio_var.get() == 1:  # Decimal to Binary
            result = bin(int(input_value))[2:]
        elif radio_var.get() == 2:  # Binary to Decimal
            result = str(int(input_value, 2))
        elif radio_var.get() == 3:  # Decimal to Hexadecimal
            result = hex(int(input_value))[2:].upper()
        elif radio_var.get() == 4:  # Hexadecimal to Decimal
            result = str(int(input_value, 16))
        output.config(text=result)
    except ValueError:
        output.config(text="Invalid input")

# Create the main window
root = tk.Tk()
root.title("Number Converter")

# Create input label and entry
label = tk.Label(root, text="Enter a number:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# Create radio buttons for conversion options
radio_var = tk.IntVar()
decimal_to_binary = tk.Radiobutton(
    root, 
    text="Decimal to Binary", 
    variable=radio_var, 
    value=1)
binary_to_decimal = tk.Radiobutton(
    root, 
    text="Binary to Decimal", 
    variable=radio_var, 
    value=2)
decimal_to_hex = tk.Radiobutton(root, 
    text="Decimal to Hexadecimal",
    variable=radio_var, 
    value=3)
hex_to_decimal = tk.Radiobutton(
    root, 
    text="Hexadecimal to Decimal", 
    variable=radio_var, 
    value=4)

decimal_to_binary.pack()
binary_to_decimal.pack()
decimal_to_hex.pack()
hex_to_decimal.pack()

# Create conversion button
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.pack()

# Create a label to display the result
output = tk.Label(root, text="")
output.pack()

# Run the main loop
root.mainloop()
