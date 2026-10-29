from days.base_part import BasePart


def get_decimal_num(exponents: str, num: str) -> int:
  total = int(num[0]) * pow(int(exponents[0]), 3)
  total += int(num[1]) * pow(int(exponents[1]), 2)
  total += int(num[2]) * pow(int(exponents[2]), 1)
  total += int(num[3])
  return total


class Part1(BasePart):
  def __init__(self):
    super().__init__(3, 1)

  def run(self):
    input = self.get_input_lines()
    total = 0
    for line in input:
      parts = line.lstrip("ISO-").split(" ")
      total += get_decimal_num(parts[0], parts[1])
    return total
