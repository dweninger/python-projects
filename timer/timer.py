import tkinter as tk
from tkinter import ttk
import winsound

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self.large_font = ('Arial', 36)
        self.normal_font = ('Arial', 16)
        self.timer_font = ('Arial', 48, 'bold')

        self.time_label = ttk.Label(
            self.root, text="Set time (MM:SS):",
            font=self.normal_font,
            foreground="black",
            background="#f0f0f0")
        self.time_label.pack(pady=10)

        self.time_entry = ttk.Entry(
            self.root, font=self.normal_font)
        self.time_entry.pack()

        self.timer_label = ttk.Label(
            self.root, text="00:00",
            font=self.timer_font,
            foreground="black",
            background="#f0f0f0")
        self.timer_label.pack(pady=20)

        self.start_button = ttk.Button(
            self.root,
            text="Start",
            command=self.start_timer,
            style='TButton')
        self.start_button.pack()
        self.start_button['style'] = 'My.TButton'

        self.stop_button = ttk.Button(
            self.root,
            text="Stop",
            command=self.stop_timer,
            style='TButton')
        self.stop_button.pack()
        self.stop_button.configure(state="disabled")
        self.stop_button['style'] = 'My.TButton'

        self.reset_button = ttk.Button(
            self.root,
            text="Reset",
            command=self.reset_timer,
            style='TButton')
        self.reset_button.pack()
        self.reset_button['style'] = 'My.TButton'

        self.timer_running = False
        self.target_time = 0
        self.elapsed_time = 0

    def start_timer(self):
        if not self.timer_running:
            time_str = self.time_entry.get()
            try:
                minutes, seconds = map(
                    int, time_str.split(":"))
                self.target_time = minutes * 60 + seconds
            except (ValueError, IndexError):
                return

            if self.target_time <= 0:
                return

            self.timer_running = True
            self.root.after(1000, self.update_timer)
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="enabled")

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time += 1
            remaining_time = (
                self.target_time - self.elapsed_time)
            if remaining_time <= 0:
                self.timer_running = False
                self.timer_label.configure(
                    text="00:00", foreground="black")
                self.start_button.configure(
                    state="enabled")
                self.stop_button.configure(
                    state="disabled")
                self.reset_button.configure(
                    state="enabled")
                self.reset_timer()
                winsound.Beep(1000, 1000)
            else:
                minutes, seconds = divmod(
                    remaining_time, 60)
                time_str = f"{minutes:02d}:{seconds:02d}"
                self.timer_label.configure(text=time_str)
                self.root.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_button.configure(state="enabled")
            self.stop_button.configure(state="disabled")

    def reset_timer(self):
        self.elapsed_time = 0
        self.timer_running = False
        self.timer_label.configure(
            text="00:00", foreground="black")
        self.start_button.configure(state="enabled")
        self.stop_button.configure(state="disabled")
        self.reset_button.configure(state="enabled")
        self.time_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    style = ttk.Style(root)
    style.configure(
        'My.TButton', font=('Arial', 14, 'bold'))
    root.mainloop()
