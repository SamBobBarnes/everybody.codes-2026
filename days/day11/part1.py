import sys
from dataclasses import dataclass, field
from queue import PriorityQueue

from days.base_part import BasePart


class Portal:
  def __init__(self, id: int):
    self.id = id
    self.connections: list[Portal] = []

  def __str__(self) -> str:
    string = f"{self.id} ["
    string += ",".join(map(lambda x: f"{x.id}", self.connections))
    string += "]"
    return string


@dataclass(order=True)
class PrioritizedItem:
  priority: int
  item: Portal = field(compare=False)

  def __init__(self, priority: int, item: Portal):
    self.priority = priority
    self.item = item


class Part1(BasePart):
  def __init__(self):
    super().__init__(11, 1)
    self.portals: list[Portal] = []

  def run(self):
    input = self.get_input_lines()
    portal_count = int(input[0][9:])

    for i in range(1, portal_count + 1):
      self.portals.append(Portal(i))
    for i in range(0, portal_count):
      if i < portal_count - 1:
        self.portals[i].connections.append(self.portals[i + 1])
      else:
        self.portals[i].connections.append(self.portals[0])
      if i > 0:
        self.portals[i].connections.append(self.portals[i - 1])
      else:
        self.portals[i].connections.append(self.portals[portal_count - 1])

    pre_shortcut_strain = self.get_strain()

    for conn in input[2:]:
      a, b = map(lambda x: int(x) - 1, conn.split(" "))
      self.portals[a].connections.append(self.portals[b])
      self.portals[b].connections.append(self.portals[a])

    post_shortcut_strain = self.get_strain()

    return pre_shortcut_strain - post_shortcut_strain

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
