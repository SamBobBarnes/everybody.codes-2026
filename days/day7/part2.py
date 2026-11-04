from days.base_part import BasePart


class Part2(BasePart):
  def __init__(self):
    super().__init__(7, 2)

  def run(self):
    input = self.get_input_lines()
    dict = {}
    max_connections = 0
    max_connections_id = ""
    for line in input:
      parts = line.split(", ")
      id = parts[0].split("=")[1]
      energy = int(parts[1].split("=")[1])
      connections = parts[2].split("=")[1].split(",")
      dict[id] = {"energy": energy, "connections": connections}
      if len(connections) > max_connections:
        max_connections = len(connections)
        max_connections_id = id

    def shock(id: str, energy: int):
      dict[id]["energy"] += energy
      if energy == 1:
        return
      for i in dict[id]["connections"]:
        shock(i, energy - 1)

    shock(max_connections_id, 10)

    return sum(list(map(lambda x: x["energy"], dict.values())))
