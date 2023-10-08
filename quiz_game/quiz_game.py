import tkinter as tk

# Define quiz questions and answers
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "correct_option": 2,
    },
    {
        "question": "Which programming language is "
        "known for its readability?",
        "options": ["Java", "Python", "C++", "JavaScript"],
        "correct_option": 1,
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_option": 1,
    },
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz")
        self.root.geometry("400x550")
        self.root.configure(bg="#F5F5F5")

        self.current_question = 0
        self.score = 0
        self.quiz_finished = False

        # Title label
        self.title_label = tk.Label(
            root,
            text="Quiz", 
            font=("Arial", 24, "bold"), 
            bg="#F5F5F5", 
            fg="#333333"
        )
        self.title_label.pack(pady=10)

        self.question_label = tk.Label(
            root, 
            text="", 
            font=("Arial", 16), 
            wraplength=380, 
            justify="center", 
            bg="#F5F5F5"
        )
        self.question_label.pack(pady=20)

        self.radio_var = tk.IntVar()
        self.radio_buttons = []

        for i in range(4):
            radio_button = tk.Radiobutton(
                root, 
                text="", 
                variable=self.radio_var, 
                value=i, 
                font=("Arial", 14), 
                bg="#F5F5F5"
            )
            radio_button.pack(anchor="w", padx=20)
            self.radio_buttons.append(radio_button)

        self.next_button = tk.Button(
            root,
            text="Next",
            command=self.next_question,
            font=("Arial", 16),
            bg="#007BFF",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
        )
        self.next_button.pack(pady=20)

        self.result_label = tk.Label(
            root, 
            text="", 
            font=("Arial", 20, "bold"), 
            fg="#007BFF", 
            bg="#F5F5F5"
        )

        self.start_over_button = tk.Button(
            root,
            text="Start Over",
            command=self.start_over,
            font=("Arial", 16),
            bg="#007BFF",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
        )

        self.update_question()

    def update_question(self):
        if self.current_question < len(questions):
            question_data = questions[
                self.current_question]
            self.question_label.config(
                text=question_data["question"])
            for i in range(4):
                self.radio_buttons[i].config(
                    text=question_data["options"][i])
            self.radio_var.set(-1)
        else:
            self.show_result()

    def next_question(self):
        if self.quiz_finished:
            return

        if self.radio_var.get() == questions[
            self.current_question]["correct_option"]:
            self.score += 1

        self.current_question += 1

        if self.current_question < len(questions):
            self.update_question()
        else:
            self.show_result()

    def show_result(self):
        self.quiz_finished = True
        result_text = f"Your Score: "
        result_text = result_text + f"{self.score}"
        result_text = result_text + f"/{len(questions)}"
        self.result_label.config(
            text=result_text, 
            fg="#007BFF")
        self.result_label.pack(pady=20)
        self.next_button.config(state="disabled")
        self.start_over_button.pack(pady=10)

    def start_over(self):
        self.current_question = 0
        self.score = 0
        self.quiz_finished = False
        self.result_label.pack_forget()
        self.start_over_button.pack_forget()
        self.next_button.config(state="active")
        self.update_question()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
