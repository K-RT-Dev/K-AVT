import tkinter as tk

class Separator():
    def __init__(self, app):
        self.app = app
        self.separator = tk.ttk.Separator(app.parent, orient='horizontal')
        self.separator.pack(fill="x")