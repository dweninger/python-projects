import tkinter as tk
from tkinter import ttk
import threading
from pynput.mouse import Controller, Button
import time
from pynput import mouse

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("300x250")

        self.large_font = ('Helvetica', 16)
        self.normal_font = ('Helvetica', 12)

        self.clicks_label = ttk.Label(
            self.root, text="Clicks per second:", 
            font=self.large_font)
        self.clicks_label.pack(pady=10)

        self.clicks_entry = ttk.Entry(
            self.root, font=self.normal_font)
        self.clicks_entry.pack()

        self.duration_label = ttk.Label(
            self.root, text="Duration (seconds):", 
            font=self.large_font)
        self.duration_label.pack(pady=10)

        self.duration_entry = ttk.Entry(
            self.root, font=self.normal_font)
        self.duration_entry.pack()

        self.start_button = ttk.Button(
            self.root, 
            text="Start Clicking", 
            command=self.start_clicking, 
            style='TButton')
        self.start_button.pack(pady=20)

        self.stop_button = ttk.Button(
            self.root, 
            text="Stop Clicking", 
            command=self.stop_clicking, 
            style='TButton')
        self.stop_button.pack()
        self.stop_button.configure(state="disabled")

        self.clicking = False
        self.clicks_per_second = 0
        self.duration = 0
        self.listener = None

    def start_clicking(self):
        if not self.clicking:
            self.start_button.configure(
                text="Click anywhere on "
                "the screen to start")
            self.listener = mouse.Listener(
                on_click=self.on_click)
            self.listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.listener.stop()
            try:
                self.clicks_per_second = float(
                    self.clicks_entry.get())
                self.duration = int(
                    self.duration_entry.get())
            except (ValueError, IndexError):
                return

            if self.clicks_per_second <= 0 or (
                self.duration <= 0):
                return

            self.clicking = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="enabled")

            click_thread = threading.Thread(
                target=self.click)
            click_thread.start()

            self.root.after(
                self.duration * 1000, 
                self.stop_clicking)

    def stop_clicking(self):
        self.clicking = False
        self.start_button.configure(state="enabled")
        self.stop_button.configure(state="disabled")

    def click(self):
        mouse_controller = Controller()
        click_interval = 1 / self.clicks_per_second
        end_time = time.time() + self.duration

        while self.clicking and time.time() < end_time:
            mouse_controller.click(Button.left)
            time.sleep(click_interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
