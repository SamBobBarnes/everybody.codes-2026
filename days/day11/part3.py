from collections import deque
from math import floor

from days.base_part import BasePart
from days.day11.part1 import Portal


class Part3(BasePart):
  def __init__(self):
    super().__init__(11, 3)
    self.portals: list[Portal] = []

  def run(self):
    input = self.get_input_lines()
    portal_count = int(input[0][9:])

    for i in range(1, portal_count + 1):
      self.portals.append(Portal(i))
    for i in range(0, portal_count):
      self.portals[i].connections.append(self.portals[(i + 1) % portal_count])
      self.portals[i].connections.append(self.portals[(i + 2) % portal_count])
      self.portals[i].connections.append(self.portals[(i + 3) % portal_count])
      self.portals[i].connections.append(self.portals[(i - 1) % portal_count])
      self.portals[i].connections.append(self.portals[(i - 2) % portal_count])
      self.portals[i].connections.append(self.portals[(i - 3) % portal_count])
    self.watch.start()
    pre_shortcut_strain = self.get_strain()

    for conn in input[2:]:
      a, b = map(lambda x: int(x) - 1, conn.split(" "))
      self.portals[a].connections.append(self.portals[b])
      self.portals[b].connections.append(self.portals[a])

    min_strain = self.get_strain()

    spacing = floor(portal_count / 8)
    for i in range(0, spacing):
      crystals = []
      for i2 in range(0, portal_count, spacing):
        crystals.append(self.portals[(i + i2) % portal_count])

      arrangements: list[list[tuple[Portal, Portal]]] = self.get_arrangements([], crystals)

      for arr in arrangements:
        for a, b in arr:
          self.connect(a, b)

        strain = self.get_strain()
        min_strain = min(min_strain, strain)

        for a, b in arr:
          self.disconnect(a, b)

    self.watch.stop()
    return pre_shortcut_strain - min_strain

  def get_arrangements(self, claims: list[tuple[Portal, Portal]], crystals: list[Portal]) -> list[
    list[tuple[Portal, Portal]]]:
    if len(claims) == 4:
      return [claims]

    arrangements: list[list[tuple[Portal, Portal]]] = []

    for i in range(0, len(crystals)):
      a = crystals[i]
      for j in range(i, len(crystals)):
        b = crystals[j]
        if a == b:
          continue
        new_claims = list(map(lambda x: x, claims))
        new_claims.append(tuple((a, b)))
        left_over_crystals = []
        for c in crystals:
          if len(list(filter(lambda x: x[0] == c or x[1] == c, new_claims))) > 0:
            continue
          left_over_crystals.append(c)
        arrangements.extend(self.get_arrangements(new_claims, left_over_crystals))
    return arrangements

  def connect(self, a: Portal, b: Portal):
    a.connections.append(b)
    b.connections.append(a)

  def disconnect(self, a: Portal, b: Portal):
    a.connections.remove(b)
    b.connections.remove(a)

  def get_strain(self) -> int:
    total = 0
    for p_start in self.portals:
      total += self.bfs_total(p_start)
    return total

  def bfs_total(self, start: Portal) -> int:
    q = deque([start])
    dist = {start: 0}

    while q:
      p = q.popleft()
      for c in p.connections:
        if c not in dist:
          dist[c] = dist[p] + 1
          q.append(c)

    return sum(dist.values())
