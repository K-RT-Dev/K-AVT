import tkinter as tk

class Frame():
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(app.parent)
        self.frame.pack()