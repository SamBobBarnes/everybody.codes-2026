from math import floor

from days.base_part import BasePart


def create_branch_collection():
  return {}


class Plant:

  def __init__(self, details: str):
    parts = details.split(", ")
    self.id = int(parts[0][3:])
    self.growth = int(parts[1][7:])
    self.limit = int(parts[2][6:])
    self.branches = create_branch_collection()
    self.split_len = floor(self.growth / 2)
    self.leaves = 0

  def total(self):
    return self.leaves

  def next_split_in(self) -> int:
    if len(self.branches.keys()) == 0:
      raise Exception("Plant must be grown once before we can determine next split")
    keys = sorted(map(lambda x: int(x), self.branches.keys()), reverse=True)
    return self.growth - keys[0]

  def grow(self, grow_by: int = 1):
    if len(self.branches.keys()) == 0:
      self.branches['1'] = 1
      self.leaves += 1
      return
    split_req = 0

    # loop in reverse key order
    for key, val in sorted(self.branches.items(), key=lambda x: -int(x[0])):
      if key == f"{self.growth - grow_by}":
        split_req += val
      # remove from lower and add to upper
      self.add_branches(val, int(key) + grow_by)
      self.add_branches(-val, int(key))

    if split_req > 0:
      self.add_branches(-split_req, self.growth)
      self.add_branches(split_req, 1)
      self.add_branches(split_req * 2, self.split_len)
      self.leaves += split_req

    self.compress_branches()

  def compress_branches(self):
    deletions = []
    for key, val in self.branches.items():
      if val == 0:
        deletions.append(key)
    for key in deletions:
      self.branches.pop(key)

  def add_branches(self, num_to_add: int, length: int):
    if self.branches.get(f"{length}") is None:
      self.branches[f"{length}"] = 0
    self.branches[f"{length}"] += num_to_add


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
        plant.grow(secs_to_next)
        secs += secs_to_next
      total += secs

    return total
