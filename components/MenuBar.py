from tkinter import Menu

class MenuBar():

  def __init__(self, master=None):
    self.master = master
    self.menubar = Menu(self.master)
    self.add_filemenu_commands()
  
  def add_filemenu_commands(self):
    self.filemenu = Menu(self.menubar, tearoff=0)
    self.filemenu.add_command(label="Open", command=self.master.open_file)

    self.filemenu.add_separator()
    
    self.filemenu.add_command(label="Exit", command=self.master.quit)
    self.menubar.add_cascade(label="File", menu=self.filemenu)


  def donothing(self):
    print("nothing")