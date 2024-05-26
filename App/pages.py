import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox, PhotoImage
from .create_dataset import start_capture
from .create_classifier import train_classifier
from .Detector import detect

from talking import *

names = set()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='pictures/homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font, fg="#263942")
        label.grid(row=0, sticky="ew")

        button1 = tk.Button(self, text="   Sign up  ", fg="#263942", bg="#ffffff", command=lambda: self.controller.show_frame("SignUpPage"))
        button2 = tk.Button(self, text="   Login  ", fg="#263942", bg="#ffffff", command=lambda: self.controller.show_frame("CheckUserPage"))
        button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)

        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=0, ipady=3, ipadx=32)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.controller.save_names()
            self.controller.destroy()

class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", fg="#263942", bg="#ffffff", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#263942", bg="#ffffff", command=self.start_training)
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#263942", bg="#ffffff")
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)

    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["CheckUserPage"].refresh_names()
        self.controller.show_frame("CapturePage")

    def clear(self):
        self.user_name.delete(0, 'end')

class CheckUserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Enter your username", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), fg="#263942", bg="#ffffff")
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear,fg="#263942", bg="#ffffff")
        self.menuvar = tk.StringVar(self)
        self.menuvar.set('')
        self.buttonext = tk.Button(self, text="Next", command=self.next_foo, fg="#263942", bg="#ffffff")
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)

    def next_foo(self):
        if self.user_name.get() == 'None':
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.user_name.get()
        self.controller.show_frame("DashboardPage")  

    def clear(self):
        self.user_name.delete(0, 'end')

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class CapturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#263942", bg="#ffffff", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#263942", bg="#ffffff", command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "300 pictures will be captured")
        self.numimglabel.config(text="Captured Images = " + str(start_capture(self.controller.active_name)))

    def trainmodel(self):
        train_classifier(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained")
        self.controller.show_frame("StartPage")

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Dashboard", font=self.controller.title_font, fg="#263942")
        self.label.pack(side="top", fill="x", pady=10)
        self.name_label = tk.Label(self, text="Name: ", font='Helvetica 12 bold')
        self.name_label.pack(pady=5)
        self.face_label = tk.Label(self, text="Recognized Faces: ", font='Helvetica 12 bold')
        self.face_label.pack(pady=5)
        self.button = tk.Button(self, text="Login", command=self.start_recognition, fg="#263942", bg="#ffffff")
        self.button.pack(pady=20)
        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage"), fg="#263942", bg="#ffffff")
        self.back_button.pack()

    def start_recognition(self):
        username = detect(self.controller.active_name, timeout=5)
        if username == 'pnw':
            self.controller.show_frame("RedPage")
            introduction(username)
        elif username == 'pnwkrdsup':
            self.controller.show_frame("GreenPage")
            introduction(username)
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Personalize Dashbaords

class RedPage(tk.Frame): # Red dashbaord
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg_color = "red"
        self.configure(bg=self.bg_color)
        
        # Create and pack time_label
        self.time_label = tk.Label(self, font=("Helvetica", 12), bg=self.bg_color)
        self.time_label.pack(side=tk.TOP, pady=5)

        # Create and pack weather_label
        self.weather_label = tk.Label(self, font=("Helvetica", 12), bg=self.bg_color)
        self.weather_label.pack(side=tk.TOP, pady=5)

        # Title frame
        title_frame = tk.Frame(self, bg=self.bg_color)
        title_frame.pack(pady=20)

        # Title label
        title_label = tk.Label(title_frame, text="Personal Dashboard", font=("Helvetica", 20), bg=self.bg_color)
        title_label.pack()

        # Header frame
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(pady=20)

        # Weather section
        weather_frame = tk.Frame(header_frame, bg=self.bg_color)
        weather_frame.pack(side=tk.LEFT, padx=20)

        weather_icon_image = Image.open("pictures/weather_icon.png")  # Replace with your icon path
        weather_icon_image = weather_icon_image.resize((50, 50), Image.Resampling.LANCZOS)
        weather_icon = ImageTk.PhotoImage(weather_icon_image)
        weather_icon_label = tk.Label(weather_frame, image=weather_icon, bg=self.bg_color)
        weather_icon_label.pack(side=tk.TOP, pady=5)

        weather_label = tk.Label(weather_frame, text="", font=("Helvetica", 16), bg=self.bg_color)
        weather_label.pack(side=tk.TOP, pady=5)

        # Clock section
        clock_frame = tk.Frame(header_frame, bg=self.bg_color)
        clock_frame.pack(side=tk.LEFT, padx=20)

        clock_icon_image = Image.open("pictures/clock_icon.png")  # Replace with your icon path
        clock_icon_image = clock_icon_image.resize((50, 50), Image.Resampling.LANCZOS)
        clock_icon = ImageTk.PhotoImage(clock_icon_image)
        clock_icon_label = tk.Label(clock_frame, image=clock_icon, bg=self.bg_color)
        clock_icon_label.pack(side=tk.TOP, pady=5)

        time_label = tk.Label(clock_frame, text="", font=("Helvetica", 16), bg=self.bg_color)
        time_label.pack(side=tk.TOP, pady=5)

        # To-do list frame
        todo_frame = tk.Frame(header_frame, bg=self.bg_color)
        todo_frame.pack(side=tk.LEFT, padx=20)

        # To-do list title
        todo_title = tk.Label(todo_frame, text="To-Do List", font=("Helvetica", 20), bg=self.bg_color)
        todo_title.pack(pady=10)

        # To-do list items
        todos = ["Breakfast", "Shower", "Gym", "Project001"]
        todo_vars = []

        for todo in todos:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(todo_frame, text=todo, variable=var)
            chk.pack(anchor=tk.W, pady=2)
            todo_vars.append(var)

        self.talkbutton = tk.Button(self, text="Talk", fg="#263942", bg="#ffffff", command=self.listening)
        self.talkbutton.pack(side=tk.LEFT, padx=10, pady=10)

        # Start updating time and weather
        self.update_time()
        self.update_weather()

    def update_time(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.config(text=now)
        self.after(1000, self.update_time)

    def update_weather(self):
        weather = self.get_weather()
        self.weather_label.config(text=f"{weather['temperature']} - {weather['condition']}")
        self.after(3600000, self.update_weather)

    def get_weather(self):
        # Replace with real API call
        # response = requests.get('your_api_url')
        # data = response.json()
        # For now, return dummy data
        return {
            "temperature": "20°C",
            "condition": "Sunny"
        }

    def listening(self):
        while True:
            # Get user's question through voice input
            speech = recognize_speech_from_mic()

            # Check if speech is recognized
            if not speech:
                continue

            if "jarvis" in speech.lower():
                # Get response from OpenAI based on the speech
                response = self.get_response(speech)
                # Print the response
                print("Response:", response)
                # Speak the response
                speak(response)
            elif "shut down" in speech.lower():
                # Break the loop if "shut down" is detected
                speak("Shutting down. Goodbye!")
                break
            else:
                # Continue listening for the keyword "jarvis"
                continue

    def start_listening(self):
        # Start the listening process in a separate thread to avoid blocking the GUI
        import threading
        listening_thread = threading.Thread(target=self.listening)
        listening_thread.start()

    def get_response(self, question):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print("Error:", e)
            return "Sorry, I couldn't generate a response at the moment."
        

class GreenPage(tk.Frame): # Red dashbaord
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg_color = "green"
        self.configure(bg=self.bg_color)
        
        # Create and pack time_label
        self.time_label = tk.Label(self, font=("Helvetica", 16), bg=self.bg_color)
        self.time_label.pack(side=tk.TOP, pady=5)

        # Create and pack weather_label
        self.weather_label = tk.Label(self, font=("Helvetica", 16), bg=self.bg_color)
        self.weather_label.pack(side=tk.TOP, pady=5)

        # Title frame
        title_frame = tk.Frame(self, bg=self.bg_color)
        title_frame.pack(pady=20)

        # Title label
        title_label = tk.Label(title_frame, text="Personal Dashboard", font=("Helvetica", 24), bg=self.bg_color)
        title_label.pack()

        # Header frame
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(pady=20)

        # Weather section
        weather_frame = tk.Frame(header_frame, bg=self.bg_color)
        weather_frame.pack(side=tk.LEFT, padx=20)

        weather_icon_image = Image.open("pictures/weather_icon.png")  # Replace with your icon path
        weather_icon_image = weather_icon_image.resize((50, 50), Image.Resampling.LANCZOS)
        weather_icon = ImageTk.PhotoImage(weather_icon_image)
        weather_icon_label = tk.Label(weather_frame, image=weather_icon, bg=self.bg_color)
        weather_icon_label.pack(side=tk.TOP, pady=5)

        weather_label = tk.Label(weather_frame, text="", font=("Helvetica", 16), bg=self.bg_color)
        weather_label.pack(side=tk.TOP, pady=5)

        # Clock section
        clock_frame = tk.Frame(header_frame, bg=self.bg_color)
        clock_frame.pack(side=tk.LEFT, padx=20)

        clock_icon_image = Image.open("pictures/clock_icon.png")  # Replace with your icon path
        clock_icon_image = clock_icon_image.resize((50, 50), Image.Resampling.LANCZOS)
        clock_icon = ImageTk.PhotoImage(clock_icon_image)
        clock_icon_label = tk.Label(clock_frame, image=clock_icon, bg=self.bg_color)
        clock_icon_label.pack(side=tk.TOP, pady=5)

        time_label = tk.Label(clock_frame, text="", font=("Helvetica", 16), bg=self.bg_color)
        time_label.pack(side=tk.TOP, pady=5)

        # To-do list frame
        todo_frame = tk.Frame(header_frame, bg=self.bg_color)
        todo_frame.pack(side=tk.LEFT, padx=20)

        # To-do list title
        todo_title = tk.Label(todo_frame, text="To-Do List", font=("Helvetica", 20), bg=self.bg_color)
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
        self.update_time()
        self.update_weather()

    def update_time(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.config(text=now)
        self.after(1000, self.update_time)

    def update_weather(self):
        weather = self.get_weather()
        self.weather_label.config(text=f"{weather['temperature']} - {weather['condition']}")
        self.after(3600000, self.update_weather)

    def get_weather(self):
        # Replace with real API call
        # response = requests.get('your_api_url')
        # data = response.json()
        # For now, return dummy data
        return {
            "temperature": "20°C",
            "condition": "Sunny"
        }