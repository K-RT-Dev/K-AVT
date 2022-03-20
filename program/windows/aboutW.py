import tkinter as tk
import webbrowser

class AboutW():
    def __init__(self, app):
        self.app = app

    def drawWindow(self):
        self.win = tk.Toplevel(self.app.parent)
        self.win.title("About")
        self.win.geometry("400x150")

        tk.Label(self.win, text="This is an open source tool for translation through image recognition.").grid(row=0)
        tk.Label(self.win, text="For more information visit:").grid(row=1)
        link = tk.Label(self.win, text="www.tutorialspoint.com",font=('Helveticabold', 10), fg="blue", cursor="hand2")
        link.grid(row=2)
        link.bind("<Button-1>", lambda e: self.callback("www.theerogereviewer.wordpress.com/k-avt"))
        tk.Label(self.win, text="By K").grid(row=3)

    def destroyWindow(self):
        self.win.destroy()
        self.win = None

    def callback(self, url):
        webbrowser.open_new(url)