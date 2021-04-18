from tkinter import Canvas, NW
from PIL import Image, ImageTk
from components.ResolutionDialog import ResolutionDialog

WINDOW_HEIGHT = 600

class Canvas(Canvas):
  def __init__(self, master):
    print("abriu")
    self.height = 600
    self.width = 800
    self.master = master
    super().__init__(master, height=self.height, width=self.width, cursor="dot")
    self.bind('<Button-1>', self.motion)
    self.master.region_of_interest = ""

  def load_image(self, path):
    load = Image.open(path)
    resize_factor = WINDOW_HEIGHT / load.size[1]
    self.width, self.height = round(load.size[0]*resize_factor), round(load.size[1]*resize_factor)
    load_resized = load.resize((self.width, self.height))
    self.master.image = image = ImageTk.PhotoImage(load_resized)
    self.config(heigh = self.height, width = self.width)
    super().create_image(0, 0, image=image, anchor=NW)

  def motion(self, event):
    x, y = event.x, event.y
    self.draw_box({"x": x, "y": y})

  def draw_box(self, center):
    self.delete(self.master.region_of_interest)
    self.master.region_of_interest = self.create_rectangle(center["x"] - 64, center["y"] - 64, center["x"] + 64, center["y"] + 64, outline="blue", width=2)
    ResolutionDialog(self.master)
    
