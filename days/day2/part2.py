from functools import total_ordering

from days.base_part import BasePart


def rule_followed(key, rule, group):
  i = group.index(key)
  for b in rule["before"]:
    if group.index(b) > i:
      return False
  for a in rule["after"]:
    if group.index(a) < i:
      return False
  return True


@total_ordering
class Rule:
  def __init__(self, a: int, b: int):
    self.a = a
    self.b = b

  def __eq__(self, other):
    if not isinstance(other, Rule):
      return NotImplemented
    return self.a == other.a and self.b == other.b

  # 2. Define Less Than (or any one of: <=, >, >=)
  def __lt__(self, other):
    if not isinstance(other, Rule):
      return NotImplemented
    return self.a < other.a or (self.a == other.a and self.b < other.b)

  def __repr__(self) -> str:
    sign = "<"
    return f"{self.a}{sign}{self.b}"


class Part2(BasePart):
  width = 9

  def __init__(self):
    super().__init__(2, 2)

  def run(self):
    input = self.get_input_lines()
    groups = []
    for line in input:
      group = []
      for i in range(1, self.width + 1):
        group.append(i)

      rules = []

      # initial rules
      for comp in line.split(" "):
        a = int(comp[0])
        b = int(comp[2])
        lt = comp[1] == "<"
        if lt:
          rules.append(Rule(a, b))
        else:
          rules.append(Rule(b, a))

      # extend rules
      extra_rules = []
      for rule in rules:
        a_s = list(filter(
          lambda x: x.b == rule.a, rules))
        b_s = list(filter(
          lambda x: x.a == rule.b, rules))
        for a in a_s:
          if len(list(filter(lambda x: x.a == a.a and x.b == rule.b, extra_rules))) == 0 and len(
            list(filter(lambda x: x.a == a.a and x.b == rule.b, rules))) == 0:
            extra_rules.append(Rule(a.a, rule.b))
        for b in b_s:
          if len(list(filter(lambda x: x.a == rule.a and x.b == b.b, extra_rules))) == 0 and len(
            list(filter(lambda x: x.a == rule.a and x.b == b.b, rules))) == 0:
            extra_rules.append(Rule(rule.a, b.b))

      rules.extend(extra_rules)

      def run_rule(rule: Rule):
        if group.index(rule.a) > group.index(rule.b):
          group.remove(rule.a)
          group.insert(group.index(rule.b), rule.a)

      rules.sort()
      for comp in rules:
        run_rule(comp)
      group.reverse()
      groups.append(int(str(group).replace(", ", "").lstrip("[").rstrip("]")))
    total = 0
    for group in groups:
      total += group
    return total
