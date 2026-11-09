from math import floor, ceil

from days.base_part import BasePart, Point


class GrowingSpot:
  def __init__(self, pos: Point, tree_height: int):
    self.tree_height: int = tree_height
    self.pos: Point = pos
    self.shadow_height = 0

  def illuminated(self) -> bool:
    return self.tree_height > self.shadow_height


class Part1(BasePart):
  def __init__(self):
    super().__init__(8, 1)
    self.input = list(self.get_input_lines())
    self.width = len(self.input[0])
    self.height = len(self.input)
    self.map: list[list[GrowingSpot]] = []

  def run(self):
    row_count = self.height
    row_len = floor(row_count / 2)
    for i in range(0, ceil(row_count / 2)):
      x = i
      y = floor(row_count / 2) - i
      if y > 0:
        print(f"{i}: {Point(x, y)}")
        self.traverse_map(Point(x, y), row_len)
        row_len += 1

      else:
        for x1 in range(x, x + (ceil(row_count / 2) * 2), 2):
          print(f"{i}: {Point(x1, y)}")
          self.traverse_map(Point(x1, y), row_len)
          row_len -= 1

    total = 0
    for row in self.map:
      for tree in row:
        if tree.illuminated(): total += 1
    return total

  def traverse_map(self, start: Point, row_len: int):
    x = start.x
    y = start.y
    shadow_height = 0
    map_row: list[GrowingSpot] = []
    for _ in range(0, row_len + 1):  # todo: implement max row len calc
      tree = GrowingSpot(Point(x, y), int(self.input[y][x]))
      tree.shadow_height = shadow_height
      if tree.tree_height > shadow_height:
        shadow_height = tree.tree_height
      map_row.append(tree)
      x += 1
      y += 1
      shadow_height -= 1
    self.map.append(map_row)
