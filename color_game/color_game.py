import tkinter as tk
from tkinter import ttk
import random
import time

class ColorGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Game")
        self.root.geometry("400x250")

        self.score = 0
        self.rounds = 0
        self.current_color = ""
        self.text_color = ""
        self.playing = False
        self.start_time = 0

        self.score_label = ttk.Label(
            self.root, text="0 / 0", 
            font=('Helvetica', 16))
        self.score_label.pack(pady=10)

        self.timer_label = ttk.Label(
            self.root, text="Time: 0s", 
            font=('Helvetica', 16))
        self.timer_label.pack()

        self.color_label = ttk.Label(
            self.root, text="", 
            font=('Helvetica', 24))
        self.color_label.pack()

        self.input_entry = tk.Entry(
            self.root, font=("Helvetica", 14))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", self.check_color)

        self.start_button = tk.Button(
            self.root, text="Start", 
            command=self.start_game, 
            font=("Helvetica", 14))
        self.start_button.pack()

    def show_color(self):
        color_name = self.random_color()
        self.text_color = self.random_color()
        while color_name == self.text_color:
            self.text_color = self.random_color()
        self.color_label.config(
            text=color_name, 
            foreground=self.text_color)

    def random_color(self):
        colors = [
            "red",
            "green",
            "blue",
            "yellow",
            "purple",
            "orange",
            "pink",
            "brown",
            "gray",
            "black",
        ]
        return random.choice(colors)

    def start_game(self):
        self.playing = True
        self.rounds = 0
        self.score = 0
        self.start_time = time.time()
        self.update_score()
        self.update_timer()
        self.play_round()

    def play_round(self):
        if self.playing and self.rounds < 10:
            self.show_color()
            self.input_entry.delete(0, tk.END)
            self.rounds += 1
        elif self.rounds == 10:
            self.playing = False
            self.current_color = ""
            self.color_label.config(
                text="Game Over", 
                foreground="black")
            self.start_button.config(
                text="Restart")

    def check_color(self, event):
        if self.playing:
            input_color = self.input_entry.get().lower()
            if input_color == self.text_color:
                self.score += 1
            self.update_score()
            self.play_round()

    def update_score(self):
        self.score_label.configure(
            text=f"{self.score} / {self.rounds}")

    def update_timer(self):
        if self.playing:
            elapsed_time = time.time() - self.start_time
            self.timer_label.configure(
                text=f"Time: {int(elapsed_time)}s")
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorGameApp(root)
    root.mainloop()
