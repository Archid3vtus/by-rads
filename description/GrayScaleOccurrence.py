'''
Componentes:
  Ricardo Xavier Sena - 481694
  Yuri Cancela Braga - 553286
'''

from PIL.Image import Image
from math import sqrt, log2

class GrayScaleOccurrence:
  occurrence: list[list[int]]
  cooccurrence: list[list[float]]
  gray_spectre_matrix: list[list[int]]
  color_spectre: int
  H: float
  E: float
  C: float

  def __init__(self, color_spectre: int, image: Image) -> None:
    self.color_spectre = color_spectre
    self.gray_spectre_matrix = self.generate_gray_scale(image)
    self.occurrence = self.build_matrix(color_spectre, color_spectre)
    self.cooccurrence = self.build_matrix(color_spectre, color_spectre)
    self.H = self.E = self.C = 0

  # 0: 0,1; 45: -1,1; 90: -1, 0; 135: -1, -1
  def relate(self, radius: int, vertical: int, horizontal: int) -> None:
    for i in range(len(self.gray_spectre_matrix)):
      for j in range(len(self.gray_spectre_matrix[i])):
        if(i+(radius*vertical) > 0 and j+(radius*horizontal) > 0 and i+(radius*vertical) < len(self.gray_spectre_matrix) and j+(radius*horizontal) < len(self.gray_spectre_matrix[i])):
          self.occurrence[self.gray_spectre_matrix[i][j]][self.gray_spectre_matrix[i+(radius*vertical)][j+(radius*horizontal)]] += 1

    self.generate_cooccurrence()

    # homogeneity, entropy and contrast
    for i, c_list in enumerate(self.cooccurrence):
      for j, c in enumerate(c_list):
        self.H += c/(1 + sqrt((i-j)**2))
        if(c > 0):
          self.E += c * log2(c)
        self.C += (i-j)**2 * c
    
    self.E = -1 * self.E

  def generate_cooccurrence(self):
    sum = 0

    for i in self.occurrence:
      for j in i:
        sum += j

    for i in self.occurrence:
      aux = []
      for j in i:
        aux.append(j/sum)
      self.cooccurrence.append(aux)


  def get_haralick(self):
    return (self.H, self.E, self.C)


  def generate_gray_scale(self, image: Image) -> list[list[int]]:
    x, y = image.size
    response: list[list[int]] = []
    for i in range(x):
      aux: list[int] = []
      for j in range(y):
        aux.append(image.getpixel((i,j)))
      response.append(aux)
    return response

  def build_matrix(self, width: int, height: int) -> list[list[int]]:
    response: list[list[int]] = []
    for i in range(width):
      aux: list[int] = []
      for j in range(height):
        aux.append(0)
      response.append(aux)

    return response

  def print_cooccurrence(self) -> None:
    print("\n", self.occurrence)

      