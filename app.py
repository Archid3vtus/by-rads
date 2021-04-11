import tkinter as tk
from tkinter import messagebox

class Application(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master, width=480, height=360, bg="blue")
    self.master = master
    self.pack()
    self.propagate(0)
    self.create_widgets()

  def create_widgets(self):
    self.hi_there = tk.Button(self, text="Hello World", command=lambda: self.hello_world())
    self.hi_there.pack(side="top")

    self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)

    self.quit.pack(side="bottom")

  def hello_world(self, name="world"):
    return messagebox.showinfo(title="hello", message="Hello there, {}!".format(name))

  def say_hi(self):
    print("hi there, everyone!")

root = tk.Tk()
root.title("teste")
root.geometry("800x600")
root.resizable(0, 0)
app = Application(master=root)
app.mainloop()