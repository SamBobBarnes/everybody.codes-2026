class BasePart:
    def __init__(self,day:int,part:int,test:bool = False):
        self.day = day
        self.part = part
        self.test = test

    def run_part(self):
        answer = self.run()
        print(f"\n----------------\nDay {self.day} Part {self.part}\n{answer}\n----------------\n")

    def run(self):
        return f"day {self.day} part {self.part} not yet implemented!"

    def get_input(self) -> list[str]:
        test_str = ".test"
        with open(f"inputs/day{self.day}-input{self.test and test_str}.txt",'r', encoding='utf-8-sig') as file:
            content = file.read().replace("\r\n","\n").split("\n")
            return content