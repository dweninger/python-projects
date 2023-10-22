import tkinter as tk
import tkinter.simpledialog

# Chessboard dimensions
BOARD_SIZE = 8
SQUARE_SIZE = 60
CANVAS_SIZE = BOARD_SIZE * SQUARE_SIZE

# Colors
LIGHT_BROWN = "#D2B48C"
DARK_BROWN = "#8B4513"

class ChessGame:
    def __init__(self, root):
        self.current_player = 'white'
        self.selected_square_highlight = None
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_king_rook_moved = False
        self.white_queen_rook_moved = False
        self.black_king_rook_moved = False
        self.black_queen_rook_moved = False
        self.last_double_move_pawn = None
        self.en_passant_capture = False
        self.root = root
        self.root.title("Chess")

        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=DARK_BROWN)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_square_click)

        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.selected_square = None
        self.move_history = []
        self.current_player = 'white'  # White goes first

        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_move, font=("Helvetica", 16))
        self.undo_button.pack()

        self.start_over_button = tk.Button(self.root, text="Start Over", command=self.start_over, font=("Helvetica", 16))
        self.start_over_button.pack()

        self.turn_label = tk.Label(self.root, text="Turn: White", font=("Helvetica", 16))
        self.turn_label.pack()

        self.check_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.check_label.pack()

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x0 = col * SQUARE_SIZE
                y0 = row * SQUARE_SIZE
                x1 = x0 + SQUARE_SIZE
                y1 = y0 + SQUARE_SIZE

                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                piece = self.board[row][col]
                text_color = "black" if piece.islower() else "white"
                self.canvas.create_text(
                    (x0 + x1) / 2, (y0 + y1) / 2,
                    text=piece.upper(), font=("Helvetica", 24), fill=text_color
                )

    def start_over(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.selected_square = None
        self.move_history = []
        self.current_player = 'white'
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_king_rook_moved = False
        self.white_queen_rook_moved = False
        self.black_king_rook_moved = False
        self.black_queen_rook_moved = False
        self.last_double_move_pawn = None
        self.en_passant_capture = False
        self.check_label.config(text="")
        self.update_turn_label()
        self.draw_board()

    def is_king_in_check(self, player, board):
        """
        Check if the given player's king is in check.
        """
        # Determine the position of the player's king
        king_position = None
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece.lower() == 'k' and piece.islower() == (player == 'black'):
                    king_position = (row, col)

        if king_position is None:
            return False  # Player's king not found

        # Loop through all opponent's pieces to see if any can capture the king
        opponent = 'white' if player == 'black' else 'black'
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = board[row][col]
                if piece.lower() != 'k' and piece.islower() != (player == 'black'):
                    if self.is_valid_move((row, col), king_position, board):
                        return True  # King is in check

        return False  # King is not in check

    def is_stalemate(self):
        return False

    def is_checkmate(self, player):
        # First, check if the player's king is in check
        if not self.is_king_in_check(player, self.board):
            return False  # The king is not in check, so it's not checkmate

        # Find all the pieces of the current player
        player_pieces = [piece for row in self.board for piece in row if (player == 'black' and piece.islower()) or (player == 'white' and piece.isupper())]
        print(player_pieces)
        # Iterate through the player's pieces to check their possible moves
        for row1 in range(BOARD_SIZE):
            for col1 in range(BOARD_SIZE):
                piece = self.board[row1][col1]
                if piece in player_pieces:
                    if piece =="p":
                        print("pawn")
                    for row2 in range(BOARD_SIZE):
                        for col2 in range(BOARD_SIZE):
                            if self.is_valid_move((row1, col1), (row2, col2), self.board):
                                # Try making the move on a copy of the board to check for king in check
                                board_copy = [row[:] for row in self.board]
                                board_copy[row2][col2] = board_copy[row1][col1]
                                board_copy[row1][col1] = ' '
                                print(board_copy)
                                print()
                                print(self.is_king_in_check(player,board_copy))
                                print()

                                # After making the move, check if the king is still in check
                                if not self.is_king_in_check(player, board_copy):
                                    return False  # A piece can move to safety, it's not checkmate
        print("CHECKMATE")
        # No valid move to get out of check, it's checkmate
        return True

    def check_for_winner(self):
        """
        Check if there's a winner (checkmate) or if the game is in stalemate.
        """
        if self.is_checkmate('white'):
            return 'black'  # Black wins
        elif self.is_checkmate('black'):
            return 'white'  # White wins
        elif self.is_stalemate():
            return 'stalemate'  # Stalemate
        else:
            return None  # No winner (ongoing game)

    def on_square_click(self, event):
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        square = (row, col)
        
        piece = self.board[row][col]
        
        if self.selected_square is None:
            # If no square is currently selected, try to select one
            if piece != ' ' and ((self.current_player == 'white' and piece.isupper()) or (self.current_player == 'black' and piece.islower())):
                self.selected_square = square
                self.highlight_selected_square(square)
        else:
            if square == self.selected_square:
                # Clicking the same piece again unselects it
                self.selected_square = None
                self.remove_highlight()
            elif self.is_valid_move(self.selected_square, square, self.board):
                # Try making the move on a copy of the board to check for king in check
                board_copy = [row[:] for row in self.board]
                board_copy[row][col] = board_copy[self.selected_square[0]][self.selected_square[1]]
                board_copy[self.selected_square[0]][self.selected_square[1]] = ' '

                # After making the move, check if the king is still in check
                if not self.is_king_in_check(self.current_player, board_copy):
                    self.move_piece(self.selected_square, square)
                    self.current_player = 'black' if self.current_player == 'white' else 'white'
                    self.update_turn_label()
                    self.selected_square = None
                    self.remove_highlight()

                    # Check for check and update the label
                    if self.is_king_in_check(self.current_player, self.board):
                        self.check_label.config(text=f"{self.current_player.capitalize()} is in check")
                    else:
                        self.check_label.config(text="")

                    # Check for checkmate, stalemate, or winner
                    winner = self.check_for_winner()
                    if winner is not None and winner != '':
                        if winner == 'stalemate':
                            self.check_label.config(text="Stalemate!")
                        else:
                            self.check_label.config(text=f"Checkmate! {winner.capitalize()} wins!")
                else:
                    self.check_label.config(text="Invalid move! Your king is in check.")
            else:
                # Clicking on a different piece with an invalid move reselects the new piece
                if piece != ' ' and ((self.current_player == 'white' and piece.isupper()) or (self.current_player == 'black' and piece.islower())):
                    self.selected_square = square
                    self.remove_highlight()
                    self.highlight_selected_square(square)

    def highlight_selected_square(self, square):
        if self.selected_square_highlight is not None:
            self.remove_highlight()

        row, col = square
        x0 = col * SQUARE_SIZE
        y0 = row * SQUARE_SIZE
        x1 = x0 + SQUARE_SIZE
        y1 = y0 + SQUARE_SIZE

        self.selected_square_highlight = self.canvas.create_rectangle(
            x0, y0, x1, y1, outline="light blue", width=4, stipple="gray50"
        )

    def remove_highlight(self):
        if self.selected_square_highlight is not None:
            self.canvas.delete(self.selected_square_highlight)
            self.selected_square_highlight = None

    def is_valid_move(self, from_square, to_square, board):
        row1, col1 = from_square
        row2, col2 = to_square
        piece = board[row1][col1]

        if piece == 'p' or piece == 'P':
            return self.is_valid_move_pawn(from_square, to_square, board)

        if piece == 'r' or piece == 'R':
            return self.is_valid_move_rook(from_square, to_square, board)

        if piece == 'n' or piece == 'N':
            return self.is_valid_move_knight(from_square, to_square, board)

        if piece == 'b' or piece == 'B':
            return self.is_valid_move_bishop(from_square, to_square, board)

        if piece == 'q' or piece == 'Q':
            return self.is_valid_move_queen(from_square, to_square, board)

        if piece == 'k' or piece == 'K':
            return self.is_valid_move_king(from_square, to_square, board)

        return False
    
    def is_valid_move_pawn(self, from_square, to_square, board):
        row1, col1 = from_square
        row2, col2 = to_square
        piece = board[row1][col1]
        direction = -1 if piece.isupper() else 1  # Determine direction (up for white, down for black)

        # Normal pawn move (one square forward)
        if col1 == col2 and row2 == row1 + direction and board[row2][col2] == ' ':
            return True

        # Initial double pawn move (two squares forward)
        if col1 == col2 and row2 == row1 + 2 * direction and row1 in (1, 6) and board[row2][col2] == ' ':
            return True

        # Pawn capture (diagonally)
        if abs(col2 - col1) == 1 and row2 == row1 + direction:
            target_piece = board[row2][col2]
            if target_piece != ' ' and target_piece.islower() != piece.islower():
                return True

        # En passant capture
        if abs(col2 - col1) == 1 and row2 == row1 + direction and (row1 + direction, col2) == self.last_double_move_pawn:
            return True

        return False

    def is_valid_move_rook(self, from_square, to_square, board):
        row1, col1 = from_square
        row2, col2 = to_square
        piece = board[row1][col1]
        # Rook cannot move through its own pieces
        if row1 == row2:
            if col1 < col2:
                for col in range(col1 + 1, col2):
                    if board[row1][col] != ' ':
                        return False
                return board[row2][col2] == ' ' or board[row2][col2].islower() != piece.islower()  # Capture or empty square

            if col1 > col2:
                for col in range(col2 + 1, col1):
                    if board[row1][col] != ' ':
                        return False
                return board[row2][col2] == ' ' or board[row2][col2].islower() != piece.islower()  # Capture or empty square

        elif col1 == col2:
            if row1 < row2:
                for row in range(row1 + 1, row2):
                    if board[row][col1] != ' ':
                        return False
                return board[row2][col2] == ' ' or board[row2][col2].islower() != piece.islower()

            if row1 > row2:
                for row in range(row2 + 1, row1):
                    if board[row][col1] != ' ':
                        return False
                return board[row2][col2] == ' ' or board[row2][col2].islower() != piece.islower() 

        return False

    def is_valid_move_bishop(self, from_square, to_square, board):
        row1, col1 = from_square
        row2, col2 = to_square
        piece = board[row1][col1]

        if abs(row2 - row1) != abs(col2 - col1):
            return False  # Bishop can only move diagonally

        step_row = 1 if row2 > row1 else -1
        step_col = 1 if col2 > col1 else -1

        current_row, current_col = row1 + step_row, col1 + step_col

        # Check if the bishop is moving through or landing on its own pieces
        while current_row != row2:
            target_piece = board[current_row][current_col]
            if target_piece != ' ':
                return False  # Bishop can't move through or on top of its own pieces
            current_row += step_row
            current_col += step_col

        target_piece = board[row2][col2]
        if target_piece == ' ':
            return True  # Bishop can move to an empty square
        elif target_piece.islower() != piece.islower():
            return True  # Bishop can capture an enemy piece
        else:
            return False  # Bishop can't capture its own pieces

    def is_valid_move_knight(self, from_square, to_square, board):
        row1, col1 = from_square
        row2, col2 = to_square
        piece = board[row1][col1]

        delta_row = abs(row2 - row1)
        delta_col = abs(col2 - col1)

        if (delta_row == 1 and delta_col == 2) or (delta_row == 2 and delta_col == 1):
            target_piece = board[row2][col2]
            if target_piece == ' ':
                return True
            elif target_piece.islower() != piece.islower():
                return True

        return False

    def is_valid_move_queen(self, from_square, to_square, board):
        return (
            self.is_valid_move_rook(from_square, to_square, board) or
            self.is_valid_move_bishop(from_square, to_square, board)
        )

    def is_valid_move_king(self, from_square, to_square, board):
        row1, col1 = from_square
        row2, col2 = to_square
        row_diff = abs(row1 - row2)
        col_diff = abs(col1 - col2)
        piece = board[row1][col1]

        if (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1):
            print("Valid king move")
            target_piece = board[row2][col2]
            if target_piece == ' ':
                return True
            elif target_piece.islower() != piece.islower():
                return True
            
        # Check for castling
        if self.is_valid_castling(from_square, to_square):
            print("Valid castle")
            return True

        return False

    def is_valid_king_side_castling(self):
        # Check if the squares between the king and rook are empty
        if self.board[7][5] != ' ' or self.board[7][6] != ' ':
            return False

        # Check if the squares the king moves through are not under attack
        if self.is_square_under_attack((7, 4)) or self.is_square_under_attack((7, 5)) or self.is_square_under_attack((7, 6)):
            return False

        # Check if the king and rook have not moved
        if self.has_king_moved or self.has_king_rook_moved:
            return False

        return True
    
    def is_square_under_attack(self, square):
        """
        Check if the given square is under attack by the opponent.
        """
        row, col = square
        piece = self.board[row][col]
        opponent = 'black' if self.current_player == 'white' else 'white'

        # Loop through all opponent's pieces to see if any can capture the square
        for row2 in range(BOARD_SIZE):
            for col2 in range(BOARD_SIZE):
                piece2 = self.board[row2][col2]
                if piece2.islower() == (opponent == 'white'):
                    if self.is_valid_move((row2, col2), square):
                        return True

        return False

    def promote_pawn(self, row, col):
        promotion_options = ['Queen', 'Rook', 'Bishop', 'Knight']  # Options for pawn promotion

        def promote_to(piece):
            promoted_piece = piece[0]  # Use the first letter of the selected piece
            if self.current_player == 'black':
                promoted_piece = promoted_piece.upper()  # If current player is white, promote to uppercase piece
            else:
                promoted_piece = promoted_piece.lower()  # If current player is black, promote to lowercase piece

            self.board[row][col] = promoted_piece
            self.draw_board()
            promotion_window.destroy()

        promotion_window = tk.Toplevel(self.root)
        promotion_window.title("Pawn Promotion")

        for option in promotion_options:
            button = tk.Button(promotion_window, text=option, command=lambda opt=option: promote_to(opt))
            button.pack()

    def move_piece(self, from_square, to_square):
        row1, col1 = from_square
        row2, col2 = to_square
        piece = self.board[row1][col1]

        if piece == 'p' and row2 == 7:
            # Black pawn reached the 1st rank, trigger promotion
            self.promote_pawn(row2, col2)
        elif piece == 'P' and row2 == 0:
            # White pawn reached the 8th rank, trigger promotion
            self.promote_pawn(row2, col2)

        # Check for en passant capture and remove the captured pawn
        if piece.lower() == 'p' and self.en_passant_capture:
            # En passant capture: Remove the captured pawn
            self.board[row1][col2] = ' '
            self.en_passant_capture = False

        # Check if the piece is a king and update movement history flags
        if piece.lower() == 'k':
            if self.current_player == 'white':
                self.white_king_moved = True
            else:
                self.black_king_moved = True
        elif piece.lower() == 'r':
            if self.current_player == 'white':
                if (row1, col1) == (7, 0):
                    self.white_queen_rook_moved = True
                elif (row1, col1) == (7, 7):
                    self.white_king_rook_moved = True
            else:
                if (row1, col1) == (0, 0):
                    self.black_queen_rook_moved = True
                elif (row1, col1) == (0, 7):
                    self.black_king_rook_moved = True

        # Check if it's a castling move and move the rook accordingly
        if piece.lower() == 'k' and abs(col2 - col1) == 2:
            if col2 > col1:  # King-side castling
                rook_col1, rook_col2 = 7, 5
            else:  # Queen-side castling
                rook_col1, rook_col2 = 0, 3

            rook = self.board[row1][rook_col1]
            self.board[row1][rook_col1] = ' '
            self.board[row1][rook_col2] = rook

        # Continue with the rest of the move logic
        self.move_history.append(((row1, col1), (row2, col2), piece))
        self.board[row1][col1] = ' '
        self.board[row2][col2] = piece
        self.draw_board()

    def is_valid_castling(self, from_square, to_square):
        row1, col1 = from_square
        row2, col2 = to_square
        piece = self.board[row1][col1]

        if piece.lower() == 'k':
            if self.current_player == 'white':
                if not self.white_king_moved:
                    if row1 == 7 and abs(col2 - col1) == 2:  # King-side or queen-side castling
                        if col2 == 6:  # King-side castling
                            if not self.white_king_rook_moved:
                                for col in range(col1 + 1, col2):
                                    if self.board[row1][col] != ' ':
                                        return False
                            else:
                                return False
                        elif col2 == 2:  # Queen-side castling
                            if not self.white_queen_rook_moved:
                                for col in range(col2 + 1, col1):
                                    if self.board[row1][col] != ' ':
                                        return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                if not self.black_king_moved:
                    if row1 == 0 and abs(col2 - col1) == 2:  # King-side or queen-side castling
                        if col2 == 6:  # King-side castling
                            if not self.black_king_rook_moved:
                                for col in range(col1 + 1, col2):
                                    if self.board[row1][col] != ' ':
                                        return False
                            else:
                                return False
                        elif col2 == 2:  # Queen-side castling
                            if not self.black_queen_rook_moved:
                                for col in range(col2 + 1, col1):
                                    if self.board[row1][col] != ' ':
                                        return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        return True

    def undo_move(self):
        if self.move_history:
            from_square, to_square, piece = self.move_history.pop()
            row1, col1 = from_square
            row2, col2 = to_square
            self.board[row1][col1] = piece
            self.board[row2][col2] = ' '
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            self.update_turn_label()
            self.draw_board()

    def update_turn_label(self):
        turn = "White" if self.current_player == "white" else "Black"
        self.turn_label.config(text=f"Turn: {turn}")

def main():
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
