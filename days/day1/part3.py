from days.base_part import BasePart


def get_req(side_len: int):
    return side_len * side_len - 1


class Part3(BasePart):
    def __init__(self):
        super().__init__(1, 3)

    def run(self):
        total = 0
        input = self.get_input().split(",")
        for i in input:
            remaining = int(i)
            side_len = 3
            ttl = get_req(side_len)
            while ttl < remaining:
                side_len += 2
                ttl = get_req(side_len)
            total += ttl - remaining
        return total
