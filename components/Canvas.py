from tkinter import Canvas, Scrollbar, Frame, NW, BOTTOM, RIGHT, X, Y
from PIL import Image, ImageTk
from components.ResolutionDialog import ResolutionDialog

class Canvas(Canvas):
  def __init__(self, master):
    master.update()
    self.parent_frame = master
    self.master = master.canvas_frame
    self.height = self.master.winfo_height() 
    self.width = self.master.winfo_width() 
    self.region_info = {}
    self.select_region_enable = False

    super().__init__(self.master, height=self.height, width=self.width, cursor="tcross", bg="grey")
    self._add_scroll_bars()
    self.bind('<Button-1>', self.select_region)
    self.bind('<Button-3>', self.unselect_region)
    self.master.region_of_interest = ""


  def load_image(self, path):
    self.load = Image.open(path)
    self.insert_image(self.load)
    self.select_region_enable = True

  def load_image_crop(self, resolution):
    cropped = self.load.crop((self.region_info["initial_x"], self.region_info["initial_y"], self.region_info["final_x"], self.region_info["final_y"]))
    resized = cropped.resize(resolution)
    self.load = resized
    self.insert_image(self.load)
    self.delete(self.master.region_of_interest)
    self.select_region_enable = False
    self.parent_frame.toolbar.change_button_state(0, "disabled")
    self.parent_frame.toolbar.change_button_state(1, "disabled")
    self.parent_frame.toolbar.change_button_state(2, "active")
    self.parent_frame.toolbar.change_button_state(3, "active")
    self.parent_frame.toolbar.change_button_state(4, "active")


  def insert_image(self, load):
    print(load)
    self.width, self.height = load.size[0], load.size[1]
    self.master.image = image = ImageTk.PhotoImage(load)
    self.config(heigh = self.height, width = self.width)
    super().create_image(0, 0, image=image, anchor=NW)

    # update
    self.configure(scrollregion=self.bbox("all"))

  def select_region(self, event):
    if self.select_region_enable:
      x, y = event.x, event.y
      self.region_info = {"initial_x": x - 64, "initial_y": y - 64, "final_x": (x-64) + 128, "final_y": (y-64) + 128}
      self.draw_box({"x": x, "y": y})

  def unselect_region(self, event):
    self.delete(self.master.region_of_interest)
    self.parent_frame.toolbar.change_button_state(0, "disabled")
    self.parent_frame.toolbar.change_button_state(1, "disabled")


  def draw_box(self, center):
    self.delete(self.master.region_of_interest)
    self.master.region_of_interest = self.create_rectangle(center["x"] - 64, center["y"] - 64, center["x"] + 64, center["y"] + 64, outline="blue", width=2)
    self.parent_frame.toolbar.change_button_state(0, "active")
    self.parent_frame.toolbar.change_button_state(1, "active")

  def _add_scroll_bars(self):
    #add scroll bars
    self.scroll_x = Scrollbar(self.master, orient="horizontal", command=self.xview)
    self.scroll_x.pack(side=BOTTOM, fill=X)

    self.scroll_y = Scrollbar(self.master, orient="vertical", command=self.yview)
    self.scroll_y.pack(side=RIGHT, fill=Y)
    self.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

    self.master.bind('<Enter>', self._bound_to_mousewheel)
    self.master.bind('<Leave>', self._unbound_to_mousewheel)

  def _bound_to_mousewheel(self, event):
    self.bind_all("<MouseWheel>", self._on_mousewheel_vertical)
    self.bind_all("<Shift-MouseWheel>", self._on_mousewheel_horizontal)

  def _unbound_to_mousewheel(self, event):
    self.unbind_all("<MouseWheel>")
    self.unbind_all("<Shift-MouseWheel>")

  def _on_mousewheel_vertical(self, event):
    self.yview_scroll(int(-1*(event.delta/120)), "units")

  def _on_mousewheel_horizontal(self, event):
    self.xview_scroll(int(-1*(event.delta/120)), "units")
    
