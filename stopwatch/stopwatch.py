import tkinter as tk
from datetime import datetime, timedelta

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("400x180")

        self.is_running = False
        self.start_time = None
        self.elapsed_time = timedelta(0)

        self.time_label = tk.Label(
            root, text="00:00.000", 
            font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        button_frame = tk.Frame(root)
        button_frame.pack()

        self.start_button = tk.Button(
            button_frame, text="Start", 
            command=self.start_stop, 
            font=("Helvetica", 14))
        self.reset_button = tk.Button(
            button_frame, text="Reset", 
            command=self.reset, 
            font=("Helvetica", 14))

        self.start_button.grid(row=0, column=0, padx=10)
        self.reset_button.grid(row=0, column=1, padx=10)

        self.update_time()

    def start_stop(self):
        if self.is_running:
            self.is_running = False
            self.start_button["text"] = "Resume"
            if self.start_time is not None:
                self.elapsed_time += datetime.now(
                ) - self.start_time
                self.start_time = None
        else:
            self.is_running = True
            self.start_button["text"] = "Pause"
            self.start_time = datetime.now()
            self.update_time()

    def reset(self):
        self.is_running = False
        self.start_button["text"] = "Start"
        self.elapsed_time = timedelta(0)
        self.start_time = None
        self.update_time()

    def update_time(self):
        if self.is_running:
            if self.start_time is not None:
                elapsed_time = self.elapsed_time + (
                    datetime.now() - self.start_time)
            else:
                elapsed_time = self.elapsed_time
        else:
            elapsed_time = self.elapsed_time
        total_seconds = elapsed_time.total_seconds()
        minutes, seconds = divmod(total_seconds, 60)
        minutes = int(minutes)
        seconds = int(seconds)
        milliseconds = int((
            total_seconds - minutes * 60 - seconds) 
            * 1000)
        time_str = f"{minutes:02d}:{seconds:02d}"
        time_str = time_str + f".{milliseconds:03d}"
        self.time_label.config(text=time_str)
        self.root.after(50, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
