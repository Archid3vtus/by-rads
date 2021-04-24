from tkinter import Frame, Button, TOP
from components.ResolutionDialog import ResolutionDialog

class ToolBar(Frame):
  master: Frame
  buttons: [Button] 

  def __init__(self, master: Frame):
    self.master = master
    self.buttons = []
    super().__init__(master, width=60, height=600, bg="green")
    self._add_buttons()

  def _add_buttons(self):
    self.buttons.append(Button(self, text="32", command=self._select_32x32, height=30, width=30, state="disabled"))
    self.buttons.append(Button(self, text="64", command=self._select_64x64, height=30, width=30, state="disabled"))
    self.buttons.append(Button(self, text="256", command=self._select_256_colors, height=30, width=30, state="disabled"))
    self.buttons.append(Button(self, text="32", command=self._select_32_colors, height=30, width=30, state="disabled"))
    self.buttons.append(Button(self, text="16", command=self._select_16_colors, height=30, width=30, state="disabled"))

    x, y = 0, 0
    for i in range(len(self.buttons)):
      if(i % 2 == 0):
        self.buttons[i].place(x = x, y = y, width = 30, height = 30)
        x = 30
      else:
        self.buttons[i].place(x = x, y = y, width = 30, height = 30)
        y += 30
        x = 0


  def hello_select(self):
    print("testing")

  def _select_64x64(self):
    self.master.canvas.load_image_crop((64,64))

  def _select_32x32(self):
    self.master.canvas.load_image_crop((32,32))

  def _select_256_colors(self):
    self.master.canvas.set_color_spectre(256)

  def _select_32_colors(self):
    self.master.canvas.set_color_spectre(32)

  def _select_16_colors(self):
    self.master.canvas.set_color_spectre(16)

  def change_button_state(self, index, state):
    self.buttons[index].configure(state = state)