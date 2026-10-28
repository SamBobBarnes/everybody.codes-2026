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


class Part2(BasePart):
  def __init__(self):
    super().__init__(2, 2, True)

  def run(self):
    input = self.get_input_lines()
    groups = []
    for line in input:
      group = {"1": {"before": [], "after": []}, "2": {"before": [], "after": []},
               "3": {"before": [], "after": []}, "4": {"before": [], "after": []},
               "5": {"before": [], "after": []}}
      for comp in line.split(" "):
        a = comp[0]
        b = comp[2]
        lt = comp[1] == "<"
        if lt:
          group[a]["after"].append(b)
          group[b]["before"].append(a)
        else:
          group[b]["after"].append(a)
          group[a]["before"].append(b)
      found = False
      for a in range(1, 6):
        for b in range(1, 6):
          if a == b or found: continue
          for c in range(1, 6):
            if a == c or b == c or found: continue
            for d in range(1, 6):
              if a == d or b == d or c == d or found: continue
              for e in range(1, 6):
                if a == e or b == e or c == e or d == e or found: continue
                for key, rule in group.items():
                  if rule_followed(key, rule, [str(a), str(b), str(c), str(d), str(e)]):
                    groups.append(int(f"{e}{d}{c}{b}{a}"))
                    found = True
                    break

    total = 0
    for g in groups:
      total += g
    return total
