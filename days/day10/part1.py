from days.base_part import BasePart, Point


class Ghost:
  def __init__(self, pos: Point, dir: int):
    self.collisions = 0
    self.pos = pos
    self.dir = dir

  def __str__(self):
    match self.dir:
      case 0:
        dir_str = '^'
      case 1:
        dir_str = '>'
      case 2:
        dir_str = 'v'
      case 3:
        dir_str = '<'
    return f"[{self.pos.x},{self.pos.y}] {dir_str}"

  def turn_right(self):
    self.dir = (self.dir + 1) % 4

  def turn_around(self):
    self.dir = (self.dir + 2) % 4

  def move(self, walls: list[list[bool]]) -> Point:
    new_pos = self.pos
    match self.dir:
      case 0:
        new_pos.y -= 1
      case 1:
        new_pos.x += 1
      case 2:
        new_pos.y += 1
      case 3:
        new_pos.x -= 1

    if walls[new_pos.y][new_pos.x]:
      self.turn_right()
      self.collisions += 1
    else:
      self.pos = new_pos
    return self.pos


class Part1(BasePart):
  def __init__(self):
    super().__init__(10, 1, True)
    self.ghosts: list[Ghost] = []
    self.map = []

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
            self.ghosts.append(Ghost(Point(x, y), 1))
          case '<':
            self.ghosts.append(Ghost(Point(x, y), 3))
          case '^':
            self.ghosts.append(Ghost(Point(x, y), 0))
          case 'v':
            self.ghosts.append(Ghost(Point(x, y), 2))

      self.map.append(row)
    rounds = 10

    for _ in range(0, rounds):
      positions = {}
      for i, g in enumerate(self.ghosts):
        new_pos = g.move(self.map)
        if positions.get(new_pos.to_string()) is None:
          positions[new_pos.to_string()] = [i]
        else:
          positions[new_pos.to_string()].append(i)

      overlaps = list(filter(lambda x: len(x[1]) > 1, positions.items()))
      for _, gl in overlaps:
        collisions = len(gl)
        total_collisions += collisions
        for i in gl:
          self.ghosts[i].turn_around()

    return sum(map(lambda x: x.collisions, self.ghosts)) + total_collisions
