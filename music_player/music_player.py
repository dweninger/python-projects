import tkinter as tk
import pygame
from tkinter import filedialog
from tkinter import font
from tkinter import ttk

# add a song to playlist
def add_song():
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        song_list.insert(tk.END, file_path.split('/')[-1]) 
        song_paths.append(file_path)

# play selected song
def play_song():
    selected_song = song_list.curselection()
    if selected_song:
        song_index = selected_song[0]
        pygame.mixer.init()
        pygame.mixer.music.load(song_paths[song_index])
        pygame.mixer.music.play()
        update_progress()  # Start updating progress

# stop currently playing song
def stop_song():
    pygame.mixer.music.stop()

# delete selected song from playlist
def delete_song():
    selected_song = song_list.curselection()
    if selected_song:
        song_index = selected_song[0]
        song_list.delete(song_index)
        song_paths.pop(song_index)

def update_progress():
    if pygame.mixer.music.get_busy():
        current_position = pygame.mixer.music.get_pos()
        current_position /= 1000
        progress_var.set(current_position)
        root.after(100, update_progress)
    else:
        progress_var.set(0)

# main window
root = tk.Tk()
root.title("Music Player")
root.geometry("400x600")

# buttons
button_font = font.Font(family='Helvetica', size=16)

play_button = tk.Button(
    root, 
    text="Play", 
    command=play_song, 
    font=button_font)
play_button.pack(fill=tk.BOTH, padx=20, pady=10)

stop_button = tk.Button(
    root, 
    text="Stop", 
    command=stop_song, 
    font=button_font)
stop_button.pack(fill=tk.BOTH, padx=20, pady=10)

add_button = tk.Button(
    root, 
    text="Upload Song", 
    command=add_song,
    font=button_font)
add_button.pack(fill=tk.BOTH, padx=20, pady=10)

delete_button = tk.Button(
    root, 
    text="Delete Song", 
    command=delete_song,
    font=button_font)
delete_button.pack(fill=tk.BOTH, padx=20, pady=10)

# progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(
    root, 
    variable=progress_var, 
    maximum=100, 
    mode="determinate")
progress_bar.pack(fill=tk.BOTH, padx=20, pady=10)

# list box
list_font = font.Font(family='Helvetica', size=14)

song_list = tk.Listbox(
    root, 
    selectmode=tk.SINGLE, 
    font=list_font, 
    height=12)
song_list.pack(fill=tk.BOTH, padx=20, pady=10)

song_paths = []

# main loop
root.mainloop()
