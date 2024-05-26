import tkinter as tk
from App.pages import RedPage

def main():
    # Create the main window (root)
    root = tk.Tk()
    root.title("RedPage Test")

    # Create an instance of RedPage
    controller = None  # You can replace this with an actual controller if needed
    red_page = RedPage(root, controller)
    red_page.pack(side="top", fill="both", expand=True)

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
