import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput import mouse
import pyperclip

class ColorDropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Dropper")
        self.root.geometry("400x400")

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16))
        style.configure('TLabel', font=('Helvetica', 20))

        self.color_label = ttk.Label(
            self.root, text="Picked Color:")
        self.color_label.pack(pady=20)

        self.color_canvas = tk.Canvas(
            self.root, width=100, height=100, 
            highlightthickness=2, highlightbackground="black")
        self.color_canvas.pack()

        self.color_hex_label = ttk.Label(
            self.root, text="Hex Value:")
        self.color_hex_label.pack(pady=20)

        self.copy_hex_button = ttk.Button(
            self.root, text="Copy", command=self.copy_hex_value)
        self.copy_hex_button.pack()

        self.pick_color_button = ttk.Button(
            self.root, text="Pick Color", command=self.toggle_color_picker)
        self.pick_color_button.pack(pady=20)

        self.picking_color = False
        self.listener = None  # Initialize listener as None
        self.clear_color()
        self.copied_color = None  # Initialize copied color variable

    def toggle_color_picker(self):
        if self.picking_color:
            self.picking_color = False
            self.pick_color_button.configure(text="Pick Color")
            self.stop_listener()
        else:
            self.picking_color = True
            self.pick_color_button.configure(text="Picking... Click anywhere")
            self.start_listener()

    def copy_hex_value(self):
        if self.copied_color:
            pyperclip.copy(self.copied_color)

    def start_listener(self):
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def on_click(self, x, y, button, pressed):
        if pressed:
            color = pyautogui.screenshot(region=(x, y, 1, 1)).getpixel((0, 0))
            color_hex = self.rgb_to_hex(color)
            self.update_color(color_hex)
            self.copied_color = color_hex  # Update copied color
            self.picking_color = False
            self.pick_color_button.configure(text="Pick Color")
            self.stop_listener()

    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    def update_color(self, color_hex):
        self.color_canvas.configure(bg=color_hex)
        self.color_hex_label.configure(text="Hex Value: " + color_hex)

    def clear_color(self):
        self.color_canvas.configure(bg="white")
        self.color_hex_label.configure(text="Hex Value: ")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorDropperApp(root)
    root.mainloop()
