import tkinter as tk
from tkinter import ttk
import random
import time

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Test")
        self.root.geometry("500x300")
        self.root.configure(bg="lightblue")

        self.instruction_label = ttk.Label(
            self.root, text="Type the text below:", 
            font=("Helvetica", 16, "bold"),
            background="lightblue")
        self.instruction_label.pack(pady=10)

        self.phrases = [
            "The quick brown fox jumps over the lazy dog.",
            "Python is a versatile programming language.",
            "Hello, world! This is a typing test.",
            "Programming is fun and challenging.",
        ]

        self.current_phrase = ""
        self.text_label = ttk.Label(
            self.root, text="", 
            font=('Helvetica', 16), wraplength=480, 
            background="lightblue")
        self.text_label.pack()

        self.entry = ttk.Entry(
            self.root, font=('Helvetica', 16))
        self.entry.pack(pady=10)
        self.entry.bind("<Key>", self.start_timer)
        self.entry.bind("<Return>", self.check_input)

        self.result_label = ttk.Label(
            self.root, text="", 
            font=('Helvetica', 16), 
            background="lightblue")
        self.result_label.pack()

        self.typing_started = False
        self.start_time = 0
        self.select_random_phrase()

        self.start_over_button = ttk.Button(
            self.root, text="Start Over", 
            command=self.start_over, 
            style="Fun.TButton")
        self.start_over_button.pack(pady=10)

        self.style = ttk.Style()
        self.style.configure(
            "Fun.TButton", font=('Helvetica', 14), 
            background="green", foreground="black")
        self.style.map(
            "Fun.TButton", 
            background=[("active", "blue")])

    def select_random_phrase(self):
        self.current_phrase = random.choice(self.phrases)
        self.text_label.config(text=self.current_phrase)

    def start_timer(self, event):
        if not self.typing_started:
            self.typing_started = True
            self.start_time = time.time()

    def check_input(self, event):
        if not self.typing_started:
            return

        input_text = self.entry.get()
        errors = self.calculate_errors(
            self.current_phrase, input_text)
        elapsed_time = time.time() - self.start_time
        wpm = self.calculate_wpm(elapsed_time, input_text)

        self.result_label.config(
            text=f"WPM: {wpm}, Errors: {errors}")

    def calculate_errors(self, phrase, input_text):
        errors = 0
        for i in range(min(len(phrase), len(input_text))):
            if phrase[i] != input_text[i]:
                errors += 1
        return errors

    def calculate_wpm(self, elapsed_time, text):
        words = text.split()
        num_words = len(words)
        minutes = elapsed_time / 60
        wpm = int(num_words / minutes)
        return wpm

    def start_over(self):
        self.select_random_phrase()
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.typing_started = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
