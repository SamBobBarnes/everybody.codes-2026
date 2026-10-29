from days.base_part import BasePart


class Part1(BasePart):
  def __init__(self):
    super().__init__(1, 1, True)

  def run(self):
    input = self.get_input()
    for line in input:
      print(line)
