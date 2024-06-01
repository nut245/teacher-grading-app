import tkinter as tk
from tkinter import ttk
import random
from SettingsFile import *

from ErrorWindowFile import ErrorWindow
from VerticalScrolledFrameFile import VerticalScrolledFrame

class Grading(tk.Frame):
    def __init__(self, parent):
        # window setup
        self.parent = parent
        super().__init__(master=self.parent)
        # instantiating a list of students to use to display later
        self.students = []

        # layout
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=1)
        columnsTuple = (0,1,2,3)
        self.columnconfigure(columnsTuple, weight=1)

        # frame to store the title of the form
        self.Heading = tk.Label(master=self, text="Grade Students")
        self.Heading.grid(column=0, row=0, padx=PADX, pady=PADY, columnspan=len(columnsTuple), sticky='news')

        # creating frame that displays all titles of the different columns
        self.columnHeadingFrame = tk.Frame(self, bg=DARKER_SHADE)
        self.columnHeadingFrame.grid(column=0, row=1, columnspan=len(columnsTuple), sticky='news', padx=PADX, pady=PADY)

        # creating scrollable frame to place all StudentRow widgets/objects into
        self.studentsFrame = VerticalScrolledFrame(self)
        self.studentsFrame.grid(column=0, row=2, columnspan=len(columnsTuple), sticky='news')

        # widgets

        # displayed three columns found within the database
        self.create_column_heading(text='Students')
        self.create_column_heading(text='Year Level / Class')
        self.create_column_heading(text='Grades')

        # lazily implemented random button that generates random greates for all students
        self.randomButton = tk.Button(master=self.columnHeadingFrame, text='Gernerate Random Grades', command=self.generate_random_grades,
                                      font=FONT, bg=BUTTON_COLOR)
        self.randomButton.pack(side='right', padx=PADX, pady=PADY)

        # commit button that saves all student grades into the database
        self.commitButton = tk.Button(master=self, text='Commit', command=self.commit,
                                       font=FONT, bg=BUTTON_COLOR)
        self.commitButton.grid(column=1, row=3, columnspan=len(columnsTuple)-1, sticky='news', padx=PADX, pady=PADY)

        # runs update method to display new class after import button is pressed
        self.refreshButton = tk.Button(master=self, text='Refresh', command=self.update,
                                       font=FONT, bg=BUTTON_COLOR)
        self.refreshButton.grid(column=0, row=3, sticky='news', padx=PADX, pady=PADY)

    # self explanatory
    def generate_random_grades(self):
        for student in self.students:
            student.grade.delete(0, 'end')
            student.grade.insert(0, random.randint(1, 100))

    # runs some checks for validation, before finally saving to database
    def commit(self):
        for studentID, student in enumerate(self.students):
                if not student.grade.get():
                    continue # grade does not exist, however is not considered an error. As grade can be None
                try:
                    if int(student.grade.get()) < 0 or int(student.grade.get()) > 100:
                        return ErrorWindow(parent=self, text="must be within range 0-100")
                except ValueError:
                    return ErrorWindow(parent=self, text="grade must be integer")

                self.parent.cursor.execute('''UPDATE STUDENTS SET GRADE = ? WHERE studentid = ?''', (int(student.grade.get()), studentID+1))

    # run every time the Grading File is displayed to the user, this is to refresh the students within the database
    def update(self):
        # this is to clear all the students from the student list i had previously
        for student in self.students:
            student.destroy()
        self.students = []

        # accessing database again
        data = self.parent.cursor.execute('''SELECT * FROM STUDENTS''')

        # repopulating students list, by appending a StudentRow object into with (with all necessary arguments passed)
        for row in data:
            # whenever you see  row[some number]  , imagine that is the information within each column
            # row[0] = studentID, row[1] = firstname, row[2] = lastname, row[3] = year level/class, row[4] = grade
            self.students.append(StudentRow(parent=self.studentsFrame.interior, name=f'{row[1]} {row[2]}', yearLevel=row[3]))
            self.students[-1].pack(fill='x')

    # done to make many column headings without duplicating code
    def create_column_heading(self, text):
        tk.Label(master=self.columnHeadingFrame, text=text, 
                 width=(STUDENT_COLUMN_WIDTH if text == 'Students' else YEARLEVEL_COLUMN_WIDTH if text == 'Year Level / Class' else 0),
                 wraplength=100, font=FONT, justify='left', anchor='w', bg=DARKER_SHADE).pack(side='left', fill='both')

# this is the class i use to easily create student objects to duplicate - dependant on how many students there are in the database
# bad coding practise to keep multiple classes within same file
# however, it seemed dramatic to seperate this code, as it is only used here
class StudentRow(tk.Frame):
    def __init__(self, parent, name, yearLevel):
        self.parent = parent
        self.name = name
        super().__init__(master=parent)

        # has a student name label
        self.student = tk.Label(master=self, text=name, width=STUDENT_COLUMN_WIDTH, wraplength=190,
                                justify='left', anchor='w', font=FONT, bg=HEADING_COLOR)
        self.student.pack(side='left')

        # year level label
        self.yearLevel = tk.Label(master=self, text=yearLevel, width=YEARLEVEL_COLUMN_WIDTH,
                                  justify='left', anchor='w', font=FONT, bg=HEADING_COLOR)
        self.yearLevel.pack(side='left')

        # grade entry, (to access information from entry use [ student.grade.get() ])
        self.grade = tk.Entry(master=self, font=FONT)
        self.grade.pack(side='left', expand=True, fill='both')
