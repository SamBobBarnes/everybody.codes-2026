from math import floor

from days.base_part import BasePart


class Plant:
  def __init__(self, details: str):
    parts = details.split(", ")
    self.id = int(parts[0][3:])
    self.growth = int(parts[1][7:])
    self.limit = int(parts[2][6:])
    self.branches = self.create_branch_list()
    self.split_len = floor(self.growth / 2)

  def total(self):
    return sum(list(map(lambda x: self.sum_lambda(x[0], x[1]), enumerate(self.branches))))

  def sum_lambda(self, n, x) -> int:
    if n < self.growth - 1:
      return (n + 1) * x
    else:
      return x

  def create_branch_list(self) -> list[int]:
    branches = []
    # [l1,l2,l3,...,lG-1,jn]
    for _ in range(0, self.growth):
      branches.append(0)
    return branches

  def grow(self):
    if sum(self.branches) == 0:
      self.branches[0] += 1
      return
    branches = self.create_branch_list()
    for i in range(0, self.growth - 1):
      if i == self.growth - 2:
        branches[self.split_len - 1] += self.branches[i] * 2
        branches[0] += self.branches[i]
      branches[i + 1] += self.branches[i]
    branches[self.growth - 1] += self.branches[self.growth - 1]
    self.branches = branches


class Part1(BasePart):
  def __init__(self):
    super().__init__(9, 1)

  def run(self):
    plants = list(map(lambda x: Plant(x), self.get_input_lines()))
    total = 0
    for plant in plants:
      secs = 0
      while plant.total() < plant.limit:
        plant.grow()
        secs += 1
      total += secs

    return total
