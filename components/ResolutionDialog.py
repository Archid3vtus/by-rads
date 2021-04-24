from tkinter import *

class ResolutionDialog():
  def __init__(self, parent):
    self.parent = parent
    self.win = Toplevel(self.parent)
    self.config()

  def config(self):
    self.height = 50
    self.width = 200
    self.win.title('Select a resolution')
    self.win.transient(self.parent)
    self.win.grab_set()
    self.win.geometry("{}x{}".format(self.width,self.height))
    self.win.focus()
    self.center()
    self.add_butons()

  def center(self):
    x = self.parent.winfo_rootx()
    y = self.parent.winfo_rooty()
    height = self.parent.winfo_height()
    width = self.parent.winfo_width()
    geom = "+%d+%d" % ((x+(width/2))-self.width/2, y+height/3)
    self.win.geometry(geom)

  def select_64(self):
    print("64")
    return

  def select_32(self):
    #print("32")
    self.parent.canvas.load_image_crop("32x32")
    return

  def add_butons(self):
    bottom_frame = Frame(self.win)
    bottom_frame.pack(side=BOTTOM)
    Button(bottom_frame, text="64x64", command=self.select_64).pack(side=LEFT)
    Button(bottom_frame, text="32x32", command=self.select_32).pack(side=LEFT)
