import tkinter as tk


class Label():
    def __init__(self, app, text=None):
        self.app = app
        self.label = tk.Label(app.parent, text=text)
        self.label.pack()

    def setLabelText(self, newText):
        self.label["text"] = newText