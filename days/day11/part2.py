import sys
from queue import PriorityQueue

from days.base_part import BasePart
from days.day11.part1 import Portal, PrioritizedItem


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

    return pre_shortcut_strain - min_strain

  def get_strain(self) -> int:
    total = 0
    for p_start in self.portals:
      p_total = 0
      for p_end in self.portals:
        if p_start == p_end:
          continue
        p_total += self.dijkstra(p_start, p_end)
      total += p_total
    return total

  def dijkstra(self, start: Portal, end: Portal) -> int:

    q = PriorityQueue[PrioritizedItem]()
    q.put(PrioritizedItem(0, start))

    dist = {}
    prev = {}
    for p in self.portals:
      dist[p] = sys.maxsize
      prev[p] = None
    dist[start] = 0

    while not q.empty():
      pi = q.get_nowait()
      if pi.item.id == end.id:
        return dist[pi.item]
      for c in pi.item.connections:
        alt = dist[pi.item] + 1
        if alt < dist[c]:
          prev[c] = pi.item
          dist[c] = alt
          q.put_nowait(PrioritizedItem(alt, c))

    return -1
