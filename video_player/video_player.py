import tkinter as tk
from tkinter import ttk
import vlc
from tkinter import filedialog
import time

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        self.instance = vlc.Instance('--no-xlib')
        self.player = self.instance.media_player_new()
        self.setup_player_widget()
        self.create_gui()
        self.playing = False
        self.update_progressbar()

    def setup_player_widget(self):
        # label to hold video widget
        self.label = tk.Label(self.root)
        self.label.pack(fill=tk.BOTH, expand=True)

        # label to display video widget
        self.player.set_hwnd(self.label.winfo_id())

    def create_gui(self):
        # menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="Open Media", 
            command=self.open_media)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", 
            command=self.root.quit)
        
        # button for play, pause, stop, fast forward, rewind
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
         # buttons and progress bar
        self.play_button = tk.Button(
            button_frame, 
            text="Play", 
            command=self.toggle_play)
        self.play_button.grid(
            row=1, 
            column=1, 
            padx=10, 
            pady=10)

        self.rewind_button = tk.Button(
            button_frame, 
            text="<<", 
            command=self.rewind)
        self.rewind_button.grid(
            row=1, 
            column=0, 
            padx=10, 
            pady=10)

        self.fast_forward_button = tk.Button(
            button_frame, 
            text=">>", 
            command=self.fast_forward)
        self.fast_forward_button.grid(
            row=1, 
            column=2, 
            padx=10, 
            pady=10)

        self.progressbar = ttk.Progressbar(
            button_frame, 
            mode="determinate", 
            length=400)
        self.progressbar.grid(
            row=0, 
            column=0, 
            columnspan=3, 
            padx=10, 
            pady=10)

        self.stop_button = tk.Button(
            button_frame, 
            text="Stop", 
            command=self.stop_media)
        self.stop_button.grid(
            row=2, 
            column=0, 
            columnspan=3, 
            padx=10, 
            pady=10)
        
    def open_media(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Media Files", 
                        "*.mp4 *.avi *.mp3 *.wav")])
        if file_path:
            self.media = self.instance.media_new(
                file_path)
            self.player.set_media(self.media)
            self.toggle_play()
            time.sleep(0.1)
            self.toggle_play()

    def toggle_play(self):
        if hasattr(self, 'media'):
            if not self.playing:
                self.player.play()
                self.play_button.config(text="Pause")
                self.update_progressbar()
            else:
                self.player.pause()
                self.play_button.config(text="Play")
            self.playing = not self.playing

    def rewind(self):
        if hasattr(self, 'media'):
            current_time = self.player.get_time()
            current_time -= 10000 
            if current_time < 0:
                current_time = 0
            self.player.set_time(current_time)


    def fast_forward(self):
        if hasattr(self, 'media'):
            current_time = self.player.get_time()
            current_time += 10000 
            self.player.set_time(current_time)

    def stop_media(self):
        if hasattr(self, 'media'):
            self.player.stop()
            self.play_button.config(text="Play")
            self.playing = False

    def update_progressbar(self):
        if hasattr(self, 'media'):
            media_length = self.media.get_duration()
            if media_length > 0:
                current_time = self.player.get_time()
                progress = int(
                    (current_time / media_length) * 100)
                self.progressbar["value"] = progress
            else:
                self.progressbar["value"] = 0
            self.root.after(100, self.update_progressbar)

def main():
    root = tk.Tk()
    app = MediaPlayer(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()
