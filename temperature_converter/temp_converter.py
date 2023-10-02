import tkinter as tk
from tkinter import messagebox

# convert temperature
def convert_temperature():
    try:
        temperature = float(temperature_entry.get())
        if conversion_type.get() == "Fahrenheit to Celsius":
            converted_temperature = (temperature - 32) * 5/9
            result_label.config(
                text=f"{temperature}°F is "
                f"{converted_temperature:.2f}°C")
        else:
            converted_temperature = (temperature * 9/5) + 32
            result_label.config(
                text=f"{temperature}°C is "
                f"{converted_temperature:.2f}°F")
    except ValueError:
        messagebox.showwarning("Warning", 
            "Please enter a valid temperature.")

# main window
root = tk.Tk()
root.title("Temperature Converter")
root.geometry("400x200")

# label and entry for temperature
temperature_label = tk.Label(
    root, 
    text="Enter Temperature:", 
    font=("Helvetica", 16))
temperature_label.pack()
temperature_entry = tk.Entry(
    root, 
    font=("Helvetica", 16))
temperature_entry.pack()

# variable to track the conversion type
conversion_type = tk.StringVar()
conversion_type.set("Fahrenheit to Celsius")

# radio buttons
f_to_c_radio = tk.Radiobutton(
    root, 
    text="Fahrenheit to Celsius", 
    font=("Helvetica", 16), 
    variable=conversion_type, 
    value="Fahrenheit to Celsius")
c_to_f_radio = tk.Radiobutton(
    root, 
    text="Celsius to Fahrenheit", 
    font=("Helvetica", 16), 
    variable=conversion_type, 
    value="Celsius to Fahrenheit")
f_to_c_radio.pack()
c_to_f_radio.pack()

# button to perform the conversion
convert_button = tk.Button(
    root, 
    text="Convert", 
    font=("Helvetica", 16), 
    command=convert_temperature)
convert_button.pack()

# label to display the result
result_label = tk.Label(
    root, 
    text="", font=("Helvetica", 16))
result_label.pack()

# run the main loop
root.mainloop()
