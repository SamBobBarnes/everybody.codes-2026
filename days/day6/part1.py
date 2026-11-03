from queue import Queue

from days.base_part import BasePart


class Part1(BasePart):
  def __init__(self):
    super().__init__(6, 1)

  def run(self):
    dict = {}
    input = self.get_input_lines()
    for line in input:
      item = line.split(":")[0]
      ingredients = line.split(":")[1].split(",")
      dict[item] = ingredients
    null = dict["NULL"]
    q = Queue()
    q.put("NULL")
    ingredients = {}
    visited = {}
    while not q.empty():
      item = q.get_nowait()
      if item in visited:
        continue
      visited[item] = 1
      if item not in dict:
        continue

      ingrs = dict[item]
      for i in ingrs:
        if i == "NULL":
          continue
        ingredients[i] = 1
        q.put(i)
    return len(ingredients.keys())
