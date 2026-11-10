from days.base_part import BasePart, Point


class Ghost:
  def __init__(self, pos: Point, dir: int):
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

  def move(self, walls: list[list[bool]]) -> tuple[Point, bool]:
    new_pos = Point(self.pos.x, self.pos.y)
    collision = False
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
      collision = True
    else:
      self.pos = new_pos
    return tuple((self.pos, collision))


class Part1(BasePart):
  def __init__(self):
    super().__init__(10, 1)
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
        new_pos, collision = g.move(self.map)
        if positions.get(new_pos.to_string()) is None:
          positions[new_pos.to_string()] = [i]
        else:
          positions[new_pos.to_string()].append(i)
        if collision:
          total_collisions += 1
      # print("moves")
      overlaps = list(filter(lambda x: len(x[1]) > 1, positions.items()))
      for _, gl in overlaps:
        collisions = len(gl)
        total_collisions += collisions
        for i in gl:
          self.ghosts[i].turn_around()
      # print("overlaps")

    return total_collisions
