from tkinter import Frame, LEFT, BOTH
from components.Canvas import Canvas
from components.ToolBar import ToolBar

class MainFrame(Frame):
  canvas: Canvas

  def __init__(self, master=None):
    self.master = master
    super().__init__(self.master, width=800, height=600, bg="blue")
    self.place(x = 0,y = 0,width = 800,height = 600)

    #insert toolbar
    self.toolbar = ToolBar(self)
    self.toolbar.place(x = 0, y = 0, width = 60, height = 570)

    self.insert_canvas()

  def insert_canvas(self):
    self.canvas_frame = Frame(self, width=740, height=600, bg="red")
    self.canvas_frame.place(x = 60, y = 0, width = 740, height = 570)
    self.canvas = Canvas(self)
    self.canvas.place(x = 0, y = 0, width = 740, height = 580)