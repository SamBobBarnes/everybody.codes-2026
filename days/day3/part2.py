from days.base_part import BasePart


def get_decimal_num(exponents: str, num: str) -> int:
  num_len = len(num)
  extended_ex = exponents

  while len(extended_ex) < num_len:
    extended_ex += exponents

  extended_ex = extended_ex[len(extended_ex) % num_len:]

  ex_len = len(extended_ex)

  total = 0
  for i in range(0, num_len):
    val = int(num[i]) * pow(int(extended_ex[i % ex_len]), num_len - 1 - i)
    total += val

  return total


class Part2(BasePart):
  def __init__(self):
    super().__init__(3, 2)

  def run(self):
    input = self.get_input_lines()
    total = 0
    for line in input:
      parts = line.lstrip("ISO-").split(" ")
      total += get_decimal_num(parts[0], parts[1])
    return total
