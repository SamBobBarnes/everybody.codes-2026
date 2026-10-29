from operator import indexOf

from days.base_part import BasePart


class Part1(BasePart):
  def __init__(self):
    super().__init__(4, 1)

  def run(self):
    input = self.get_input_lines()
    dict = {}
    for line in input:
      [id, _, _, time] = list(map(lambda x: x[indexOf(x, "=") + 1:], line.split(" ")))
      if dict.__contains__(id):
        dict[id] += int(time)
      else:
        dict[id] = int(time)
    times = list(map(lambda x: x[1], dict.items()))
    times.sort()
    return sum(list(map(lambda x: (x[0] + 1) * x[1], enumerate(times))))
