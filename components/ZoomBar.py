'''
Componentes:
  Ricardo Xavier Sena - 481694
  Yuri Cancela Braga - 553286
'''

from tkinter import Frame, Scale, Label, HORIZONTAL

class ZoomBar(Frame):
  master: Frame
  slider: Scale
  value: int

  def __init__(self, master):
    self.master = master
    self.slider = None
    self.value = 100

    super().__init__(self.master, width = 800, height = 30, bg = "light blue")
    self.add_zoom_slider()
    self.value_label = Label(self, textvariable = self.value)
    self.value_label.place(x = 450, y = 5, width = 50, height = 20)

  def add_zoom_slider(self):
    self.slider = Scale(self, variable = self.value, from_ = 100, to = 1000, orient = HORIZONTAL, showvalue = 0, command = self._set_image_zoom)
    self.slider.place(x = 500, y = 5, width = 300, height = 20)


  def _set_image_zoom(self, event):
    self.master.canvas.set_image_zoom(int(event))