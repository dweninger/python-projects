import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time
from pynput import mouse

class AutoScrollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Scroller")
        self.root.geometry("400x300")

        self.large_font = ('Helvetica', 16)
        self.normal_font = ('Helvetica', 12)

        self.scroll_speed_label = ttk.Label(
            self.root, text="Scroll Speed:", 
            font=self.large_font)
        self.scroll_speed_label.pack(pady=10)

        self.scroll_speed_entry = ttk.Entry(
            self.root, font=self.normal_font)
        self.scroll_speed_entry.pack()

        self.scroll_duration_label = ttk.Label(
            self.root, text="Scroll Duration (s):", 
            font=self.large_font)
        self.scroll_duration_label.pack(pady=10)

        self.scroll_duration_entry = ttk.Entry(
            self.root, font=self.normal_font)
        self.scroll_duration_entry.pack()

        self.style = ttk.Style()
        self.style.configure(
            'TButton', font=self.large_font)

        self.start_button = ttk.Button(
            self.root, 
            text="Start Scrolling (Click to Begin)", 
            command=self.setup_listener, 
            style='TButton')
        self.start_button.pack(pady=20)

        self.stop_button = ttk.Button(
            self.root, text="Stop Scrolling", 
            command=self.stop_scrolling, 
            style='TButton')
        self.stop_button.pack()
        
        self.scrolling = False
        self.listener = None

    def setup_listener(self):
        self.start_button.config(
            text="Scroller Running (Click to Start)")
        self.listener = mouse.Listener(
            on_click=self.on_click)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.listener.stop()
            self.start_scrolling()

    def start_scrolling(self):
        self.scrolling = True
        scroll_thread = threading.Thread(
            target=self.scroll)
        scroll_thread.start()

    def stop_scrolling(self):
        self.scrolling = False
        self.start_button.config(
            text="Start Scrolling (Click to Begin)")

    def scroll(self):
        scroll_duration = float(
            self.scroll_duration_entry.get())
        start_time = time.time()
        while self.scrolling:
            elapsed_time = time.time() - start_time
            if elapsed_time >= scroll_duration:
                self.scrolling = False
                self.start_button.config(
                    text="Start Scrolling "
                    "(Click to Begin)")
                break

            scroll_speed = float(
                self.scroll_speed_entry.get())
            scroll_speed = int(scroll_speed) * -1
            pyautogui.scroll(scroll_speed)
            time.sleep(0.001)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoScrollerApp(root)
    root.mainloop()
