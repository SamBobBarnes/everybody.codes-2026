from days.base_part import BasePart

class Part1(BasePart):
  def __init__(self):
    super().__init__(13,1,True)

  def run(self) -> str:
    input = self.get_input_lines()
    for line in input:
      print(line)

    return "hi"