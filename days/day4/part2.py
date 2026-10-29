from operator import indexOf

from days.base_part import BasePart


class Part2(BasePart):
  def __init__(self):
    super().__init__(4, 2)

  def run(self):
    input = self.get_input_lines()
    dict = {}
    for line in input:
      [id, _, _, time] = list(map(lambda x: x[indexOf(x, "=") + 1:], line.split(" ")))
      if dict.__contains__(id):
        dict[id]["time"] += int(time)
        dict[id]["parts"] += 1
      else:
        dict[id] = {"parts": 1, "time": int(time)}
    times = list(map(lambda x: x[1], dict.items()))
    times.sort(key=lambda x: (-x["parts"], x["time"]))
    return sum(list(map(lambda x: (x[0] + 1) * x[1]["time"], enumerate(times))))
