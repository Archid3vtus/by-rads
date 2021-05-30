import csv

class CsvUtil:
  file_name: str
  fieldnames: list[str]
  directory: str

  def __init__(self, file_name: str, fieldnames: list[str]) -> None:
    self.file_name = file_name
    self.fieldnames = fieldnames
    self.directory = "data/"

  def write_dict(self, dict: any) -> None:
    with open("{}{}".format(self.directory, self.file_name), 'w', newline="") as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
      writer.writeheader()
      for item in dict:
        writer.writerow(item)

  def write_str_list(self, str_list: list[str]) -> None:
    with open("{}{}".format(self.directory, self.file_name), 'w', newline="") as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
      writer.writeheader()
      for item in str_list:
        writer.writerow({self.fieldnames[0]: item})

  def open_dic(self) -> list[any]:
    response: any = []

    with open("{}{}".format(self.directory, self.file_name), newline="") as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        response.append(row)

    return response