from days.base_part import BasePart


def get_decimal_num(base: list[int], num: list[int]) -> int:
  num_len = len(num)
  ex_len = len(base)

  total = 0
  for i in range(0, num_len):
    val = int(num[i]) * pow(base[i % ex_len], i)
    total += val

  return total


class Part3(BasePart):
  def __init__(self):
    super().__init__(3, 3)

  def run(self):
    input = self.get_input_lines()
    total = 0
    for line in input:
      parts = line[5:].split(" ")
      base = list(map(lambda x: int(x), list(parts[0])))[::-1]
      vals = list(map(lambda x: int(x), list(parts[1])))[::-1]

      val = get_decimal_num(base, vals)
      dupe = False
      lower_bound = 1
      if len(parts[1]) > 1:
        lower_bound = pow(10, len(parts[1]) - 2)
      for i in range(lower_bound, int(parts[1]))[::-1]:
        if dupe:
          break
        vals = list(map(lambda x: int(x), list(str(i))))[::-1]
        if get_decimal_num(base, vals) == val:
          dupe = True
          break
      if not dupe:
        total += val
    return total
