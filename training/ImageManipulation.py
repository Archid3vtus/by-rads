'''
Componentes:
  Ricardo Xavier Sena - 481694
  Yuri Cancela Braga - 553286
'''

from PIL import Image
import numpy as np
from numpy.core.shape_base import block
from skimage.color import rgb2gray
from skimage.feature import hog
import matplotlib as mpl
from matplotlib.pyplot import imshow, show


class ImageManipulation:
  path_list: list[str]

  def __init__(self, path_list: list[str]) -> None:
    self.path_list = path_list

  def export_np_array(self, index: int) -> np.array:
    filename: str = self.path_list[index]
    image: Image = Image.open(filename)
    return np.array(image)

  def export_all(self) -> list[np.array]:
    response: list[np.array] = []

    for filename in self.path_list:
      image: Image = Image.open(filename)
      response.append(image)

    return response

  def to_gray_scale(self, data: np.array) -> any:
    return rgb2gray(data)

  def visualize_histogram(self, data: np.array) -> None:
    hog_features, hog_image = hog(data, visualize=True, block_norm="L2-Hys", pixels_per_cell=(16,16))
    imshow(hog_image, cmap=mpl.cm.gray)
    show()