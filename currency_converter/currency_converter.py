import tkinter as tk
from tkinter import ttk

# Define fixed conversion rates 
conversion_rates = {
    'USD': {'EUR': 0.85, 'GBP': 0.73, 
            'JPY': 110.16, 'CAD': 1.26},
    'EUR': {'USD': 1.18, 'GBP': 0.87, 
            'JPY': 129.54, 'CAD': 1.49},
    'GBP': {'USD': 1.37, 'EUR': 1.15, 
            'JPY': 150.75, 'CAD': 1.71},
    'JPY': {'USD': 0.0091, 'EUR': 0.0077, 
            'GBP': 0.0066, 'CAD': 0.0082},
    'CAD': {'USD': 0.79, 'EUR': 0.67, 
            'GBP': 0.59, 'JPY': 122.41}
}

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        self.from_currency_var = tk.StringVar()
        self.to_currency_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.result_var = tk.StringVar()

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
            values=list(conversion_rates.keys()))
        from_currency_dropdown.grid(row=0, column=1)
        from_currency_dropdown.set('USD')
        from_currency_dropdown.config(
            font=("Arial", 18), state="readonly")

        to_currency_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.to_currency_var, 
            values=list(conversion_rates.keys()))
        to_currency_dropdown.grid(row=1, column=1)
        to_currency_dropdown.set('EUR')
        to_currency_dropdown.config(
            font=("Arial", 18), state="readonly")

        # Entry field for amount
        tk.Entry(
            self.root, 
            textvariable=self.amount_var, 
            font=("Arial", 18)).grid(row=2, column=1)

        # Entry field for converted amount (readonly)
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
            converted_amount = amount * conversion_rates[
                from_currency][to_currency]
            self.result_var.set(
                f"{amount} {from_currency} = "
                f"{converted_amount:.2f} {to_currency}")
        except KeyError:
            self.result_var.set("Invalid currency code")

def main():
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
