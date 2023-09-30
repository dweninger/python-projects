import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
            update_word_count()

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get(1.0, tk.END))

def clear_text():
    text.delete(1.0, tk.END)
    update_word_count()

def update_word_count():
    content = text.get(1.0, tk.END)
    words = content.split()
    word_count_label.config(text=f"Word Count: {len(words)}")

def on_key_release(event):
    window.after(1000, update_word_count)

# Create the main window
window = tk.Tk()
window.title("Simple Text Editor")

# Create a text widget
text = tk.Text(window, wrap=tk.WORD)
text.pack(expand=tk.YES, fill=tk.BOTH)
text.bind("<KeyRelease>", on_key_release)

# Create a menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# Create an Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Clear", command=clear_text)

# Create a label for word count
word_count_label = tk.Label(window, text="Word Count: 0")
word_count_label.pack()

# Start the main loop
window.mainloop()
