from operator import indexOf

from days.base_part import BasePart


class Part3(BasePart):
  def __init__(self):
    super().__init__(4, 3, True)

  def run(self):
    input = self.get_input_lines()
    dict = {}
    for line in input:
      id = line.split(" ")[0]
      index = indexOf(id, "=")
      id = int(id[3:])
      dict[id] = {"time": 0, "score": 0}
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
      for _, part in quest.items():
        for run in part["runs"]:
          print(run)
