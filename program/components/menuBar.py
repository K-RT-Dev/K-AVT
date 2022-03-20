import tkinter as tk

class MenuBar():
    def __init__(self, app):
        self.app = app
        self.menubar = tk.Menu(app.parent, foreground='black', activebackground='white', activeforeground='black')
        self.dropdownMenus = []
        app.parent.config(menu=self.menubar)

    def addDropdown(self, label, tearoff=False):
        newDropdown = tk.Menu(self.menubar, foreground='black', tearoff=tearoff)
        self.dropdownMenus.append({label:newDropdown})
        self.menubar.add_cascade(label=label, menu=newDropdown)  

    def getDropdown(self, tag):
        for dropdown in self.dropdownMenus:
            if list(dropdown.keys())[0] == tag:
                return dropdown[tag]

    def addRadioButtonGroup(self, dropdownTag, lableValueDict, variable=None, command=None):
        dropdown = self.getDropdown(dropdownTag)
        for label in list(lableValueDict.keys()):
            dropdown.add_radiobutton(label=label, value=lableValueDict[label], variable=variable, command=command) 

    def addButton(self, dropdownTag, label, command=None):
        dropdown = self.getDropdown(dropdownTag)
        dropdown.add_command(label=label, command=command)

    def getMenuBar(self):
        return self.menubar
