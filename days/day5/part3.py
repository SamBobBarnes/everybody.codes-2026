import copy
from math import floor

from days.base_part import BasePart, Map, Point


def count_potential_land(bin_map: Map[bool], land_map: Map[bool], p: Point, width, height) -> int:
  count = 0
  land_count = 0
  if p.y + 1 < height:
    if land_map[p.x][p.y + 1]:
      land_count += 1
    elif bin_map[p.x][p.y + 1]:
      count += 1
  if p.y - 1 >= 0:
    if land_map[p.x][p.y - 1]:
      land_count += 1
    elif bin_map[p.x][p.y - 1]:
      count += 1
  if p.x + 1 < width:
    if land_map[p.x + 1][p.y]:
      land_count += 1
    elif bin_map[p.x + 1][p.y]:
      count += 1
  if p.x - 1 >= 0:
    if land_map[p.x - 1][p.y]:
      land_count += 1
    elif bin_map[p.x - 1][p.y]:
      count += 1
  if p.x + 1 < width and p.y - 1 >= 0:
    if land_map[p.x + 1][p.y - 1]:
      land_count += 1
    elif bin_map[p.x + 1][p.y - 1]:
      count += 1
  if p.x - 1 >= 0 and p.y - 1 >= 0:
    if land_map[p.x - 1][p.y - 1]:
      land_count += 1
    elif bin_map[p.x - 1][p.y - 1]:
      count += 1
  if p.x + 1 < width and p.y + 1 < height:
    if land_map[p.x + 1][p.y + 1]:
      land_count += 1
    elif bin_map[p.x + 1][p.y + 1]:
      count += 1
  if p.x - 1 >= 0 and p.y + 1 < height:
    if land_map[p.x - 1][p.y + 1]:
      land_count += 1
    elif bin_map[p.x - 1][p.y + 1]:
      count += 1
  if land_count == 0:
    return 0
  return count + land_count


def can_contain_tree(land_map: Map[bool], sand_map: Map[bool], p: Point, width, height):
  if p.x < 2 or p.x > width - 3 or p.y < 2 or p.y > height - 3:
    return False
  for x in range(-2, 3):
    for y in range(-2, 3):
      if abs(x) == 2 and abs(y) == 2:
        continue
      if not land_map[p.x + x][p.y + y]:
        return False
      if sand_map[p.x + x][p.y + y]:
        return False
  return True


def count_neighbors(map: Map[bool], p: Point, width, height) -> int:
  count = 0
  if p.y + 1 < height and map[p.x][p.y + 1]:
    count += 1
  if p.y - 1 >= 0 and map[p.x][p.y - 1]:
    count += 1
  if p.x + 1 < width and map[p.x + 1][p.y]:
    count += 1
  if p.x - 1 >= 0 and map[p.x - 1][p.y]:
    count += 1
  if p.x + 1 < width and p.y - 1 >= 0 and map[p.x + 1][p.y - 1]:
    count += 1
  if p.x - 1 >= 0 and p.y - 1 >= 0 and map[p.x - 1][p.y - 1]:
    count += 1
  if p.x + 1 < width and p.y + 1 < height and map[p.x + 1][p.y + 1]:
    count += 1
  if p.x - 1 >= 0 and p.y + 1 < height and map[p.x - 1][p.y + 1]:
    count += 1
  return count


def print_map(land_map: Map[bool], sand_map: Map[bool], tree_map: Map[bool]):
  for y in range(0, len(land_map[0])):
    line = ""
    for x in range(0, len(land_map)):
      if tree_map[x][y]:
        line += "@"
      elif sand_map[x][y]:
        line += "="
      elif land_map[x][y]:
        line += "#"
      else:
        line += "."
    print(line)
  print("")


class Part3(BasePart):
  def __init__(self):
    super().__init__(5, 3)

  def run(self):
    input = self.get_input_lines()
    height = len(input)
    width = len(input[0])
    center = Point(floor(width / 2), floor(height / 2))
    land_map = list()
    bin_map = list()
    sand_map = list()
    tree_map = list()
    for x in range(0, width):
      map_col = list()
      bin_map_col = list()
      sand_map_col = list()
      tree_map_col = list()
      for y in range(0, height):
        map_col.append(y == center.y and x == center.x)
        bin_map_col.append(input[y][x] == '1')
        sand_map_col.append(False)
        tree_map_col.append(False)
      land_map.append(map_col)
      bin_map.append(bin_map_col)
      sand_map.append(sand_map_col)
      tree_map.append(tree_map_col)

    created = 1
    while created > 0:
      created = 0
      for y in range(0, len(land_map[0])):
        for x in range(0, len(land_map)):
          if land_map[x][y]:
            continue
          count = count_potential_land(bin_map, land_map, Point(x, y), width, height)
          if count > 4:
            land_map[x][y] = True
            created += 1

    created = 1
    while created > 0:
      created = 0
      for y in range(0, len(land_map[0])):
        for x in range(0, len(land_map)):
          if not land_map[x][y]:
            continue
          if sand_map[x][y]:
            continue
          land_count = count_neighbors(land_map, Point(x, y), width, height)
          sand_count = count_neighbors(sand_map, Point(x, y), width, height)
          if land_count < 8 or sand_count > 4:
            sand_map[x][y] = True
            created += 1

    total = 0
    for y in range(0, len(land_map[0])):
      for x in range(0, len(land_map)):
        if can_contain_tree(land_map, sand_map, Point(x, y), width, height):
          tree_map[x][y] = True
          total += 1

    # print_map(land_map, sand_map, tree_map)
    # print("")

    for _ in range(0, 2):
      tree_map2 = copy.deepcopy(tree_map)
      for y in range(0, len(land_map[0])):
        for x in range(0, len(land_map)):
          if tree_map[x][y]:
            continue
          if count_neighbors(tree_map, Point(x, y), width, height) > 3 and count_neighbors(sand_map, Point(x, y), width,
                                                                                           height) == 0:
            tree_map2[x][y] = True
            total += 1
      tree_map = tree_map2.copy()
      # print_map(land_map, sand_map, tree_map)
      # print("")

    return total
