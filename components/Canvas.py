from tkinter import Canvas, NW
from PIL import Image, ImageTk

class Canvas(Canvas):
  def __init__(self, master):
    print("abriu")
    self.HEIGHT = 600
    self.WIDTH = 800
    super().__init__(master, height=self.HEIGHT, width=self.WIDTH)

  def load_image(self, path):
    load = Image.open(path)
    resize_factor = self.HEIGHT / load.size[1]
    print(resize_factor)
    load_resized = load.resize((round(load.size[0]*resize_factor), round(load.size[1]*resize_factor)))
    print('width: {}\nheight: {}'.format(load.size[0], load.size[1]))
    self.master.image = image = ImageTk.PhotoImage(load_resized)
    super().create_image(0, 0, image=image, anchor=NW)
    
