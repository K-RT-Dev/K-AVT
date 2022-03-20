import tkinter as tk

class CredentialsW():
    def __init__(self, app, translator):
        self.app = app
        self.translatorRef = translator

    def drawWindow(self):
        self.win = tk.Toplevel(self.app.parent)
        self.win.title("DeepL Key")
        self.win.geometry("380x60")
        
        try:
            f = open("deeplkey.txt", "r")
            defaultKey = f.read()
            f.close()
        except:
            defaultKey = ""
        
        v = tk.StringVar(self.win, value=defaultKey)
        tk.Label(self.win, text="DeepL API KEY:").grid(row=0)
        entry1 = tk.Entry(self.win, textvariable=v, width=38) 
        entry1.grid(row=0, column=1)
        tk.Button(self.win, text='OK', command=lambda: self.setDeeplKey(entry1.get())).grid(row=0, column=2, padx=8)

    # When the DeepL API Key change
    def setDeeplKey(self, newKey):
        f = open("deeplkey.txt", "w")
        f.write(newKey)
        f.close()
        self.translatorRef.setDeepLKey()
        self.destroyWindow()
    
    def destroyWindow(self):
        self.win.destroy()
        self.win = None
