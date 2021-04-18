from tkinter import Frame, LEFT
from components.Canvas import Canvas

class MainFrame(Frame):
  def __init__(self, master=None):
    super().__init__(master, width=800, height=600, bg="blue")
    self.master = master
    self.pack()
    self.propagate(0)
    self.insert_canvas()

  def insert_canvas(self):
    self.canvas = Canvas(self)
    self.canvas.pack(side = LEFT)

  def hello_world(self, name="world"):
    return messagebox.showinfo(title="hello", message="Hello there, {}!".format(name))

  def say_hi(self):
    print("hi there, everyone!")