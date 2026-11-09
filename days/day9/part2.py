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
    self.leaves = 0
    # todo: find a way to move away from enormous lists

  def total(self):
    return self.leaves

  def create_branch_list(self) -> list[int]:
    branches = []
    # [l1,l2,l3,...,lG-1,jn]
    for _ in range(0, self.growth):
      branches.append(0)
    return branches

  def next_split_in(self) -> int:
    if sum(self.branches) == 0:
      return self.growth
    total = 0
    for i in reversed(range(0, self.growth - 1)):
      total += 1
      if self.branches[i] != 0:
        return total
    raise Exception("Should have found a positive number by now")

  def grow_secs(self, secs: int):

    if sum(self.branches) == 0:
      raise Exception("Plant must be grown once before it can be grown multiple steps at a time")

    if secs > 1:
      branches = self.create_branch_list()
      for i in range(0, self.growth - secs):
        branches[i + secs - 1] = self.branches[i]
      branches[self.growth - 1] = self.branches[self.growth - 1]
      self.branches = branches

    self.grow()

  def grow(self):
    if sum(self.branches) == 0:
      self.branches[0] += 1
      self.leaves += 1
      return
    branches = self.create_branch_list()
    for i in range(0, self.growth - 1):
      if i == self.growth - 2:
        branches[self.split_len - 1] += self.branches[i] * 2
        branches[0] += self.branches[i]
        self.leaves += self.branches[i]
      branches[i + 1] += self.branches[i]
    branches[self.growth - 1] += self.branches[self.growth - 1]
    self.branches = branches


class Part2(BasePart):
  def __init__(self):
    super().__init__(9, 2)

  def run(self):
    plants = list(map(lambda x: Plant(x), self.get_input_lines()))
    total = 0
    for plant in plants:
      secs = 1
      plant.grow()
      while plant.total() < plant.limit:
        secs_to_next = plant.next_split_in()
        plant.grow_secs(secs_to_next)
        secs += secs_to_next
      total += secs

    return total
