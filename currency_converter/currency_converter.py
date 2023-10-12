import tkinter as tk
from tkinter import ttk
from forex_python.converter import CurrencyRates

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.from_currency_var = tk.StringVar()
        self.to_currency_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.result_var = tk.StringVar()

        self.c = CurrencyRates()

        self.create_gui()

    def create_gui(self):
        # Labels
        tk.Label(
            self.root, 
            text="From Currency", 
            font=("Arial", 18)).grid(row=0, column=0)
        tk.Label(
            self.root, 
            text="To Currency", 
            font=("Arial", 18)).grid(row=1, column=0)
        tk.Label(
            self.root, 
            text="Amount", 
            font=("Arial", 18)).grid(row=2, column=0)
        tk.Label(
            self.root, 
            text="Converted Amount", 
            font=("Arial", 18)).grid(row=3, column=0)

        # Dropdown menus for currency selection
        from_currency_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.from_currency_var, 
            values=list(self.c.get_rates("").keys()))
        from_currency_dropdown.grid(row=0, column=1)
        from_currency_dropdown.set('USD')
        from_currency_dropdown.config(
            font=("Arial", 18), state="readonly")

        to_currency_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.to_currency_var, 
            values=list(self.c.get_rates("").keys()))
        to_currency_dropdown.grid(row=1, column=1)
        to_currency_dropdown.set('EUR')
        to_currency_dropdown.config(
            font=("Arial", 18), state="readonly")

        # Entry field for amount
        tk.Entry(
            self.root, 
            textvariable=self.amount_var, 
            font=("Arial", 18)).grid(row=2, column=1)

        # Entry field for converted amount
        tk.Entry(
            self.root, 
            textvariable=self.result_var, 
            state='readonly', 
            font=("Arial", 18)).grid(row=3, column=1)

        # Convert button
        tk.Button(
            self.root, 
            text="Convert", 
            command=self.convert_currency, 
            font=("Arial", 18)).grid(row=4, columnspan=2)

    def convert_currency(self):
        from_currency = self.from_currency_var.get(
        ).upper()
        to_currency = self.to_currency_var.get(
        ).upper()
        amount = float(self.amount_var.get())

        try:
            converted_amount = self.c.convert(
                from_currency, 
                to_currency, 
                amount)
            self.result_var.set(
                f"{amount} {from_currency} = "
                f"{converted_amount:.2f} {to_currency}")
        except Exception as e:
            self.result_var.set("Error: " + str(e))

def main():
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
