from days.base_part import BasePart
from days.day9.part2 import Plant


class Part3(BasePart):
  def __init__(self):
    super().__init__(9, 3, True)

  def run(self):
    plants = list(map(lambda x: Plant(x), self.get_input_lines()))
    total = 0
    for n, plant in enumerate(plants[2:]):
      secs = 0
      while True:
        # while plant.total() < plant.limit:
        plant.grow()
        secs += 1
      total += secs

    return total
