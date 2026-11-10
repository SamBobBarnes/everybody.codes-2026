from days.base_part import BasePart, Point


class Ghost:
  def __init__(self, pos: Point, dir: int, expire_after: int):
    self.pos = pos
    self.dir = dir
    self.collisions = 0
    self.max_collisions = expire_after

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

  def expired(self) -> bool:
    return self.collisions >= self.max_collisions

  def turn_right(self):
    self.dir = (self.dir + 1) % 4
    self.collisions += 1

  def turn_around(self):
    self.dir = (self.dir + 2) % 4
    self.collisions += 1

  def move(self, walls: list[list[bool]]) -> Point:
    new_pos = Point(self.pos.x, self.pos.y)
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
    else:
      self.pos = new_pos
    return self.pos


class Part2(BasePart):
  def __init__(self):
    super().__init__(10, 2)
    self.ghosts: list[Ghost] = []
    self.map = []
    self.max_collisions = 10000

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
