import tkinter as tk
from tkinter import messagebox

current_player = 'X'
board = [' ' for _ in range(9)]

# handle player's move
def make_move(position):
    global current_player
    if board[position] == ' ':
        board[position] = current_player
        button_list[position].config(
            text=current_player, 
            font=('Helvetica', 40))
        check_winner()
        current_player = 'O' if current_player == 'X' else 'X'

# check for winner
def check_winner():
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            messagebox.showinfo(
                "Tic-Tac-Toe", 
                f"Player {board[i]} wins!")
            reset_game()
            return
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != ' ':
            messagebox.showinfo(
                "Tic-Tac-Toe",
                f"Player {board[i]} wins!")
            reset_game()
            return
    if (board[0] == board[4] == board[8] != ' ') or (
        board[2] == board[4] == board[6] != ' '):
        messagebox.showinfo(
            "Tic-Tac-Toe", 
            f"Player {board[4]} wins!")
        reset_game()
        return
    if ' ' not in board:
        messagebox.showinfo(
            "Tic-Tac-Toe", 
            "It's a draw!")
        reset_game()

# reset game
def reset_game():
    global current_player, board
    current_player = 'X'
    board = [' ' for _ in range(9)]
    for button in button_list:
        button.config(text=' ', font=('Helvetica', 40))

# main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# buttons for Tic-Tac-Toe grid
button_list = []
for i in range(9):
    row = i // 3
    col = i % 3
    button = tk.Button(
        root, 
        text=' ', 
        font=('Helvetica', 40), 
        width=6, 
        height=3,
        command=lambda i=i: make_move(i))
    button.grid(row=row, column=col, padx=10, pady=10)
    button_list.append(button)

# main loop
root.mainloop()
