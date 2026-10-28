from days.base_part import BasePart


class Part1(BasePart):
  def __init__(self):
    super().__init__(2, 1)

  def run(self):
    input = self.get_input_lines()
    groups = []
    for line in input:
      group = [1, 2, 3, 4, 5]
      for comp in line.split(" "):
        a = int(comp[0])
        b = int(comp[2])
        lt = comp[1] == "<"
        if lt and group.index(a) > group.index(b):
          group.remove(a)
          group.insert(group.index(b), a)
        elif not lt and group.index(b) > group.index(a):
          group.remove(a)
          group.insert(group.index(b) + 1, a)
      group.reverse()
      groups.append(int(str(group).replace(", ", "").lstrip("[").rstrip("]")))
    total = 0
    for group in groups:
      print(group)
      total += group
    return total
