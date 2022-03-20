import tkinter as tk

class Button():
    def __init__(self, app, text, onClick=None, inFrame=False, frameSide=tk.LEFT):
        self.app = app
        self.button = tk.Button(app.parent, text=text,
                                command=lambda: onClick())
        if inFrame:
            self.button.pack(in_=inFrame, side=frameSide)
        else:
            self.button.pack()

    def setState(self, newState):
        self.button["state"] = newState

    def changeText(self, newText):
        self.button["text"] = newText