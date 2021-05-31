import math
import time
from training.DataInterpret import DataInterpret
from description.CsvUtil import CsvUtil
from description.MainDescribe import MainDescribe
from tkinter import messagebox, Tk, filedialog, Frame, RIGHT, simpledialog
from training.ImageManipulation import ImageManipulation
from components.MenuBar import MenuBar
from components.Canvas import Canvas
from components.MainFrame import MainFrame
from random import shuffle

class master(Tk):
  def __init__(self):
    super().__init__()
    self.load_data_csv()
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
    start = time.time()
    path: list[str] = filedialog.askopenfilenames(parent=self, title="Choose a file")
    birads_type:int = simpledialog.askinteger("Input", "What's the BIRADS type?", parent=self)
    images: list[str] = []

    for file in path:
      if(file.find(".png") != -1):
        images.append(file)

    shuffle(images)
    list_portion_number: int = math.ceil(len(images) * 0.75)
    data_store: list[str] = images[0: list_portion_number]
    no_store: list[str] = images[list_portion_number: len(path)]

    image_characteristics = []
    for image in data_store:
      md = MainDescribe(birads_type, path=image)
      image_characteristics = image_characteristics + md.generate_characteristics()

    csv_data = CsvUtil("{}_calculated.csv".format(birads_type), ["id", "name", "resolution", "tones", "radius", "direction_vertical", "direction_horizontal", "homogeneity", "entropy", "contrast"])
    csv_nodata = CsvUtil("{}_ignored.csv".format(birads_type), ["name"])
    csv_data.write_dict(image_characteristics)
    csv_nodata.write_str_list(no_store)
    print("done!")
    end = time.time()
    print("Tempo de execução para crianção de métricas: {}".format(end - start, ".2f"))

  def load_data_csv(self):
    start = time.time()
    data = []
    for i in [1,2,3,4]:
      csv = CsvUtil("{}_calculated.csv".format(i), None)
      try:
        data = data + csv.open_dic()
      except:
        pass

    if len(data) > 0:
      self.di = DataInterpret(data)
      self.di.train()
      end = time.time()
      print("Tempo de execução do treinamento: {}".format(end - start, '.2f'))

  def identify(self):
    start = time.time()
    #path = filedialog.askopenfilename()
    path_list = self.get_ignored()
    true = []
    pred = []
    for path in path_list:
      md = MainDescribe(0, path=path["name"])
      true.append(int(path["id"]))
      a = md.generate_characteristics()

      prediction: list[int] = [0,0,0,0]
      for characteristic in a:
        b = self.di.predict(md.characteristics_list(characteristic))
        prediction[b[0]-1] += 1
      pred.append(prediction.index(max(prediction)) + 1)

    confusion = self.di.confusion_matrix(true, pred, labels=[1,2,3,4])

    # sensibilidade média
    sen = 0
    for hit_list in confusion:
      for hit in hit_list:
        sen += hit / 100

    # especificidade média
    esp = 1
    for (i, hit_list) in enumerate(confusion):
      for (j, hit) in enumerate(hit_list):
        if(i != j):
          esp -= hit / 300

    # acuracia
    acc = self.di.accuracy_score(true, pred)

    end = time.time()

    print("Tempo de execução da identificação: {}".format(end - start, ".2f"))
    messagebox.showinfo("Resultados", "Matriz de confusão:\n{}\n\nSensibilidade média: {}\nEspecificidade média: {}\nPrecisão: {}\n".format(confusion, sen, esp, acc))

  def get_ignored(self):
    data = []

    for i in [1,2,3,4]:
      csv = CsvUtil("{}_ignored.csv".format(i), None)
      file_list = []
      for file in csv.open_dic():
        file_list.append({"id": i, "name": file["name"]})
      data = data + file_list
    
    return data

if __name__ == '__main__':
  master()