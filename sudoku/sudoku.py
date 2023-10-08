import tkinter as tk
import tkinter.messagebox as messagebox
import random

def is_valid_move(board, row, col, num):
    # check if number already present in row or column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # check if number is present in 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    num_cells_to_remove = random.randint(45, 55)

    # remove random cells
    cells_removed = 0
    while cells_removed < num_cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            cells_removed += 1

    return board

def solve_sudoku(board):
    def backtrack():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid_move(
                            board, 
                            row, 
                            col, 
                            num):
                            board[row][col] = num
                            if backtrack():
                                return True
                            board[row][col] = 0
                    return False
        return True

    # Make a copy of the original board and solve it
    original_board = [row[:] for row in board]
    return backtrack()

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.board = [[
            tk.StringVar() for _ in range(9)] 
            for _ in range(9)]
        self.entry_widgets = [[
            None for _ in range(9)] 
            for _ in range(9)]

        self.create_gui()
        self.generate_puzzle()
        self.winner = False

    def create_gui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(
                    self.frame,
                    width=2,
                    font=('Arial', 30),
                    textvariable=self.board[i][j],
                    justify='center',
                    bd=2,
                    relief="solid"
                )
                entry.grid(row=i, column=j)
                self.entry_widgets[i][j] = entry
                entry.bind(
                    '<Key>', 
                    lambda event, 
                    row=i, 
                    col=j: self.validate_input(row, col))

        self.new_button = tk.Button(
            self.frame, 
            text="New Puzzle", 
            command=self.generate_puzzle)
        self.new_button.grid(row=9, columnspan=9)

    def validate_input(self, row, col):
        user_input = self.board[row][col].get()
        if not user_input.isdigit():
            return
        num = int(user_input)
        if num < 1 or num > 9:
            self.board[row][col].set('')
        else:
            self.check_winner()

    def generate_puzzle(self):
        self.clear_board()
        sudoku_puzzle = generate_sudoku()
        for i in range(9):
            for j in range(9):
                value = sudoku_puzzle[i][j]
                self.board[i][j].set(
                    str(value) if value != 0 else '')
                if value == 0:
                    self.entry_widgets[i][j].config(
                        fg='black', 
                        state='normal', 
                        bg='white' if (
                            i // 3 + j // 3) % 2 == 0 
                            else 'light blue')
                else:
                    self.entry_widgets[i][j].config(
                        fg='black', 
                        state='disabled', 
                        disabledbackground='light blue' 
                        if (i // 3 + j // 3) % 2 == 
                            0 else 'white')

        # Alternate background colors for 3x3 groups
        for row_group in range(0, 9, 3):
            for col_group in range(0, 9, 3):
                color = 'light blue' if (
                    row_group // 3 + col_group // 3
                    ) % 2 == 0 else 'white'
                for i in range(
                    row_group, 
                    row_group + 3):
                    for j in range(
                        col_group,
                        col_group + 3):
                        self.entry_widgets[i][j].config(
                            bg=color)

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j].set('')
                self.entry_widgets[i][j].config(
                    fg='black', 
                    bg='white', 
                    state='normal')

    def check_winner(self):
        for i in range(9):
            for j in range(9):
                if not self.board[i][j].get().isdigit():
                    return  # Not all cells are filled

        # Check if the board is solved
        board = [[int(self.board[i][j].get()) 
                  for j in range(9)] for i in range(9)]
        if solve_sudoku(board):
            self.display_message("Congratulations! "
                                 "You've won!")
            self.winner = True
        else:
            self.display_message("Sorry, "
                    "that's not correct. Keep trying!")

    def display_message(self, message):
        messagebox.showinfo("Sudoku", message)

def main():
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
