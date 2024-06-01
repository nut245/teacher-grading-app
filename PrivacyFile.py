import tkinter as tk
from SettingsFile import *

import os
# to get the location of the current python file
basedir = os.path.dirname(os.path.abspath(__file__))
# to join it with the filename
categorization_file = os.path.join(basedir,'Privacy.txt')

class Privacy(tk.Frame):
    def __init__(self, parent):
        # window setup
        self.parent = parent
        super().__init__(master=self.parent)

        # layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        columnsTuple = (0,)
        self.columnconfigure(columnsTuple, weight=1)

        self.Heading = tk.Label(master=self, text="Privacy Policy")
        self.Heading.grid(column=0, row=0, padx=PADX, pady=PADY, columnspan=len(columnsTuple), sticky='news')

        # using text widget for easy access to scrollable text
        self.textWidget = tk.Text(master=self, bg=BACKGROUND_COLOR)
        self.textWidget.grid(column=0, row=1, sticky='news')

        # grabs text from privacy text file to display to user
        self.privacyText = ''
        with open(categorization_file, 'r') as file:
            for line in file:
                self.privacyText += line

        self.textWidget.insert(tk.END, self.privacyText)
        # text files are automatically editable
        # 'disabled' disallowes users from manipulating the text
        self.textWidget.configure(state='disabled')