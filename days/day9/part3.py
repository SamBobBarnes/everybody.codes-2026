from days.base_part import BasePart
from days.day9.part2 import Plant


class Part3(BasePart):
  def __init__(self):
    super().__init__(9, 3)

  def run(self):
    plants = list(map(lambda x: Plant(x), self.get_input_lines()))
    total = 0
    for plant in plants:
      secs = 1
      plant.grow()
      while plant.total() < plant.limit:
        secs_to_next = plant.next_split_in()
        plant.grow(secs_to_next)
        secs += secs_to_next
      total += secs

    return total
