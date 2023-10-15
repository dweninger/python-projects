import tkinter as tk
from tkinter import ttk
import requests

class WordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Generator")

        self.large_font = ('Arial', 16)
        self.normal_font = ('Arial', 12)

        self.frame = ttk.Frame(self.root)
        self.frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.length_label = ttk.Label(
            self.frame, text="Word Length:",
            font=self.normal_font)
        self.length_label.pack(pady=10)

        self.length_entry = ttk.Entry(
            self.frame, font=self.normal_font)
        self.length_entry.pack()

        self.amount_label = ttk.Label(
            self.frame, text="Amount of Words:",
            font=self.normal_font)
        self.amount_label.pack(pady=10)

        self.amount_entry = ttk.Entry(
            self.frame, font=self.normal_font)
        self.amount_entry.pack()

        self.generate_button = ttk.Button(
            self.frame,
            text="Generate Words",
            command=self.generate_words)
        self.generate_button.pack(pady=20)

        self.words_label = ttk.Label(
            self.frame, text="", font=self.large_font, 
            wraplength=380, justify="left")
        self.words_label.pack()

        self.copy_button = ttk.Button(
            self.frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard)
        self.copy_button.pack(side="left")

        self.reset_button = ttk.Button(
            self.frame,
            text="Reset",
            command=self.reset)
        self.reset_button.pack(side="left")

        self.reset_button.configure(state="disabled")

    def generate_words(self):
        word_length = self.length_entry.get()
        amount = self.amount_entry.get()

        try:
            word_length = int(word_length)
            amount = int(amount)
        except ValueError:
            return

        if word_length <= 0 or amount <= 0:
            return

        response = requests.get(
            f"https://random-word-api.herokuapp.com/word?number={amount}&length={word_length}")

        if response.status_code == 200:
            words = ", ".join(response.json())
            self.words_label.config(text=words)
            self.reset_button.configure(state="enabled")

    def reset(self):
        self.length_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.words_label.config(text="")
        self.reset_button.configure(state="disabled")

    def copy_to_clipboard(self):
        words = self.words_label.cget("text")
        self.root.clipboard_clear()
        self.root.clipboard_append(words)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGeneratorApp(root)
    root.mainloop()
