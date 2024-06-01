import tkinter as tk
from tkinter import ttk
from SettingsFile import *

# To be very honest, this code was taken from the internet and used without fill understanding
# in my defense, the implementation of scrollbars within tkinter should not be this complex
# this abomination of complexity for such simple output accentuates tkinter's shortcomings
class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(bg=BACKGROUND_COLOR)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand=False)

        self.canvas = tk.Canvas(self, yscrollcommand=vscrollbar.set, bg=DARKER_SHADE)
        self.canvas.pack(side='left', fill='both', expand=True)
        vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)
        self.interior_id = self.canvas.create_window(0, 0, window=interior, anchor='nw')

        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        
    # Track changes to the canvas and frame width and sync them,
    # also updating the scrollbar.
    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())