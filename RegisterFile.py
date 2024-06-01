import tkinter as tk
from SettingsFile import *
from ErrorWindowFile import ErrorWindow

class Register(tk.Frame):
    def __init__(self, parent):
        # window setup
        self.parent = parent
        super().__init__(master=self.parent)
        self.studentid = 1

        # layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        columnsTuple = (0,)
        self.columnconfigure(columnsTuple, weight=1)

        self.Heading = tk.Label(master=self, text="Register Student")
        self.Heading.grid(column=0, row=0, padx=PADX, pady=PADY, columnspan=len(columnsTuple), sticky='news')

        # to place all input widgets within
        self.widgetFrame = tk.Frame(master=self, bg=BACKGROUND_COLOR)
        self.widgetFrame.grid(column=0, row=1, sticky='news')

        self.widgetFrame.columnconfigure((0,1), weight=1)
        self.widgetFrame.rowconfigure((0,1,2), weight=1)


        # widgets
        self.firstname = InputWidget(parent=self.widgetFrame, text='First Name:')
        self.firstname.grid(column=0, row=0, sticky='news', padx=PADX, pady=PADY)
        self.lastname = InputWidget(parent=self.widgetFrame, text='Last Name:')
        self.lastname.grid(column=1, row=0, sticky='news', padx=PADX, pady=PADY)
        self.studentClass = InputWidget(parent=self.widgetFrame, text='Class:')
        self.studentClass.grid(column=0, row=1, columnspan=2, sticky='news', padx=PADX, pady=PADY)

        self.widgets = [self.firstname, self.lastname, self.studentClass]

        self.submitButton = tk.Button(master=self.widgetFrame, text='Submit', command=self.submit, font=FONT,
                                      bg=BUTTON_COLOR)
        self.submitButton.grid(column=0, row=2, padx=PADX, pady=PADY, columnspan=2, sticky='news')

    # runs many checks and validation amongst all input widgets to ensure data exists, is of the correct type, and within proper range 
    def submit(self):
        try:
            # as student class is an integer and character, must ensure both exist seperately
            # utilising built in python split function to do so
            studentClass = self.studentClass.entry.get().split()
            # studentClass[0] is year level, and studentClass[1] is class
            if not (self.firstname.entry.get() and self.lastname.entry.get() and studentClass[0] and studentClass[1]):
                return ErrorWindow(parent=self, text='must fill in all regions')
        except IndexError:
            return ErrorWindow(parent=self, text='must seperate year level and class with space character')
        
        if not self.firstname.entry.get().isalpha() or not self.lastname.entry.get().isalpha():
            return ErrorWindow(parent=self, text='name must only contain letters')

        if not (studentClass[0].isnumeric() and studentClass[1].isalpha() and len(studentClass[1]) == 1):
            return ErrorWindow(parent=self, text='year level must be number and class must be a letter')

        studentClass = f"{studentClass[0]} {studentClass[1].upper()}"
        
        # once all validation is passed, student data is placed into database
        self.parent.cursor.execute(f'''INSERT INTO STUDENTS (studentid, firstname, lastname, class, grade) VALUES (?, ?, ?, ?, ?)''', 
                                   (self.studentid ,self.firstname.entry.get().capitalize(), self.lastname.entry.get().capitalize(), studentClass, None))
        self.studentid += 1

        # clears all text within input widgets
        for widget in self.widgets:
            widget.entry.delete(0, 'end')
            
        # removes focus from wherever user had previously been typing
        self.parent.focus()

# custom class that groups a label for text and entry together
# only used within register form
# however, still bad practise to group many classes into one file
class InputWidget(tk.Frame):
    def __init__(self, parent, text: str) -> None:
        self.parent = parent
        self.text = text
        self.outputVariable = ''

        super().__init__(master=self.parent)

        self.label = tk.Label(master=self, text=text, font=FONT, bg=BUTTON_COLOR)
        self.label.pack(fill='both', expand=True)

        self.entry = tk.Entry(master=self, font=FONT)
        self.entry.pack(fill='both', expand=True, padx=PADX, pady=PADY)

        self.configure(borderwidth=5, relief='groove', bg=DARKER_SHADE)