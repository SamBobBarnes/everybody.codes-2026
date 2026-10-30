from operator import indexOf

from days.base_part import BasePart


def new_dict(lines):
  dict = {}
  for line in lines:
    id = line.split(" ")[0]
    index = indexOf(id, "=")
    id = id[3:]
    dict[id] = {"id": id, "time": 0, "score": 0, "parts": 0}
  return dict


class Part3(BasePart):
  def __init__(self):
    super().__init__(4, 3, True)

  def run(self):
    input = self.get_input_lines()
    dict = new_dict(input)

    runs = list(map(lambda x: {"id": int(x[0]), "quest": int(x[1]), "part": int(x[2]), "time": int(x[3])},
                    list(map(lambda line: list(map(lambda x: x[indexOf(x, "=") + 1:], line.split(" "))), input))))
    runs.sort(key=lambda x: (x["quest"], x["part"], x["time"]))

    quests = {}
    quest = "0"
    part = "0"

    for run in runs:
      if str(run["quest"]) != quest:
        quest = str(run["quest"])

        quests[quest] = {}

      if str(run["part"]) != part:
        part = str(run["part"])
        quests[quest][part] = []

      quests[quest][part].append(run)

    for _, quest in quests.items():
      running_totals = new_dict(input)
      for _, part in quest.items():
        for run in part:
          running_totals[run["id"]]["time"] += run["time"]
          running_totals[run["id"]]["parts"] += run["parts"]
        sorted_totals = []
