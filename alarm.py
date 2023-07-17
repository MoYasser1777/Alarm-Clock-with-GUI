import tkinter as tk
from tkinter import messagebox, ttk
import time
import pygame
import threading

# Play the alarm sound
def play_alarm_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play(-1) 

# Stop the alarm sound
def stop_alarm_sound():
    pygame.mixer.music.stop()

# Set the alarms
def set_alarms():
    hour = hour_var.get()
    minute = minute_var.get()
    am_pm = am_pm_var.get()

    try:
        time_obj = time.strptime(f"{hour}:{minute} {am_pm}", '%I:%M %p')
        alarm_time = time.strftime('%H:%M', time_obj)
    except ValueError:
        messagebox.showerror("Invalid Time", "Please enter a valid time.")
        return

    alarms.append(alarm_time)
    messagebox.showinfo("Alarm Set", f"Alarm set successfully for {alarm_time}!")

# Check and trigger the alarms
def check_alarms():
    while True:
        current_time = time.strftime('%H:%M')
        if current_time in alarms:
            play_alarm_sound()
            response = messagebox.askyesno("Alarm", f"Time to wake up! Alarm set for {current_time}. Snooze for 5 minutes?")
            stop_alarm_sound() 
            if response:
                alarms.remove(current_time)
                alarms.append(time.strftime('%H:%M', time.localtime(time.time() + 300)))
            else:
                alarms.remove(current_time)
        time.sleep(1)

# Update the digital clock
def update_clock():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    app.after(1000, update_clock)

# Create the main application window
app = tk.Tk()
app.title("Alarm Clock")
app.geometry("300x200")  
app.configure(bg="#FFFFFF") 

# Create and pack the widgets
label = tk.Label(app, text="Enter alarm time:", bg="#FFFFFF", fg="#000000")
label.pack(pady=10)

# Hour input
hour_frame = tk.Frame(app, bg="#FFFFFF")
hour_frame.pack()
hour_label = tk.Label(hour_frame, text="Hour:", bg="#FFFFFF", fg="#000000")
hour_label.pack(side=tk.LEFT)
hour_var = tk.StringVar()
hour_combobox = ttk.Combobox(hour_frame, width=5, textvariable=hour_var, values=[str(i).zfill(2) for i in range(1, 13)])
hour_combobox.pack(side=tk.LEFT)

# Minute input
minute_frame = tk.Frame(app, bg="#FFFFFF")
minute_frame.pack()
minute_label = tk.Label(minute_frame, text="Minute:", bg="#FFFFFF", fg="#000000")
minute_label.pack(side=tk.LEFT)
minute_var = tk.StringVar()
minute_combobox = ttk.Combobox(minute_frame, width=5, textvariable=minute_var, values=[str(i).zfill(2) for i in range(60)])
minute_combobox.pack(side=tk.LEFT)

# AM/PM selection
am_pm_frame = tk.Frame(app, bg="#FFFFFF")
am_pm_frame.pack()
am_pm_label = tk.Label(am_pm_frame, text="AM/PM:", bg="#FFFFFF", fg="#000000")
am_pm_label.pack(side=tk.LEFT)
am_pm_var = tk.StringVar(value="AM")
am_pm_combobox = ttk.Combobox(am_pm_frame, width=5, textvariable=am_pm_var, values=["AM", "PM"])
am_pm_combobox.pack(side=tk.LEFT)

button = tk.Button(app, text="Set Alarm", command=set_alarms, bg="#000000", fg="#FFFFFF")
button.pack(pady=10)

clock_label = tk.Label(app, text="", font=("Helvetica", 20), bg="#FFFFFF", fg="#000000")
clock_label.pack(pady=10)

alarms = []

update_clock()

alarm_thread = threading.Thread(target=check_alarms, daemon=True)
alarm_thread.start()

pygame.mixer.init()

app.mainloop()
