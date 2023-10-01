import tkinter as tk
from tkinter import messagebox
from tkinter import font

# add a task to the list
def add_task():
    task = entry.get()
    if task:
        task_listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", 
                    "Please enter a task.")

# remove a selected task from the list
def remove_task():
    selected_task_index = task_listbox.curselection()
    if selected_task_index:
        task_listbox.delete(selected_task_index)
    else:
        messagebox.showwarning("Warning", 
                    "Please select a task to remove.")

# create the main window
root = tk.Tk()
root.title("To-Do List")
# size of the main window
root.geometry("400x400")

custom_font = font.nametofont("TkDefaultFont")
custom_font.configure(size=14)
entry = tk.Entry(root, font=custom_font, width=30)
entry.pack(pady=10)

# create buttons
add_button = tk.Button(root, 
            text="Add Task",
            font=custom_font, 
            command=add_task)
remove_button = tk.Button(root, 
            text="Remove Task", 
            font=custom_font, 
            command=remove_task)
add_button.pack()
remove_button.pack()

# create a listbox of the tasks
task_listbox = tk.Listbox(root, 
                font=custom_font, 
                selectmode=tk.SINGLE, 
                width=30, 
                height=10)
task_listbox.pack()

# run the main loop
root.mainloop()
