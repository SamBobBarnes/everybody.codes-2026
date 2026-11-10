from days.base_part import BasePart, Point
from days.day10.part2 import Ghost


class Part3(BasePart):
  def __init__(self):
    super().__init__(10, 3, True)
    self.ghosts: list[Ghost] = []
    self.map = []
    self.max_collisions = 1000000000000

  def run(self):
    input = self.get_input_lines()
    total_collisions = 0
    for y, line in enumerate(input):
      row = []
      for x, char in enumerate(line):
        if char == '#':
          row.append(True)
        else:
          row.append(False)
        match char:
          case '>':
            self.ghosts.append(Ghost(Point(x, y), 1, self.max_collisions))
          case '<':
            self.ghosts.append(Ghost(Point(x, y), 3, self.max_collisions))
          case '^':
            self.ghosts.append(Ghost(Point(x, y), 0, self.max_collisions))
          case 'v':
            self.ghosts.append(Ghost(Point(x, y), 2, self.max_collisions))

      self.map.append(row)
    self.watch.start()
    rounds = 0
    while len(self.ghosts) > 0:
      positions = {}
      for i, g in enumerate(self.ghosts):
        new_pos = g.move(self.map)
        if not g.expired():
          if positions.get(new_pos) is None:
            positions[new_pos] = [i]
          else:
            positions[new_pos].append(i)

      # print("moves")
      overlaps = list(filter(lambda x: len(x[1]) > 1, positions.items()))
      for _, gl in overlaps:
        collisions = len(gl)
        total_collisions += collisions
        for i in gl:
          self.ghosts[i].turn_around()
      # print("overlaps")
      rounds += 1

      for i in reversed(range(0, len(self.ghosts))):
        if self.ghosts[i].expired():
          self.ghosts.pop(i)
    self.watch.stop()
    return rounds
