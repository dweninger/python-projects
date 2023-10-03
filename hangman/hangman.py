import tkinter as tk
import random

# List of words for the Hangman game
words = ["python", "typescript", "java", 
         "ruby", "perl", "rust", "swift"]

# List of Hangman ASCII art
hangman_parts = ['''
        +---+
        |   |
            |
            |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
            |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
        |   |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|   |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|\  |
            |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|\  |
       /    |
            |
        =========''', '''
        +---+
        |   |
        O   |
       /|\  |
       / \  |
            |
        =========''']

# choose a random word from the list
def choose_word():
    return random.choice(words)

# initialize the game
def new_game():
    global word_to_guess, guessed_word
    global attempts_left, current_hangman
    word_to_guess = choose_word()
    guessed_word = ["_"] * len(word_to_guess)
    attempts_left = 6  # Number of attempts allowed
    current_hangman = 0  # Current Hangman art index
    update_display()
    update_hangman()
    letter_entry.config(state=tk.NORMAL) 
    result_label.config(text="")

# handle a guessed letter
def guess_letter():
    global attempts_left, current_hangman
    letter = letter_entry.get().lower()
    if len(letter) == 1 and letter.isalpha():
        if letter in word_to_guess:
            for i in range(len(word_to_guess)):
                if word_to_guess[i] == letter:
                    guessed_word[i] = letter
        else:
            attempts_left -= 1
            current_hangman += 1
            update_hangman()
        update_display()
        check_game_over()

# update the game display
def update_display():
    word_label.config(text=" ".join(guessed_word))
    attempts_label.config(
        text=f"Attempts Left: {attempts_left}")
    letter_entry.delete(0, tk.END)

# update the Hangman ASCII art
def update_hangman():
    if current_hangman < len(hangman_parts):
        hangman_ascii.config(text=hangman_parts[current_hangman])
    else:
        hangman_ascii.config(text="Game Over")

# check if the game is over
def check_game_over():
    if "_" not in guessed_word:
        result_label.config(text="You Win! Play Again?")
    elif attempts_left == 0:
        result_label.config(
            text=f"You Lose! The word was "
            f"'{word_to_guess}'. Play Again?")
    else:
        return
    letter_entry.config(state=tk.DISABLED)

# main window
root = tk.Tk()
root.title("Hangman Game")

# labels
word_label = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 24))
word_label.pack()

attempts_label = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 16))
attempts_label.pack()

result_label = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 16))
result_label.pack()

hangman_ascii = tk.Label(
    root, 
    text="", 
    font=("Courier", 16))
hangman_ascii.pack()

# letter entry and guess button
letter_entry = tk.Entry(
    root, 
    font=("Helvetica", 16))
letter_entry.pack()

guess_button = tk.Button(
    root, 
    text="Guess", 
    command=guess_letter, 
    font=("Helvetica", 16))
guess_button.pack()

# new game button
new_game_button = tk.Button(
    root, 
    text="New Game", 
    command=new_game, 
    font=("Helvetica", 16))
new_game_button.pack()

# start new game
new_game()

# run main loop
root.mainloop()
