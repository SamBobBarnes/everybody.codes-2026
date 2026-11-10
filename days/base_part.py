import time


def get_file(filename) -> str:
  with open(filename, 'r', encoding='utf-8-sig') as file:
    return file.read()


type Map[T] = list[list[T]]


class Point:
  def __init__(self, x: int, y: int, z: int = 0):
    self.x = x
    self.y = y
    self.z = z

  def __str__(self):
    return f"({self.x},{self.y},{self.z})"

  def to_string(self):
    return self.__str__()

  def __eq__(self, other):
    if not isinstance(other, Point):
      return False
    return self.x == other.x and self.y == other.y and self.z == other.z

  def __hash__(self) -> int:
    return hash((self.x, self.y, self.z))


class BasePart:
  def __init__(self, day: int, part: int, test: bool = False):
    self.day = day
    self.part = part
    self.test = test
    self.watch = Stopwatch()

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


class Stopwatch:
  def __init__(self):
    self.start_time = None
    self.elapsed_time = 0
    self.is_running = False

  def start(self):
    if not self.is_running:
      self.start_time = time.perf_counter() - self.elapsed_time
      self.is_running = True
      print("Stopwatch started.")

  def stop(self):
    if self.is_running:
      self.elapsed_time = time.perf_counter() - self.start_time
      self.is_running = False
      print(f"Stopwatch stopped. Elapsed: {self.elapsed_time:.2f} seconds")

  def reset(self):
    self.elapsed_time = 0
    if self.is_running:
      self.start_time = time.perf_counter()
    print("Stopwatch reset.")

  def get_elapsed(self):
    if self.is_running:
      return time.perf_counter() - self.start_time
    return self.elapsed_time
