import tkinter as tk
import time
import winsound

def set_alarm():
    alarm_time = entry.get()
    label.config(text="Alarm Time: " + alarm_time)
    
    root.after(1000, check_alarm, alarm_time)

def check_alarm(alarm_time):
    current_time = time.strftime("%H:%M:%S")

    if current_time == alarm_time:
        label.config(text="Alarm Time: " + alarm_time + 
                     "\n- Time to wake up!")
        # Beep sound for 2 seconds when the alarm goes off
        winsound.Beep(1000, 2000) 
    else:
        root.after(1000, check_alarm, alarm_time)

# Create the main window
root = tk.Tk()
root.title("Alarm Clock")

# Create a custom font with a larger size
custom_font = ("Helvetica", 24)

# Label and Entry for setting the alarm time
label = tk.Label(
    root,
    text="Enter alarm time (HH:MM:SS):", 
    font=custom_font)
label.pack()

entry = tk.Entry(root, font=custom_font)
entry.pack()

# Button to set the alarm
button = tk.Button(
    root, 
    text="Set Alarm", 
    command=set_alarm, 
    font=custom_font)
button.pack()

# Run the main loop
root.mainloop()
