import numpy as np
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

class DataInterpret:
  training_data: np.array
  target: np.array
  clf: Pipeline

  def __init__(self, data: list[any]) -> None:
    aux_training_data = []
    aux_target = []
    for row in data:
      aux_target.append(int(row["id"]))
      aux_training_data.append([int(row["resolution"]), int(row["tones"]), int(row["radius"]), int(row["direction_vertical"]), int(row["direction_horizontal"]), float(row["homogeneity"]), float(row["entropy"]), float(row["contrast"])])

    self.training_data = np.array(aux_training_data)
    self.target = np.array(aux_target)
    self.clf = make_pipeline(StandardScaler(), SVC(kernel="rbf", gamma="auto"))
    pass

  def train(self) -> None:
    self.clf.fit(self.training_data, self.target)

  def predict(self, data) -> list[int]:
    return self.clf.predict([data])

  def confusion_matrix(self, true, pred, labels=None):
    return confusion_matrix(true, pred, labels=labels)

