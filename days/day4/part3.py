from operator import indexOf

from days.base_part import BasePart


def new_dict(lines):
  dict = {}
  for line in lines:
    id = line.split(" ")[0][3:]
    dict[id] = {"id": id, "time": 0, "score": 0, "parts": 0}
  return dict


class Part3(BasePart):
  def __init__(self):
    super().__init__(4, 3)

  def run(self):
    input = self.get_input_lines()
    dict = new_dict(input)

    runs = list(map(lambda x: {"id": int(x[0]), "quest": int(x[1]), "part": int(x[2]), "time": int(x[3])},
                    list(map(lambda line: list(map(lambda x: x[indexOf(x, "=") + 1:], line.split(" "))), input))))
    runs.sort(key=lambda x: (x["quest"], x["part"], x["time"]))

    quests = {}
    quest = "0"
    part = "0"

    for runner in runs:
      if str(runner["quest"]) != quest:
        quest = str(runner["quest"])

        quests[quest] = {}

      if str(runner["part"]) != part:
        part = str(runner["part"])
        quests[quest][part] = []

      quests[quest][part].append(runner)

    for _, quest in quests.items():
      running_totals = new_dict(input)
      for _, part in quest.items():
        part_num = part[0]["part"]
        for runner in part:
          running_totals[str(runner["id"])]["time"] += runner["time"]
          running_totals[str(runner["id"])]["parts"] += 1
        totals = list(running_totals.values())
        totals.sort(key=lambda x: (-x["parts"], x["time"]))
        totals = [x for x in totals if x["parts"] == part_num]
        points_avail = part_num * 50
        prev_time = 0
        points_to_add = 1
        for runner in totals:
          if runner["time"] == prev_time:
            running_totals[str(runner["id"])]["score"] += points_avail + points_to_add
            points_to_add += 1
          else:
            if points_avail <= 0:
              break
            prev_time = runner["time"]
            running_totals[str(runner["id"])]["score"] += points_avail
            points_to_add = 1
          points_avail -= 1
        print(f"end of p{part_num}")
      for runner in running_totals.values():
        dict[str(runner["id"])]["score"] += runner["score"]

    times = list(map(lambda x: x["score"], dict.values()))
    times.sort(key=lambda x: -x)
    print(times)
    return sum(list(map(lambda x: (x[0] + 1) * x[1], enumerate(times))))
