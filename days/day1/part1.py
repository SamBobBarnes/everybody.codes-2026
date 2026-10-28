from math import sqrt, ceil

from days.base_part import BasePart

class Part1(BasePart):
    def __init__(self):
        super().__init__(1,1)

    def run(self):
        total = 0
        input = self.get_input().split(",")
        for i in input:
            remaining = int(i)
            rt = sqrt(remaining)
            side_len = ceil(rt)
            ttl = side_len*side_len
            total += ttl - remaining
        return total
