from days.base_part import BasePart, Point


class Part2(BasePart):
  def __init__(self):
    super().__init__(12, 2, True)
    self.shapes: list[list[Point]] = []
    self.input = self.get_input_lines()
    self.width = len(self.input[0])
    self.height = len(self.input)

  def run(self):
    for y, row in enumerate(self.input):
      for x, char in enumerate(row):
        if char == "#" and len(
          list(filter(lambda r: r[0].x <= x <= r[1].x and r[0].y <= y <= r[1].y, self.shapes))) == 0:
          self.detect_continuous(x, y)

    total = 0
    for r in self.shapes:
      print(f"{r[0]},{r[1]}")
      width = r[1].x - r[0].x + 1
      height = r[1].y - r[0].y + 1
      total += min(width, height)

    return total

  def within_shape(self,x,y):
    for shape in self.shapes:
      #todo find interior with comparisons

  def detect_continuous(self, x1: int, y1: int):
    shape: list[Point] = [Point(x1, y1)]
    # starting at top left corner
    current = Point(x1, y1)
    search_dir = Point.Direction.East
    while True:
      if current == shape[0]:
        break  # back at the beginning

      lead = self.is_magma(current.clone().move(search_dir))
      left = self.is_magma(current.clone().move(search_dir.prev()))

      # if lead and not left:  # keep going
      if left:  # concave corner, turn left
        shape.append(current.clone())
        search_dir = search_dir.prev()
      elif not lead and not left:  # convex corner, turn right
        shape.append(current.clone())
        search_dir = search_dir.next()

      current.move(search_dir)
      if not self.is_magma(current):  # we have stepped off, turn right
        current.move(search_dir.reverse())
        if current == shape[0]:
          break  # back at the beginning
        search_dir.next()
        current.move(search_dir)

  def is_magma(self, p: Point):
    return self.input[p.y][p.x] == '#'
