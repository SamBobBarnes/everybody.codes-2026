from days.base_part import BasePart, Point


class Part2(BasePart):
  def __init__(self):
    super().__init__(12, 2, True)
    self.rects: list[tuple[Point, Point]] = []
    self.input = self.get_input_lines()
    self.width = len(self.input[0])
    self.height = len(self.input)

  def run(self):
    for y, row in enumerate(self.input):
      for x, char in enumerate(row):
        if char == "#" and len(
          list(filter(lambda r: r[0].x <= x <= r[1].x and r[0].y <= y <= r[1].y, self.rects))) == 0:
          self.examine_rect(x, y)

    total = 0
    for r in self.rects:
      print(f"{r[0]},{r[1]}")
      width = r[1].x - r[0].x + 1
      height = r[1].y - r[0].y + 1
      total += min(width, height)

    return total

  def examine_rect(self, x1: int, y1: int):
    x2 = self.width - 1
    for i in range(x1, self.width):
      if self.input[y1][i] == "." or list(
        filter(lambda r: r[0].x <= i <= r[1].x and r[0].y <= y1 <= r[1].y, self.rects)) == 0:
        x2 = i - 1
        break
    y2 = self.height - 1
    for i in range(y1, self.height):
      if self.input[i][x1] == "." or list(
        filter(lambda r: r[0].x <= x1 <= r[1].x and r[0].y <= i <= r[1].y, self.rects)) == 0:
        y2 = i - 1
        break

    self.rects.append(tuple((Point(x1, y1), Point(x2, y2))))
