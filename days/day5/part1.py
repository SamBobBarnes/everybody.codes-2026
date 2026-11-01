from math import floor

from days.base_part import BasePart, Map, Point


def count_neighbors(bin_map: Map[bool], land_map: Map[bool], p: Point, width, height) -> int:
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


def print_map(land_map: Map[bool], bin_map: Map[bool]):
  for y in range(0, len(land_map[0])):
    line = ""
    for x in range(0, len(land_map)):
      if land_map[x][y]:
        line += "#"
      elif bin_map[x][y]:
        line += "*"
      else:
        line += "."
    print(line)
  print("")


def count_map(land_map: Map[bool]):
  count = 0
  for y in range(0, len(land_map[0])):
    for x in range(0, len(land_map)):
      if land_map[x][y]:
        count += 1
  return count


class Part1(BasePart):
  def __init__(self):
    super().__init__(5, 1)

  def run(self):
    input = self.get_input_lines()
    height = len(input)
    width = len(input[0])
    center = Point(floor(width / 2), floor(height / 2))
    land_map = list()
    bin_map = list()
    for x in range(0, width):
      map_col = list()
      bin_map_col = list()
      for y in range(0, height):
        map_col.append(y == center.y and x == center.x)
        bin_map_col.append(input[y][x] == '1')
      land_map.append(map_col)
      bin_map.append(bin_map_col)

    created = 1
    total = 1
    runs = 0
    while created > 0:
      runs += 1
      # print(f"run: {runs}")
      created = 0
      for y in range(0, len(land_map[0])):
        for x in range(0, len(land_map)):
          if land_map[x][y]:
            continue
          count = count_neighbors(bin_map, land_map, Point(x, y), width, height)
          if count > 4:
            land_map[x][y] = True
            total += 1
            created += 1
      # print_map(land_map, bin_map)
    return count_map(land_map)
