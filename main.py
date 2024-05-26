import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage
from App.pages import StartPage, SignUpPage, CheckUserPage, CapturePage, DashboardPage, RedPage, GreenPage

names = set()

class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        self.load_names()
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, SignUpPage, CheckUserPage, CapturePage, DashboardPage, RedPage, GreenPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.save_names()
            self.destroy()

    def load_names(self):
        global names
        try:
            with open("nameslist.txt", "r") as f:
                names.update(f.read().strip().split(" "))
        except FileNotFoundError:
            pass

    def save_names(self):
        global names
        with open("nameslist.txt", "w") as f:
            f.write(" ".join(names))

if __name__ == "__main__":
    app = MainUI()
    app.iconphoto(True, tk.PhotoImage(file='pictures/icon.ico'))
    app.mainloop()