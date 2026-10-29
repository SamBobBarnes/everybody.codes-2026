from days.base_part import BasePart


class Part3(BasePart):
  def __init__(self):
    super().__init__(4, 3, True)

  # def run(self):
  #   input = self.get_input_lines()
  #   dict = {}
  #   for line in input:
  #     [id, _, _, time] = list(map(lambda x: x[indexOf(x, "=") + 1:], line.split(" ")))
  #     if dict.__contains__(id):
  #       dict[id] += int(time)
  #     else:
  #       dict[id] = int(time)
  #   print(dict)
