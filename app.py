from tkinter import messagebox, Tk, filedialog, Frame, RIGHT
from components.MenuBar import MenuBar
from components.Canvas import Canvas
from components.MainFrame import MainFrame

class master(Tk):
  def __init__(self):
    super().__init__()
    self.configure()
    self.add_menubar()
    self.app = MainFrame(master=self)
    self.app.mainloop()

  def configure(self):
    self.title("By Rads")
    self.geometry("800x600")
    self.resizable(0, 0)

  def add_menubar(self):
    menu_bar = MenuBar(master=self)
    self.config(menu=menu_bar.menubar)

  def open_file(self):
    path = filedialog.askopenfilename()
    if path != "":
      self.app.canvas.load_image(path)

  def open_file_to_train(self):
    path = filedialog.askopenfilenames(parent=self, title="Choose a file")

    print(path)

if __name__ == '__main__':
  master()