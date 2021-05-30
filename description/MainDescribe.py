from description.GrayScaleOccurrence import GrayScaleOccurrence
from PIL import Image

class MainDescribe:
  path: str
  id: int
  radius: tuple[int]
  direction: tuple[tuple[int, int]]
  tone: tuple[int]
  resolution: tuple[int]

  def __init__(self, path: str, id: int) -> None:
    self.path = path
    self.id = id
    self.radius = (1,2,4,8,16)
    self.direction = ((0, 1), (-1, 1), (-1, 0), (-1, -1))
    self.tone = (32, 16)
    self.resolution = (128, 64, 32)

  def generate_characteristics(self) -> list[any]:
    response = []
    image = Image.open(self.path)

    image_mod = None
    for T in self.tone:
      image_mod = image.quantize(T)
      for R in self.resolution:
        image_mod = image_mod.resize((R, R))
        for r in self.radius:
          for d in self.direction:
            gso = GrayScaleOccurrence(T, image_mod)
            gso.relate(r, d[0], d[1])
            homogeneity, entropy, contrast = gso.get_haralick()
            response.append({"id": self.id, "name": self.path, "resolution": "{}".format(R), "tones": "{}".format(T), "radius": r, "direction_vertical": d[0], "direction_horizontal": d[1], "homogeneity": homogeneity,"entropy": entropy,"contrast": contrast})
            pass

    return response

  def characteristics_list(self, characteristics) -> list[any]:
    return [int(characteristics["resolution"]), int(characteristics["tones"]), int(characteristics["radius"]), int(characteristics["direction_vertical"]), int(characteristics["direction_horizontal"]), float(characteristics["homogeneity"]), float(characteristics["entropy"]), float(characteristics["contrast"])]

  