import tkinter as tk

class ImageLabel():
    def __init__(self, app, imge=None):
        self.app = app
        self.imageLabel = tk.Label(app.parent, image=None)
        self.imageLabel.pack()

    def setImage(self, newImage):
        self.imageLabel.configure(image=newImage)
        self.imageLabel.image = newImage