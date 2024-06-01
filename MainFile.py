import os
import sqlite3 as db
import tkinter as tk
from tkinter import filedialog
from SettingsFile import *

import random

import MenuFile, RegisterFile, GradingFile, PrivacyFile
from ErrorWindowFile import ErrorWindow
from CenterFunctionFile import center

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Teacher Grading App')
        self.geometry('960x540' if PHONE_SCREEN == False else "360x600")
        center(self)

        # remove line when first running code. add back after subsequent running. this is to wipe any data from the previous iterations
        os.remove("class.db")

        # creates sql database object
        self.connection = db.connect("class.db")
        # creates cursor object to execute commands on sql
        self.cursor = self.connection.cursor()

        try:
            # creating table to store student data
            self.cursor.execute("create table students(studentid integer, firstname text, lastname text, class blob, grade integer)")
        except Exception: # sqlite3.OperationalError
            pass

        # main/window layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # initialises menubar for easy access to commonly used functions to the user
        self.create_menubar()

        # instantiate return and privacy buttons that to bring user back to menu and privacy policy respectively.
        self.return_button = tk.Button(master=self, text='Return', width=20, command=lambda:self.show_frame("Menu"), padx=PADX, pady=PADY, font=FONT,
                                       bg=BUTTON_COLOR)
        self.return_button.grid(column=0, row=1, sticky='nsw', padx=PADX, pady=PADY)
        self.privacy_button = tk.Button(master=self, text="Privacy Policy", width=20, 
                                        # command for privacy button works half the time, to make it as difficult as possible to access
                                        command=lambda:self.show_frame("Privacy") if random.uniform(0,1) >= 0.5 else ErrorWindow(parent=self, text='haha didnt work'), 
                                        padx=PADX, pady=PADY, font=('calibri', 8), relief='solid', border=0, bg=BACKGROUND_COLOR)
        self.privacy_button.grid(column=0, row=1, sticky='nse', padx=PADX, pady=PADY)

        # frame setup
        self.frames = {} 

        # iterates through all forms to instantiate them and place onto main window
        for F in (MenuFile.Menu, RegisterFile.Register, GradingFile.Grading, PrivacyFile.Privacy):
            frame = F(parent=self)
            frame.configure(bg=BACKGROUND_COLOR)
            frame.Heading.configure(font=TITLE_FONT, borderwidth=5, relief='ridge', bg=HEADING_COLOR)
            # converts every key in dictionary into string of class name - for simplicity
            self.frames[str(str(str(F).split(".")[1]).split("'")[0])] = frame
            frame.grid(column=0, row=0, sticky='news')

        # shows user menu form first
        self.show_frame("Menu")

        self.configure(bg=BACKGROUND_COLOR)

    # when called, brings form, passed as cont parameter, to view 
    def show_frame(self, cont):
        # validates whether cont exists
        try:
            self.frames[cont].tkraise()
        except KeyError:
            return

        # hides return button when user is brought back to menu, vice verca for privacy policy
        if cont == "Menu":
            self.return_button.grid_forget()
            self.privacy_button.grid(column=0, row=1, sticky='nse', padx=PADX, pady=PADY)
        else:
            self.return_button.grid(column=0, row=1, sticky='nsw',padx=PADX, pady=PADY)
            self.privacy_button.grid_forget()

        # refreshes students displayed in grading form
        if cont == "Grading":
            self.frames[cont].update()

    # creates all necessary buttons within menu, seen on very top of window
    # unformately tkinter does not allow for easy abstraction of menu widgets
    # hence the obscene mess seen below
    def create_menubar(self):
        menubar = tk.Menu(master=self, background=HEADING_COLOR, fg=HEADING_COLOR)
        fileMenu = tk.Menu(menubar, tearoff=0, bg=HEADING_COLOR)
        fileMenu.add_command(label="Import Class", command=self.import_class)
        fileMenu.add_command(label="Export Class", command=self.export_class)

        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        menuMenu = tk.Menu(menubar, tearoff=0, bg=HEADING_COLOR)
        menuMenu.add_command(label="Register", command=lambda:self.show_frame("Register"))
        menuMenu.add_command(label="Grade", command=lambda:self.show_frame("Grading"))
        menuMenu.add_separator()
        menuMenu.add_command(label="Return", command=lambda:self.show_frame("Menu"))
        menubar.add_cascade(label="Menu", menu=menuMenu)

        self.config(menu=menubar)

    # used to open text files for importing and exporting databases
    def open_file(self):
        return filedialog.askopenfilename().replace('/', '//')

    # imports and converts class within text files into sqlite3 databasem
    # must follow exact formatting of data within text files to operate correctly
    def import_class(self):
        try:
            with open(self.open_file(), mode='r') as file:
                database = []
                for index, row in enumerate(file):
                    if index == 0 or index ==1:
                        continue
                    column = row.split('|')
                    for index, element in enumerate(column):
                        column[index] = element.strip()
                    database.append(tuple(column))
        except:
            return ErrorWindow(parent=self, text="invalid file type or formatting")

        # clears table to reinstantiate for new class data
        self.cursor.execute(f'''DROP TABLE students''')
        try:
            self.cursor.execute("create table students(studentid integer, firstname text, lastname text, class blob, grade integer)")
        except Exception: # sqlite3.OperationalError
            pass

        try:
            for data in database:
                yearLevel, classCharacter = data[3].split()
                # index after data represents columns specified in students database (i.e., data[0] = studentid)
                self.cursor.execute(f'''INSERT INTO students (studentid, firstname, lastname, class, grade) VALUES (?, ?, ?, ?, ?)''', 
                                    (int(data[0]) , 
                                     str(data[1]).capitalize(), 
                                     str(data[2]).capitalize(), 
                                     f"{yearLevel} {classCharacter.upper()}", 
                                     None if 'None' in data[4] else int(data[4])))
        except:
            return ErrorWindow(parent=self, text="invalid file type or formatting")

    # used for the fomatting of text files
    # finds the longest string, in terms of character length, within database
    def longest_string_function(self):
        database = self.cursor.execute('''SELECT * FROM students''')
        longest_string = '          '
        for row in database:
            for info in row:
                if len(longest_string) < len(str(info)):
                    longest_string = str(info)
        return longest_string

    # exports data within students database into text file
    def export_class(self):
        database = self.cursor.execute('''SELECT * FROM STUDENTS''')
        longest_string = self.longest_string_function()
        with open(self.open_file(), mode='w') as file:
            # leveraging python string formatting to create equal spacing between each column in text file
            # title string represents the headings over each column
            titlestring = (f"{'studentID':{len(longest_string)}s} |"
                           f"{'first name':{len(longest_string)}s} |" 
                           f"{'last name':{len(longest_string)}s} |"
                           f"{'class':{len(longest_string)}s} |" 
                           f"{'grade':{len(longest_string)}s}")
            file.write(titlestring + '\n')
            file.write('-'*len(titlestring) + '\n')

            database = self.cursor.execute('''SELECT * FROM STUDENTS''')
            for row in database:
                # leveraging the same python string formatting, but for actual data
                # each row index corresponds to piece of data per student
                # (i.e., row[0] is studentid)
                rowstring = (f"{str(row[0]):{len(longest_string)}s} |"
                             f"{str(row[1]):{len(longest_string)}s} |" 
                             f"{str(row[2]):{len(longest_string)}s} |"
                             f"{str(row[3]):{len(longest_string)}s} |" 
                             f" {str(row[4]):{len(longest_string)}s}")
                file.write(rowstring + '\n')

if __name__ == '__main__':
    app = Main()
    app.mainloop()