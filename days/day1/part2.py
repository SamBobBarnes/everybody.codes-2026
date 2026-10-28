from days.base_part import BasePart


def get_perimeter(side_len: int):
    return side_len * 4 - 4


class Part2(BasePart):
    def __init__(self):
        super().__init__(1,2)

    def run(self):
        total = 0
        input = self.get_input().split(",")
        for i in input:
            remaining = int(i)
            side_len = 3
            ttl = get_perimeter(side_len)
            while ttl < remaining:
                side_len += 1
                ttl = get_perimeter(side_len)
            total += ttl - remaining
        return total