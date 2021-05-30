from tkinter import Canvas, Scrollbar, Frame, NW, BOTTOM, RIGHT, X, Y, messagebox
from PIL import Image, ImageOps, ImageTk
from components.ResolutionDialog import ResolutionDialog
from description.GrayScaleOccurrence import GrayScaleOccurrence
from description.MainDescribe import MainDescribe

class Canvas(Canvas):
  def __init__(self, master):
    master.update()
    self.parent_frame = master
    self.master = master.canvas_frame
    self.height = self.master.winfo_height() 
    self.width = self.master.winfo_width() 
    self.region_info = {}
    self.select_region_enable = False
    self.load = None
    self.load_bkp = None
    self.cropped_resolution = None
    self.gray = 256

    super().__init__(self.master, height=self.height, width=self.width, cursor="tcross", bg="grey")
    self._add_scroll_bars()
    self.bind('<Button-1>', self.select_region)
    self.bind('<Button-3>', self.unselect_region)
    self.master.region_of_interest = ""


  def load_image(self, path):
    self.load = Image.open(path)
    self.insert_image(self.load)
    self.select_region_enable = True
    self.parent_frame.toolbar.change_button_state(0, "disabled")
    self.parent_frame.toolbar.change_button_state(1, "disabled")
    self.parent_frame.toolbar.change_button_state(2, "disabled")
    self.parent_frame.toolbar.change_button_state(3, "disabled")
    self.parent_frame.toolbar.change_button_state(4, "disabled")
    self.parent_frame.toolbar.change_button_state(5, "disabled")
    self.parent_frame.toolbar.change_button_state(6, "disabled")

  def load_image_crop(self, resolution):
    self.cropped_resolution = resolution[0]
    cropped = self.load.crop((self.region_info["initial_x"], self.region_info["initial_y"], self.region_info["final_x"], self.region_info["final_y"]))
    resized = cropped.resize(resolution)
    self.load = self.load_bkp = resized
    self.insert_image(self.load)
    self.delete(self.master.region_of_interest)
    self.select_region_enable = False
    self.parent_frame.toolbar.change_button_state(0, "disabled")
    self.parent_frame.toolbar.change_button_state(1, "disabled")
    self.parent_frame.toolbar.change_button_state(2, "active")
    self.parent_frame.toolbar.change_button_state(3, "active")
    self.parent_frame.toolbar.change_button_state(4, "active")
    self.parent_frame.toolbar.change_button_state(5, "active")
    self.parent_frame.toolbar.change_button_state(6, "active")

  def set_color_spectre(self, colors_qt):
    self.gray = colors_qt
    self.load = self.load_bkp
    configured = self.load.quantize(colors_qt)
    #self.load_bkp = self.load
    self.load = configured
    self.insert_image(configured)

  def set_image_zoom(self, value):
    double_value = value/100
    zoomed = self.load.resize((int(self.load.size[0]*double_value), int(self.load.size[1]*double_value)))
    self.insert_image(zoomed)

  def classificate(self):
    #print("vamo classificar aqui")
    md = MainDescribe(0, image=self.load)
    characteristic_list = md.generate_specific(self.cropped_resolution, self.gray)
    prediction: list[int] = [0,0,0,0]
    for charac in characteristic_list:
      b = self.parent_frame.master.di.predict(md.characteristics_list(charac))
      prediction[b[0]-1] += 1
    birads = prediction.index(max(prediction)) + 1
    to_show = ""

    if birads == 1:
      to_show = "I"
    elif birads == 2:
      to_show = "II"
    elif birads == 3:
      to_show = "III"
    elif birads == 4:
      to_show = "IV"

    messagebox.showinfo("Identificado", "BIRADS {}".format(to_show))

  def equalize(self):
    #self.load = self.load_bkp
    equalized = ImageOps.equalize(self.load).quantize(self.gray)
    self.load = equalized
    self.insert_image(self.load)


  def insert_image(self, load):
    self.width, self.height = load.size[0], load.size[1]
    self.master.image = image = ImageTk.PhotoImage(load)
    self.config(heigh = self.height, width = self.width)
    super().create_image(0, 0, image=image, anchor=NW)

    # update
    self.configure(scrollregion=self.bbox("all"))

  def select_region(self, event):
    if self.select_region_enable:
      #x, y = event.x, event.y
      x, y = self.canvasx(event.x), self.canvasy(event.y)
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
    
