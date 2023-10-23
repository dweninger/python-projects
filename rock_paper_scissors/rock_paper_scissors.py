import tkinter as tk
import random

def determine_winner(player_choice):
    choices = ["Rock", "Paper", "Scissors"]
    computer_choice = random.choice(choices)
    computer_label.config(
        text=f"Computer chooses: {computer_choice}")
    
    if player_choice == computer_choice:
        result_label.config(
            text="It's a tie!", fg="gray")
    elif (player_choice == "Rock" 
          and computer_choice == "Scissors") or \
         (player_choice == "Paper" 
          and computer_choice == "Rock") or \
         (player_choice == "Scissors" 
          and computer_choice == "Paper"):
        result_label.config(
            text="You win!", fg="green")
    else:
        result_label.config(
            text="Computer wins!", fg="red")

# Main window
root = tk.Tk()
root.title("Rock, Paper, Scissors")
root.configure(bg="lightgray")

# Labels for user and computer choices
player_label = tk.Label(
    root, text="Your choice:", 
    font=("Arial", 16), 
    bg="lightgray")
player_label.pack(pady=10)

computer_label = tk.Label(
    root, text="Computer chooses:", 
    font=("Arial", 16), 
    bg="lightgray")
computer_label.pack()

result_label = tk.Label(
    root, text="", 
    font=("Arial", 18), 
    bg="lightgray")
result_label.pack(pady=10)

# Buttons for rock, paper, and scissors
button_font = ("Arial", 14)
button_width = 10

rock_button = tk.Button(
    root, text="Rock", 
    font=button_font, 
    width=button_width, 
    command=lambda: determine_winner("Rock"))
rock_button.pack(
    side="left", padx=20, pady=10, 
    fill="both", expand=True)

paper_button = tk.Button(
    root, text="Paper", 
    font=button_font, 
    width=button_width, 
    command=lambda: determine_winner("Paper"))
paper_button.pack(
    side="left", pady=10, 
    fill="both", expand=True)

scissors_button = tk.Button(
    root, text="Scissors", 
    font=button_font, 
    width=button_width, 
    command=lambda: determine_winner("Scissors"))
scissors_button.pack(
    side="right", padx=20, pady=10, 
    fill="both", expand=True)

# Center buttons
root.update()
button_frame = tk.Frame(root, bg="lightgray")
button_frame.pack(fill="both", expand=True)
button_frame.place(
    in_=root, anchor="c", relx=0.5, rely=0.8)

root.mainloop()
