import tkinter as tk

ROWS = 6
COLS = 7
CELL_SIZE = 80

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Four in a Row Game")
        self.current_player = 1
        self.create_gui()
    
    def create_gui(self):
        self.canvas = tk.Canvas(
            self.root, 
            width=COLS * CELL_SIZE, 
            height=ROWS * CELL_SIZE + CELL_SIZE, 
            bg="skyblue")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.make_move)

        self.board = [
            [0 for _ in range(COLS)] 
            for _ in range(ROWS)]

        # Draw initial grid
        for i in range(1, COLS):
            x = i * CELL_SIZE
            self.canvas.create_line(
                x, 0, x, 
                (ROWS + 1) * CELL_SIZE, 
                fill="orange", width=5)

        for i in range(1, ROWS + 1):
            y = i * CELL_SIZE
            self.canvas.create_line(0, y, 
                COLS * CELL_SIZE, y, 
                fill="orange", width=5)

        self.start_over_button = tk.Button(
            self.root, 
            text="Start Over", 
            command=self.reset_board)
        self.start_over_button.pack()

    def make_move(self, event):
        col = event.x // CELL_SIZE
        row = self.get_empty_row(col)
        if row is not None:
            self.draw_piece(row, col)
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                winner = (
                    "Player 1" 
                    if self.current_player == 1
                    else "Player 2")
                self.show_message(f"{winner} wins!")
                self.canvas.unbind("<Button-1>")
                self.start_over_button.config(
                    state="active")
                self.canvas.create_rectangle(
                    COLS * CELL_SIZE // 4, 
                    ROWS * CELL_SIZE // 4,
                    3 * COLS * CELL_SIZE // 4, 
                    3 * ROWS * CELL_SIZE // 4,
                    fill="skyblue", outline="", 
                    width=0
                )
                self.canvas.tag_raise("winner_message") 
            elif all(self.board[0][c] != 0 
                     for c in range(COLS)):
                self.show_message("It's a draw!")
                self.canvas.unbind("<Button-1>")
                self.start_over_button.config(
                    state="active")
            else:
                self.current_player = (
                    2 if self.current_player == 1 
                    else 1)

    def get_empty_row(self, col):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return None

    def draw_piece(self, row, col):
        x = col * CELL_SIZE
        y = (row + 1) * CELL_SIZE
        color = ("red" if self.current_player == 1 
                 else "yellow")
        self.canvas.create_oval(x, y, x + CELL_SIZE, 
                        y + CELL_SIZE, fill=color)

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), 
                      (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i * dr, col + i * dc
                if (0 <= r < ROWS and 0 <= c < COLS 
                    and self.board[r][c] == 
                    self.current_player):
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - i * dr, col - i * dc
                if (0 <= r < ROWS and 
                    0 <= c < COLS and 
                    self.board[r][c] == 
                    self.current_player):
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def show_message(self, message):
        self.canvas.create_rectangle(
            COLS * CELL_SIZE // 4, 
            ROWS * CELL_SIZE // 4,
            3 * COLS * CELL_SIZE // 4, 
            3 * ROWS * CELL_SIZE // 4,
            fill="skyblue", outline="", 
            width=0, tags="winner_message"
        )
        self.canvas.create_text(
            COLS * CELL_SIZE // 2, 
            ROWS * CELL_SIZE // 2,
            text=message, font=("Arial", 24), 
            fill="black", tags="winner_message"
        )

    def reset_board(self):
        self.canvas.delete("all")
        self.current_player = 1
        self.canvas.bind("<Button-1>", self.make_move)

        self.board = [[0 for _ in range(COLS)] 
                      for _ in range(ROWS)]

        # Draw grid
        for i in range(1, COLS):
            x = i * CELL_SIZE
            self.canvas.create_line(x, 0, x, 
                (ROWS + 1) * CELL_SIZE, 
                fill="orange", width=5)

        for i in range(1, ROWS + 1):
            y = i * CELL_SIZE
            self.canvas.create_line(0, y, 
                COLS * CELL_SIZE, y, 
                fill="orange", width=5)

def main():
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()

if __name__ == "__main__":
    main()
