from tkinter import messagebox, Tk, filedialog, Frame, RIGHT
from components.MenuBar import MenuBar
from components.Canvas import Canvas

class Application(Frame):
  def __init__(self, master=None):
    super().__init__(master, width=800, height=600, bg="blue")
    self.master = master
    self.pack()
    self.propagate(0)
    self.insert_canvas()

  def insert_canvas(self):
    self.canvas = Canvas(self)
    self.canvas.pack(side = RIGHT)

  def hello_world(self, name="world"):
    return messagebox.showinfo(title="hello", message="Hello there, {}!".format(name))

  def say_hi(self):
    print("hi there, everyone!")

class master(Tk):
  def __init__(self):
    super().__init__()
    self.configure()
    self.add_menubar()
    self.app = Application(master=self)
    self.app.mainloop()

  def configure(self):
    self.title("teste")
    self.geometry("800x600")
    self.resizable(0, 0)

  def add_menubar(self):
    menu_bar = MenuBar(master=self)
    self.config(menu=menu_bar.menubar)

  def open_file(self):
    path = filedialog.askopenfilename()
    if path != "":
      print(path)
      self.app.canvas.load_image(path)


#root = master()
#app = Application(master=root)
#app.mainloop()

master()