import tkinter as tk
from SettingsFile import *
from CenterFunctionFile import center

# created to display errors to user elegantly
class ErrorWindow(tk.Toplevel):
    def __init__(self, parent, text):
        self.parent = parent
        super().__init__(master=parent, bg=BACKGROUND_COLOR)
        self.title("Teacher Grading App Error >:(")
        self.geometry("400x100")
        center(self)

        self.errorLabel = tk.Label(master=self, text=text, font=FONT, bg=BACKGROUND_COLOR, 
                                   fg='red', justify='left')
        self.errorLabel.pack(expand=True, fill='both', padx=PADX, pady=PADY)

        self.destoyButton = tk.Button(master=self, text='Ok', font=FONT, bg=BUTTON_COLOR, command=self.destroy)
        self.destoyButton.pack(expand=True, fill='x', padx=PADX, pady=PADY)

        self.bind('<Escape>', self.destroy_function)

    # created to run tkinter destroy() method after being called by bind()
    # must be wrapped by outer function to deal with unnecessary event parameter
    def destroy_function(self, event = None):
        return self.destroy()