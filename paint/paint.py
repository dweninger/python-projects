import tkinter as tk

drawing = False
last_x = 0
last_y = 0

def start_drawing(event):
    global drawing, last_x, last_y
    drawing = True
    last_x = event.x
    last_y = event.y

def stop_drawing(event):
    global drawing
    drawing = False

def draw(event):
    global last_x, last_y
    if drawing:
        canvas.create_line(
            (last_x, last_y, event.x, event.y), 
            width=2, fill="black")
        last_x = event.x
        last_y = event.y

def clear_canvas():
    canvas.delete("all")

# Create the main window
root = tk.Tk()
root.title("Simple Paint")

# Create a canvas for drawing
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Bind mouse events to functions
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<ButtonRelease-1>", stop_drawing)
canvas.bind("<B1-Motion>", draw)

# Create a "Clear" button
clear_button = tk.Button(
    root, 
    text="Clear", 
    command=clear_canvas)
clear_button.pack()

# Run the main loop
root.mainloop()
