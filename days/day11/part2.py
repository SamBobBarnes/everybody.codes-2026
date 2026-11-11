from collections import deque

from days.base_part import BasePart
from days.day11.part1 import Portal


class Part2(BasePart):
  def __init__(self):
    super().__init__(11, 2)
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

    for a in self.portals:
      for b in self.portals:
        if len(list(filter(lambda x: x.id == b.id, a.connections))): continue

        a.connections.append(b)
        b.connections.append(a)
        strain = self.get_strain()
        min_strain = min(min_strain, strain)
        a.connections.remove(b)
        b.connections.remove(a)

    self.watch.stop()
    return pre_shortcut_strain - min_strain

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
