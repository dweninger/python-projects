import tkinter as tk
from tkinter import messagebox

# add a new flashcard
def add_flashcard():
    question = question_entry.get()
    answer = answer_entry.get()
    if question and answer:
        flashcards_list.insert(tk.END, (question, answer))
        question_entry.delete(0, tk.END)
        answer_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", 
            "Both question and answer must be provided.")

# delete a selected flashcard
def delete_flashcard():
    selected_index = flashcards_list.curselection()
    if selected_index:
        flashcards_list.delete(selected_index)
    else:
        messagebox.showwarning("Warning", 
            "Select a flashcard to delete.")

# start the quiz
def start_quiz():
    flashcards = flashcards_list.get(0, tk.END)
    if not flashcards:
        messagebox.showwarning("Warning", 
            "No flashcards available for the quiz.")
        return

    def show_question():
        nonlocal current_flashcard_index
        if current_flashcard_index < len(flashcards):
            current_flashcard = flashcards[
                current_flashcard_index]
            flashcard_label.config(
                text=f"Q: {current_flashcard[0]}")
            show_question_button.config(state=tk.DISABLED)
            show_answer_button.config(state=tk.NORMAL)

    def show_answer():
        nonlocal current_flashcard_index
        if current_flashcard_index < len(flashcards):
            current_flashcard = flashcards[
                current_flashcard_index]
            flashcard_label.config(
                text=f"A: {current_flashcard[1]}")
            show_question_button.config(state=tk.NORMAL)
            current_flashcard_index += 1
            if current_flashcard_index >= len(flashcards):
                messagebox.showinfo("End of Quiz", 
                                    "End of quiz!")
                quiz_window.destroy()

    quiz_window = tk.Toplevel(root)
    quiz_window.title("Flashcard Quiz")
    quiz_window.geometry("400x200")

    current_flashcard_index = 0

    flashcard_label = tk.Label(
        quiz_window, 
        text="", 
        font=("Helvetica", 16))
    flashcard_label.pack()

    show_question_button = tk.Button(
        quiz_window, 
        text="Show Question", 
        command=show_question, 
        font=("Helvetica", 16))
    show_question_button.pack()

    show_answer_button = tk.Button(
        quiz_window, 
        text="Show Answer", 
        command=show_answer, 
        font=("Helvetica", 16))
    show_answer_button.pack()
    show_answer_button.config(state=tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("Flashcard Quiz App")
root.geometry("500x500")

# Create flashcard management UI
question_label = tk.Label(
    root, 
    text="Question:", 
    font=("Helvetica", 16))
question_label.pack()
question_entry = tk.Entry(root, font=("Helvetica", 16))
question_entry.pack()

answer_label = tk.Label(
    root, 
    text="Answer:", 
    font=("Helvetica", 16))
answer_label.pack()
answer_entry = tk.Entry(root, font=("Helvetica", 16))
answer_entry.pack()

add_button = tk.Button(
    root, 
    text="Add Flashcard", 
    command=add_flashcard, 
    font=("Helvetica", 16))
add_button.pack()

delete_button = tk.Button(
    root, 
    text="Delete Flashcard", 
    command=delete_flashcard, 
    font=("Helvetica", 16))
delete_button.pack()

# Create flashcards listbox
flashcards_list = tk.Listbox(
    root, 
    width=40, 
    height=10, 
    font=("Helvetica", 14))
flashcards_list.pack()

# Creat button to start quiz
start_quiz_button = tk.Button(
    root, 
    text="Start Quiz", 
    command=start_quiz, 
    font=("Helvetica", 16))
start_quiz_button.pack()

# Run main loop
root.mainloop()
