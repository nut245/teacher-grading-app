import tkinter as tk
from SettingsFile import *
from DrawableCanvasFile import DrawableCanvas

class Menu(tk.Frame):
    def __init__(self, parent):
        # window setup
        self.parent = parent
        super().__init__(master=self.parent)

        # layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        columnsTuple = (0,1,2,3)
        self.columnconfigure(columnsTuple, weight=1)

        # title of Menu
        self.Heading = tk.Label(master=self, text="Grading Program")
        self.Heading.grid(column=0, row=0, padx=PADX, pady=PADY, columnspan=len(columnsTuple), sticky='news')

        # frame where all buttons are placed
        self.buttonFrame = tk.Frame(master=self, bg=BACKGROUND_COLOR)
        self.buttonFrame.grid(column=0, row=1, sticky='news')

        # widgets
        # each button corresponds to a form, form argument follows the same name as each form class
        self.create_form_button(text="Register Student", form="Register")
        self.create_form_button(text="Create / Update Quiz", form=None)
        self.create_form_button(text="Grade Students", form="Grading")

        # self explanatory, added for boredom's sake
        self.drawableCanvas = DrawableCanvas(parent=self)
        self.drawableCanvas.grid(column=1, row=1, columnspan=len(columnsTuple)-1, sticky='news',
                                 padx=PADX, pady=PADY)
        # created to indicate to the existance of the drawable canvas to the user
        self.canvasDescription = tk.Label(master=self, text='Please draw in above area if bored - right click to clear.\n(originally meant for graph, but due to time constraints was not completed)',
                                          font=FONT, anchor='center', borderwidth=5, relief='sunken', bg=DARKER_SHADE)
        self.canvasDescription.grid(column=1, row=1, padx=PADX, pady=PADY, columnspan=len(columnsTuple)-1, sticky='ews')

    # easily create buttons to connect forms to menu
    def create_form_button(self, text, form):
        button = tk.Button(master=self.buttonFrame, text=text, command=lambda:self.parent.show_frame(form), font=FONT,
                           bg=BUTTON_COLOR)
        button.pack(expand=True, padx=PADX, pady=PADY, fill='both')