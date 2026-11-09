from math import floor, ceil

from days.base_part import BasePart, Point


def replace_char(text: str, index: int, new_char: str) -> str:
  return text[:index] + new_char + text[index + 1:]


class GrowingSpot:
  def __init__(self, pos: Point, tree_height: int):
    self.tree_height: int = tree_height
    self.pos: Point = pos
    self.shadow_height = 0

  def illuminated(self) -> bool:
    if self.tree_height > 9:
      return False
    return self.tree_height > self.shadow_height

  def height(self) -> int:
    if self.tree_height > 9:
      return 0
    return self.tree_height


class Part3(BasePart):
  def __init__(self):
    super().__init__(8, 3)
    self.input = list(self.get_input_lines())
    self.width = len(self.input[0])
    self.height = len(self.input)
    self.warriors = 0

  def run(self):
    row_count = self.height
    row_len = floor(row_count / 2)

    starting_points: list[list[Point]] = [[], [], [], [], [], []]
    for i in range(0, ceil(row_count / 2)):
      x = i
      y = floor(row_count / 2) - i
      if y > 0:
        starting_points[0].append(Point(x, y))  # /
        starting_points[5].append(Point(x, y))
        starting_points[4].append(Point(x, floor(row_count / 2) + i))  # \
        if y != floor(row_count / 2) + i:
          starting_points[5].append(Point(x, floor(row_count / 2) + i))

        starting_points[1].append(Point(self.width - 1 - x, y))  # / \\
        starting_points[2].append(Point(self.width - 1 - x, y))
        if y != floor(row_count / 2) + i:
          starting_points[2].append(Point(self.width - 1 - x, floor(row_count / 2) + i))  # \_//
        starting_points[3].append(Point(self.width - 1 - x, floor(row_count / 2) + i))


      else:
        for x1 in range(x, x + (ceil(row_count / 2) * 2), 2):
          if x1 == x:
            starting_points[2].append(Point(self.width - 1 - x1, y))
            starting_points[2].append(Point(self.width - 1 - x1, self.height - 1))
            starting_points[5].append(Point(x1, self.height - 1))
            starting_points[5].append(Point(x1, y))

          starting_points[0].append(Point(x1, y))  # -
          starting_points[1].append(Point(self.width - 1 - x1, y))
          starting_points[3].append(Point(self.width - 1 - x1, self.height - 1))  # _
          starting_points[4].append(Point(x1, self.height - 1))
          row_len -= 1

    total = 0

    count = 0
    while self.warriors < 100000:
      for sp_list in starting_points:
        if self.warriors >= 100000:
          break
        row_len = ceil(row_count / 2)
        horizontal = count % 3 == 2
        if horizontal:
          row_len = row_count
        tree_map = []
        for n, sp in enumerate(sp_list):
          tree_map = self.traverse_map(sp, row_len, count, tree_map)
          if horizontal and n % 2 == 0:
            row_len -= 1
          elif not horizontal:
            if n >= floor(row_count / 2):
              row_len -= 1
            else:
              row_len += 1

        for row in tree_map:
          for tree in row:
            if tree.illuminated():
              total += 1
              if tree.tree_height == 9:
                self.warriors += 1

              match tree.tree_height:
                case 9:
                  self.input[tree.pos.y] = replace_char(self.input[tree.pos.y], tree.pos.x, "A")
                case _:
                  self.input[tree.pos.y] = replace_char(self.input[tree.pos.y], tree.pos.x,
                                                        f"{tree.tree_height + 1}")
            else:
              match tree.tree_height:
                case 10:
                  self.input[tree.pos.y] = replace_char(self.input[tree.pos.y], tree.pos.x, "B")
                case 11:
                  self.input[tree.pos.y] = replace_char(self.input[tree.pos.y], tree.pos.x, "C")
                case 12:
                  self.input[tree.pos.y] = replace_char(self.input[tree.pos.y], tree.pos.x, "1")
        # for row in self.input:
        #   print(row)
        count += 1

    return total

  def traverse_map(self, start: Point, row_len: int, direction: int, tree_map: list[list[GrowingSpot]]) -> list[
    list[GrowingSpot]]:
    x = start.x
    y = start.y
    shadow_height = 0
    map_row: list[GrowingSpot] = []
    for _ in range(0, row_len):
      tree = GrowingSpot(Point(x, y), int(self.input[y][x], 16))
      tree.shadow_height = shadow_height
      if tree.height() > shadow_height:
        shadow_height = tree.height()
      map_row.append(tree)
      match direction % 6:
        case 0:
          x += 1
          y += 1
        case 1:
          x -= 1
          y += 1
        case 2:
          x -= 2
        case 3:
          x -= 1
          y -= 1
        case 4:
          x += 1
          y -= 1
        case 5:
          x += 2
      shadow_height -= 1
    tree_map.append(map_row)
    return tree_map
