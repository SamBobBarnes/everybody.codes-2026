def get_file(filename) -> str:
    with open(filename, 'r', encoding='utf-8-sig') as file:
        return file.read()


class BasePart:
    def __init__(self, day: int, part: int, test: bool = False):
        self.day = day
        self.part = part
        self.test = test

    def run_part(self):
        answer = self.run()
        print(f"\n----------------\nDay {self.day} Part {self.part}\n{answer}\n----------------\n")

    def run(self):
        return f"day {self.day} part {self.part} not yet implemented!"

    def get_input_lines(self) -> list[str]:
        if self.test:
            file = get_file(f"inputs/day{self.day}-input.test.txt")
        else:
            file = get_file(f"inputs/day{self.day}-part{self.part}-input.txt")
        return file.replace("\r\n", "\n").split("\n")

    def get_input(self) -> str:
        if self.test:
            file = get_file(f"inputs/day{self.day}-input.test.txt")
        else:
            file = get_file(f"inputs/day{self.day}-part{self.part}-input.txt")
        return file.replace("\r\n", "\n")
