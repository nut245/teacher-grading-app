import tkinter as tk

class DrawableCanvas(tk.Canvas):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(master=self.parent)
        self.line_id = None
        self.line_points = []
        self.line_options = {}

        self.bind('<Button-1>', self.set_start)
        # constantly calls draw_line function as mouse drags across screen, only when left-click is held
        self.bind('<B1-Motion>', self.draw_line)
        self.bind('<ButtonRelease-1>', self.end_line)
        self.bind('<Button-3>', lambda event:self.delete('all'))

        self.configure(borderwidth=5, relief='sunken')

    def draw_line(self, event):
        # continually adds tuple of coordinates to line_points list
        self.line_points.extend((event.x, event.y))
        if self.line_id is not None:
            self.delete(line_id)
        # with the line of points, it creates a line using such coordinates
        # necessary to pass an empty dictionary to draw plain line
        line_id = self.create_line(self.line_points, **self.line_options)

    # begins to populate line_points list
    # otherwise line would begin with latency
    def set_start(self, event):
        self.line_points.extend((event.x, event.y))

# clears list of coordniates once left-click is released
    def end_line(self, event=None):
        self.line_points.clear()
        self.line_id = None