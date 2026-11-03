from queue import Queue

from days.base_part import BasePart


class Part3(BasePart):
  def __init__(self):
    super().__init__(6, 3)

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

    master_ingredients = []
    for null in ["NULLv1", "NULLv2", "NULLv3"]:
      ingredients = {}

      q = Queue()
      q.put(null)

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
      master_ingredients.append(ingredients)

    total = 0
    for item in dict.keys():
      count = 0
      for i in range(0, 3):
        if item in master_ingredients[i]:
          count += 1
      if count > 1:
        total += 1
    return total
