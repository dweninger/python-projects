import tkinter as tk
import random
import time

class ColorMemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Memory Game")
        self.root.configure(bg="#f2f2f2")  # Set the background color

        self.colors = ["red", "green", "blue", "yellow"]
        self.lighter_colors = {
            "red": "#FF9999",  # Light Red
            "green": "#99FF99",  # Light Green
            "blue": "#9999FF",  # Light Blue
            "yellow": "#FFFFFF",  # Light Yellow
        }
        self.sequence = []
        self.player_sequence = []
        self.round = 1
        self.message_label = tk.Label(root, text="Press Start to play", font=("Helvetica", 24), bg="#f2f2f2")
        self.message_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.color_buttons = []
        for i, color in enumerate(self.colors):
            button = tk.Button(
                root,
                text=color.upper(),
                width=15,
                height=7,
                bg=color,
                activebackground=self.lighter_colors[color],
                font=("Helvetica", 20),
                command=lambda c=color: self.check_sequence(c)
            )
            self.color_buttons.append(button)
            button.grid(row=i // 2 + 1, column=i % 2, padx=10, pady=10)
            button.config(state=tk.DISABLED)

        self.start_button = tk.Button(
            root,
            text="Start",
            font=("Helvetica", 20),
            command=self.start_game,
            bg="#008CBA",  # Set a nice background color
            fg="white"  # Set the text color to white
        )
        self.start_button.grid(row=3, column=0, columnspan=2)

        self.current_sequence_index = 0

    def start_game(self):
        self.sequence = []
        self.player_sequence = []
        self.round = 1
        self.message_label.config(text=f"Round {self.round}: Watch this sequence", font=("Helvetica", 24))
        self.disable_color_buttons()
        self.root.update()
        time.sleep(0.2)  # Wait for 1 second before displaying the sequence
        self.root.after(1000, self.next_round)

    def next_round(self):
        self.message_label.config(text=f"Round {self.round}: Watch this sequence", font=("Helvetica", 24))
        self.disable_color_buttons()
        self.sequence.append(random.choice(self.colors))
        self.display_sequence(0)

    def display_sequence(self, index):
        if index < len(self.sequence):
            color = self.sequence[index]
            self.flash_color(color)
            self.root.after(800, self.restore_color, color)
            self.root.after(600, self.display_sequence, index + 1)
        else:
            self.message_label.config(text="Your turn: Repeat the sequence", font=("Helvetica", 24))
            self.current_sequence_index = 0
            self.enable_color_buttons()

    def flash_color(self, color):
        button = self.color_buttons[self.colors.index(color)]
        button.config(bg=self.lighter_colors[color])
        self.root.update()
        time.sleep(0.5)  # Flash for 0.8 seconds
        self.restore_color(color)

    def restore_color(self, color):
        button = self.color_buttons[self.colors.index(color)]
        button.config(bg=color)
        self.root.update()

    def enable_color_buttons(self):
        for button in self.color_buttons:
            button.config(state=tk.NORMAL)

    def check_sequence(self, color):
        if color == self.sequence[self.current_sequence_index]:
            self.current_sequence_index += 1
            if self.current_sequence_index == len(self.sequence):
                if self.current_sequence_index == self.round:
                    self.round += 1
                    self.disable_color_buttons()
                    self.message_label.config(text=f"Correct! Watch this sequence", font=("Helvetica", 24))
                    self.root.after(800, self.next_round)
        else:
            self.end_game()

    def disable_color_buttons(self):
        for button in self.color_buttons:
            button.config(state=tk.DISABLED)

    def end_game(self):
        score = len(self.sequence) - 1
        self.message_label.config(text=f"WRONG! Your score was: {score}. \nPress Start to play again", font=("Helvetica", 24))
        self.sequence = []
        self.player_sequence = []

if __name__ == "__main__":
    root = tk.Tk()
    game = ColorMemoryGame(root)
    root.mainloop()
