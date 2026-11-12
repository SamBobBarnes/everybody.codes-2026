from enum import Enum

from days.base_part import BasePart, Point


class ShapeType(Enum):
  NW = 0,
  NE = 1,
  SE = 2,
  SW = 3,
  Rect = 4


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
        if char == "#" and not self.within_shape(x, y):
          self.detect_shape(x, y)

    total = 0
    for r in self.shapes:
      print(f"{r[0]},{r[1]}")
      width = r[1].x - r[0].x + 1
      height = r[1].y - r[0].y + 1
      total += min(width, height)

    return total

  def within_shape(self, x, y):
    for s in self.shapes:
      shape_type = self.get_shape_type(s)
      if shape_type == ShapeType.Rect and self.within_rect(Point(x, y), s[0], s[2]):
        return True
      if shape_type == ShapeType.NE and self.within_rect(Point(x, y), s[0], s[2]) or self.within_rect(Point(x, y), s[0],
                                                                                                      s[4]):
        return True
      if shape_type == ShapeType.SW and self.within_rect(Point(x, y), s[0], s[2]) or self.within_rect(Point(x, y), s[4],
                                                                                                      s[2]):
        return True
      if shape_type == ShapeType.NW and self.within_rect(Point(x, y), s[1], s[3]) or self.within_rect(Point(x, y), s[1],
                                                                                                      s[5]):
        return True
      if shape_type == ShapeType.SE and self.within_rect(Point(x, y), s[1], s[5]) or self.within_rect(Point(x, y), s[3],
                                                                                                      s[5]):
        return True
    return False

  @staticmethod
  def within_rect(put: Point, top: Point, bot: Point) -> bool:
    return (bot.x <= put.x <= top.x and top.y <= put.y <= bot.y) or (
      top.x <= put.x <= bot.x and top.y <= put.y <= bot.y)

  @staticmethod
  def get_shape_type(points: list[Point]) -> ShapeType:
    if len(points) == 4 or len(points) == 1:
      return ShapeType.Rect

    if len(points) < 6:
      raise Exception(f'Cant classify shape containing [{",".join(map(lambda x: x.to_string(), points))}]', )

    a = points[2].x - points[3].x
    b = points[3].y - points[4].y

    if a < 0 and b < 0:
      return ShapeType.NW
    if a < 0 < b:
      return ShapeType.SE
    if b < 0:
      return ShapeType.SW
    return ShapeType.NE

  def detect_shape(self, x1: int, y1: int):
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
