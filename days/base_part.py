class BasePart:
    def __init__(self,day,part):
        self.day = day
        self.part = part

    def run(self):
        raise f"day {self.day} part {self.part} not yet implemented"

    def get_input(self):
        print("hi")