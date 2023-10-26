import tkinter as tk
import random
from tkinter import font
from tkinter import Label

# List of words to find in the grid
words_to_find = ["WORD", "SEARCH", "PYTHON", "JAVA", "GAME"]

def generate_word_search_grid(words_to_find):
    grid_size = 12  # Increase the grid size to make it larger
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    for word in words_to_find:
        placed = False
        while not placed:
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - len(word))
                if random.choice([True, False]):
                    word = word[::-1]  # Reverse the word
            else:
                row = random.randint(0, grid_size - len(word))
                col = random.randint(0, grid_size - 1)
                if random.choice([True, False]):
                    word = word[::-1]  # Reverse the word

            if all(grid[row + (i if direction == 'vertical' else 0)][col + (i if direction == 'horizontal' else 0)] == ' ' for i in range(len(word))):
                placed = True
                if direction == 'horizontal':
                    for i, letter in enumerate(word):
                        grid[row][col + i] = letter
                else:
                    for i, letter in enumerate(word):
                        grid[row + i][col] = letter

    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    return grid

class WordSearchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Search Game")

        self.canvas = tk.Canvas(self.root, width=360, height=400)  # Increase the canvas size
        self.canvas.grid(row=0, column=0)

        self.canvas.bind("<ButtonPress-1>", self.on_start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release_drag)

        self.selected_cells = []

        self.words_to_find = list(words_to_find)

        self.word_search_grid = generate_word_search_grid(self.words_to_find)

        self.create_grid()
        self.create_word_bank()
        self.create_start_over_button()  # Add Start Over button

    def create_grid(self):
        cell_size = 30  # Increase the cell size for larger components
        for i in range(len(self.word_search_grid)):
            for j in range(len(self.word_search_grid[i])):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = (j + 1) * cell_size, (i + 1) * cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=self.word_search_grid[i][j], font=("Helvetica", 12))  # Adjust the font size

    def create_word_bank(self):
        self.word_bank_frame = tk.Frame(self.root)
        self.word_bank_frame.grid(row=1, column=0)

        self.word_bank_label = tk.Label(self.word_bank_frame, text="Word Bank:", font=("Helvetica", 16))  # Adjust the font size
        self.word_bank_label.pack()

        self.word_labels = []
        for word in self.words_to_find:
            label = Label(self.word_bank_frame, text=word, font=("Helvetica", 14), padx=20, pady=0)
            label.pack()
            self.word_labels.append(label)

    def create_start_over_button(self):
        self.start_over_button = tk.Button(self.root, text="Start Over", command=self.start_over)
        self.start_over_button.grid(row=2, column=0)

    def start_over(self):
        # Clear the canvas
        self.canvas.delete("all")
        self.word_bank_label.config(text="")
        # Regenerate the game
        self.words_to_find = list(words_to_find)
        self.word_search_grid = generate_word_search_grid(self.words_to_find)
        self.create_grid()
        self.create_word_bank()
        self.canvas.bind("<ButtonPress-1>", self.on_start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release_drag)

    def on_start_drag(self, event):
        cell_size = 30  # Increase the cell size
        row = event.y // cell_size
        col = event.x // cell_size
        self.selected_cells = [(row, col)]
        self.canvas.delete("selection")
        self.canvas.create_rectangle(
            col * cell_size,
            row * cell_size,
            (col + 1) * cell_size,
            (row + 1) * cell_size,
            fill="lightblue",
            outline="blue",
            tags="selection",
        )

    def on_drag(self, event):
        cell_size = 30  # Increase the cell size
        row = event.y // cell_size
        col = event.x // cell_size

        if self.is_valid_selection(row, col):
            self.clear_non_straight_cells(row, col)
            self.selected_cells.append((row, col))
            self.canvas.delete("selection")

            # Draw the straight-line selection
            self.draw_straight_line_selection(cell_size)

    def clear_non_straight_cells(self, row, col):
        # Clear cells that are not part of the current straight line
        if len(self.selected_cells) > 1:
            last_row, last_col = self.selected_cells[-2]
            for r, c in self.selected_cells[:-2]:
                if not self.is_straight(last_row, last_col, row, col, r, c):
                    self.selected_cells.remove((r, c))

    def is_straight(self, x1, y1, x2, y2, x3, y3):
        return (x1 - x2) * (y2 - y3) == (x2 - x3) * (y1 - y2)

    def draw_straight_line_selection(self, cell_size):
        for i in range(1, len(self.selected_cells)):
            x0, y0 = self.selected_cells[i - 1][1] * cell_size + cell_size // 2, self.selected_cells[i - 1][0] * cell_size + cell_size // 2
            x1, y1 = self.selected_cells[i][1] * cell_size + cell_size // 2, self.selected_cells[i][0] * cell_size + cell_size // 2

            selected_word = "".join([self.word_search_grid[row][col] for row, col in self.selected_cells])

            if selected_word in self.words_to_find:
                self.canvas.create_line(x0, y0, x1, y1, fill="blue", width=2, tags="foundword")
            else:
                self.canvas.create_line(x0, y0, x1, y1, fill="blue", width=2, tags="selection")

    def on_release_drag(self, event):
        partial_word = ""

        for i, (row, col) in enumerate(self.selected_cells):
            if 0 <= row < len(self.word_search_grid) and 0 <= col < len(self.word_search_grid[0]):
                partial_word += self.word_search_grid[row][col]

            if partial_word in self.words_to_find:
                matching_word_labels = [label for label in self.word_labels if label.cget("text") == partial_word]
                if matching_word_labels:
                    for label in matching_word_labels:
                        label.config(text=f"{partial_word}", font=("Helvetica", 14, 'overstrike'))
                        self.words_to_find.remove(partial_word)

        self.canvas.delete("selection")

        if not self.words_to_find:
            self.word_bank_label.config(text="Word Bank: All words found! You win!")

    def is_valid_selection(self, row, col):
        if not self.selected_cells:
            return True  # First cell is always valid

        last_row, last_col = self.selected_cells[-1]
        return (row == last_row and abs(col - last_col) == 1) or (col == last_col and abs(row - last_row) == 1)

if __name__ == "__main__":
    root = tk.Tk()
    game = WordSearchGame(root)
    root.mainloop()
