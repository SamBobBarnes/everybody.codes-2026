from queue import Queue

from days.base_part import BasePart


class Part2(BasePart):
  def __init__(self):
    super().__init__(6, 2)

  def run(self):
    dict = {}
    input = self.get_input_lines()
    for line in input:
      item = line.split(":")[0]
      ingredients = line.split(":")[1].split(",")
      dict[item] = ingredients

    used_in = {}
    for item, ingrs in dict.items():
      for i in ingrs:
        if i not in used_in:
          used_in[i] = {}
        used_in[i][item] = 1

    ingredients = {}

    q = Queue()
    q.put("NULL")

    visited = {}
    while not q.empty():
      item = q.get_nowait()
      if item in visited:
        continue
      visited[item] = 1
      if item not in used_in:
        continue

      ingrs = used_in[item]
      for i in ingrs.keys():
        if i == "NULL":
          continue
        ingredients[i] = 1
        q.put(i)
    return len(ingredients.keys())
