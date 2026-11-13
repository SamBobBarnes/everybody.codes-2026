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
    super().__init__(12, 2)
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
    for s in self.shapes:
      total += self.most_efficient_cut(s)

    return total

  def within_shape(self, x, y):
    for s in self.shapes:
      shape_type = self.get_shape_type(s)
      if shape_type == ShapeType.Rect:
        if self.within_rect(Point(x, y), s[0], s[2]):
          return True
      if shape_type == ShapeType.NW:
        if self.within_rect(Point(x, y), s[0], s[2]) or self.within_rect(Point(x, y), s[0], s[4]):
          return True
      if shape_type == ShapeType.SW:
        if self.within_rect(Point(x, y), s[1], s[5]) or self.within_rect(Point(x, y), s[3], s[5]):
          return True
      if shape_type == ShapeType.NE:
        if self.within_rect(Point(x, y), s[1], s[3]) or self.within_rect(Point(x, y), s[1], s[5]):
          return True
      if shape_type == ShapeType.SE:
        if self.within_rect(Point(x, y), s[0], s[2]) or self.within_rect(Point(x, y), s[4], s[2]):
          return True
    return False

  def most_efficient_cut(self, s: list[Point]) -> int:
    match self.get_shape_type(s):
      case ShapeType.Rect:
        width = s[2].x - s[0].x + 1
        height = s[2].y - s[0].y + 1
        return min(width, height)
      case ShapeType.NE:
        height = max(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y, s[5].y) - min(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y,
                                                                           s[5].y)
        width = max(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x, s[5].x) - min(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x,
                                                                          s[5].x)

        height_p = s[5].y - s[1].y + 1
        width_p = s[1].x - s[3].x + 1
        return min(width, height, height_p + width_p)
      case ShapeType.NW:
        height = max(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y, s[5].y) - min(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y,
                                                                           s[5].y) + 1
        width = max(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x, s[5].x) - min(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x,
                                                                          s[5].x) + 1

        height_p = s[2].y - s[0].y + 1
        width_p = s[4].x - s[0].x + 1
        return min(width, height, height_p + width_p)
      case ShapeType.SE:
        height = max(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y, s[5].y) - min(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y,
                                                                           s[5].y) + 1
        width = max(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x, s[5].x) - min(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x,
                                                                          s[5].x) + 1

        height_p = s[2].y - s[4].y + 1
        width_p = s[2].x - s[0].x + 1
        return min(width, height, height_p + width_p)
      case ShapeType.SW:
        height = max(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y, s[5].y) - min(s[0].y, s[1].y, s[2].y, s[3].y, s[4].y,
                                                                           s[5].y) + 1
        width = max(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x, s[5].x) - min(s[0].x, s[1].x, s[2].x, s[3].x, s[4].x,
                                                                          s[5].x) + 1

        height_p = s[5].y - s[3].y + 1
        width_p = s[1].x - s[5].x + 1
        return min(width, height, height_p + width_p)

  @staticmethod
  def within_rect(put: Point, top: Point, bot: Point) -> bool:
    return (bot.x <= put.x <= top.x and top.y <= put.y <= bot.y) or (
      top.x <= put.x <= bot.x and top.y <= put.y <= bot.y)

  @staticmethod
  def get_shape_type(points: list[Point]) -> ShapeType:
    if len(points) == 4:
      return ShapeType.Rect

    if len(points) < 6:
      raise Exception(f'Cant classify shape containing [{",".join(map(lambda x: x.to_string(), points))}]', )

    a = points[2].x - points[4].x
    b = points[3].y - points[4].y
    c = points[5].x - points[4].x

    if a < 0:
      return ShapeType.SW
    if b < 0:
      return ShapeType.NW
    if c < 0:
      return ShapeType.NE
    return ShapeType.SE

  def detect_shape(self, x1: int, y1: int):
    shape: list[Point] = [Point(x1, y1)]
    # starting at top left corner
    current = Point(x1, y1)
    search_dir = Point.Direction.East
    while True:
      if (len(shape) == 4 or len(shape) == 6) and current == shape[0]:
        break
      left = self.is_magma(current.clone().move(search_dir.prev()))
      if left:
        shape.append(current.clone())
        search_dir = search_dir.prev()
        current.move(search_dir)
        continue

      lead = self.is_magma(current.clone().move(search_dir))
      if lead:
        current.move(search_dir)
        continue

      shape.append(current.clone())
      search_dir = search_dir.next()
    self.shapes.append(shape)

  def is_magma(self, p: Point):
    if p.x < 0 or p.y < 0 or p.x == self.width or p.y == self.height:
      return False
    return self.input[p.y][p.x] == '#'
