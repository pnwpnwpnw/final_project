import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests
from PIL import Image, ImageTk

color = "red"

# Function to fetch weather data (replace with real API call)
def get_weather():
    # Replace with real API call
    # response = requests.get('your_api_url')
    # data = response.json()
    # For now, return dummy data
    return {
        "temperature": "20°C",
        "condition": "Sunny"
    }

# Function to update the time
def update_time():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_label.config(text=now)
    root.after(1000, update_time)

# Function to update the weather
def update_weather():
    weather = get_weather()
    weather_label.config(text=f"{weather['temperature']} - {weather['condition']}")
    # Update every hour
    root.after(3600000, update_weather)

# Create the main window
root = tk.Tk()
root.title("Personal Dashboard")
root.attributes("-fullscreen", True)
root.configure(bg=color)

# Title frame
title_frame = tk.Frame(root, bg=color)
title_frame.grid(row=0, column=0, columnspan=3, pady=20)

# Title label
title_label = tk.Label(title_frame, text="Personal Dashboard", font=("Helvetica", 24), bg=color)
title_label.pack()

# Header frame
header_frame = tk.Frame(root, bg=color)
header_frame.grid(row=1, column=0, columnspan=3, pady=20)

# Weather section
weather_frame = tk.Frame(header_frame, bg=color)
weather_frame.grid(row=0, column=0, padx=20)

weather_icon_image = Image.open("pictures/weather_icon.png")  # Replace with your icon path
weather_icon_image = weather_icon_image.resize((50, 50), Image.Resampling.LANCZOS)
weather_icon = ImageTk.PhotoImage(weather_icon_image)
weather_icon_label = tk.Label(weather_frame, image=weather_icon, bg=color)
weather_icon_label.pack(side=tk.TOP, pady=5)

weather_label = tk.Label(weather_frame, text="", font=("Helvetica", 16), bg=color)
weather_label.pack(side=tk.TOP, pady=5)

# Clock section
clock_frame = tk.Frame(header_frame, bg=color)
clock_frame.grid(row=0, column=1, padx=20)

clock_icon_image = Image.open("pictures/clock_icon.png")  # Replace with your icon path
clock_icon_image = clock_icon_image.resize((50, 50), Image.Resampling.LANCZOS)
clock_icon = ImageTk.PhotoImage(clock_icon_image)
clock_icon_label = tk.Label(clock_frame, image=clock_icon, bg=color)
clock_icon_label.pack(side=tk.TOP, pady=5)

time_label = tk.Label(clock_frame, text="", font=("Helvetica", 16), bg=color)
time_label.pack(side=tk.TOP, pady=5)

# To-do list frame
todo_frame = tk.Frame(header_frame, bg=color)
todo_frame.grid(row=0, column=2, padx=20)

# To-do list title
todo_title = tk.Label(todo_frame, text="To-Do List", font=("Helvetica", 20), bg=color)
todo_title.pack(pady=10)

# To-do list items
todos = ["Breakfast", "Shower", "Gym", "Project001"]
todo_vars = []

for todo in todos:
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(todo_frame, text=todo, variable=var)
    chk.pack(anchor=tk.W, pady=2)
    todo_vars.append(var)

# Start updating time and weather
update_time()
update_weather()

# Main loop
root.mainloop()
