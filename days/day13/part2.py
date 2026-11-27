from fractions import Fraction

from days.base_part import BasePart

def delta(a,b):
  return ((a-b) % 1 + 1)

class Part2(BasePart):
  def __init__(self):
    super().__init__(13,2,True)
    self.input = self.get_input_lines()
    self.hands = []
    self.clockwise = []
    self.pos = []
    self.moves = []

  def run(self) -> str:
    total = 0

    for clock_i in range(0,len(self.input),5):
      print()
      clock_meetings = 0
      self.hands = list(map(lambda x: int(x),self.input[clock_i][6:].split(":")))
      self.clockwise = list(map(lambda x: x == "CW",self.input[clock_i+1][10:].split(":")))
      self.pos = list(map(lambda x: int(x),self.input[clock_i+2][8:].split(":")))
      self.moves = list(map(lambda x: int(x),self.input[clock_i+3][5:].split(":")))
      max_moves = max(self.moves)

      for a_i in range(0,2):
        for b_i in range(a_i+1,3):
          a_speed = Fraction(1,self.hands[a_i])
          b_speed = Fraction(1,self.hands[b_i])
          if self.clockwise[a_i] != self.clockwise[b_i]:
            b_speed = -b_speed
          rel_speed = abs(a_speed - b_speed)

          # end early if they will never pass
          if rel_speed == 0:
            continue

          if abs(a_speed) > abs(b_speed):
            pd = delta(Fraction(self.pos[b_i],self.hands[b_i]),Fraction(self.pos[a_i],self.hands[a_i]))
            t1 = pd/(a_speed-b_speed)
          else:
            pd = delta(Fraction(self.pos[a_i],self.hands[a_i]),Fraction(self.pos[b_i],self.hands[b_i]))
            t1 = pd/(b_speed-a_speed)

          td = 1/rel_speed

          print(f"a_speed: {a_speed}, b_speed: {b_speed}, rel_speed: {rel_speed}, pd: {pd}, t1: {t1}, td: {td}")



      return ""

      for t in range(0,max_moves):

        for a_i in range(0,len(self.hands)-1):
          for b_i in range(a_i+1,len(self.hands)):
            a_stopped = self.moves[a_i] <= t
            b_stopped = self.moves[b_i] <= t
            if a_stopped and b_stopped: #both stopped
              # print(f"{t}s ({total}): {a_i+1} and {b_i+1} are both stopped.")
              continue
            if self.hands[a_i] == self.hands[b_i] and self.clockwise[a_i] == self.clockwise[b_i] and self.moves[a_i] == self.moves[b_i]:
              continue

            a_pos = self.pos[a_i]
            a_start = Fraction(a_pos,self.hands[a_i])
            a_cw = self.clockwise[a_i]
            if a_stopped:
              a_speed = Fraction(0)
            else:
              a_speed = Fraction(1,self.hands[a_i])
            

            b_pos = self.pos[b_i]
            b_start = Fraction(b_pos,self.hands[b_i])
            b_cw = self.clockwise[b_i]
            if b_stopped:
              b_speed = Fraction(0)
            else:
              b_speed = Fraction(1,self.hands[b_i])

            starting_gap = self.calc_gap(a_start,b_start,a_speed,b_speed,a_cw,b_cw)
            if starting_gap == 0 and t > 0:
              clock_meetings += 1 # hands started together and it is not the first turn
            ttp = self.time_to_pass(starting_gap,a_speed,b_speed,a_cw,b_cw)
            if starting_gap > 0 and 0 < ttp < 1:
              clock_meetings += 1 # hands meet sometime in their arc but do not land on the same spot
            if (t == self.moves[a_i]-1 or t== self.moves[b_i]-1) and ttp == 1 :
              clock_meetings +=1 # hands ending in the same spot are counted if it is the last turn

            # print(f"{t}s ({total}): {a_i+1} and {b_i+1} are {str(starting_gap.numerator).rjust(2)}/{str(starting_gap.denominator).ljust(2)}u apart. TTP: {ttp.real}s")

        for i in range(0,len(self.hands)):
          if self.moves[i] <= t:
            continue
          self.pos[i] = self.next(i,self.pos[i])
      print(f"hands {self.hands[0]}:{self.hands[1]}:{self.hands[2]}\nmeetings {clock_meetings}")
      total += clock_meetings
    return f"{total}"  
    # not 136871, 137202

  @staticmethod
  def calc_gap(a_start:Fraction,b_start:Fraction,a_speed:Fraction,b_speed:Fraction,a_cw:bool,b_cw:bool)->Fraction:

    sorted = Part2.max_speed(a_start,b_start,a_speed,b_speed,a_cw,b_cw)

    if sorted["f_cw"] and sorted["s_cw"]: #both CW
      dist = sorted["s_start"]  - sorted["f_start"]  
    elif not sorted["f_cw"] and not sorted["s_cw"]: #both CCW
      dist = sorted["f_start"]  - sorted["s_start"]
    elif sorted["f_cw"] and not sorted["s_cw"]: #a CW and b CCW
      dist = sorted["s_start"] - sorted["f_start"] 
    else: # b CW and a CCW
      dist = sorted["f_start"] -sorted["s_start"]
    if dist < 0:
      dist += 1
    return dist

  @staticmethod
  def time_to_pass(gap:Fraction,a_speed:Fraction,b_speed:Fraction,a_cw:bool,b_cw:bool)->float:
    sorted = Part2.max_speed(Fraction(0),Fraction(0),a_speed,b_speed,a_cw,b_cw)
    if a_cw == b_cw:
      if a_speed == b_speed:
        return -1
      return gap/(sorted["f_speed"] - sorted["s_speed"])
    else:
      return gap/(sorted["f_speed"] + sorted["s_speed"])

  @staticmethod
  def max_speed(a_start:Fraction,b_start:Fraction,a_speed:Fraction,b_speed:Fraction,a_cw:bool,b_cw:bool):
    if a_speed > b_speed:
      return {
      "f_start" : a_start,
      "s_start" : b_start,
      "f_speed":a_speed,
      "s_speed":b_speed,
      "f_cw" : a_cw,
      "s_cw" : b_cw
      }
    else:
      return {
      "f_start" : b_start,
      "s_start" :a_start,
      "f_speed":b_speed,
      "s_speed":a_speed,
      "f_cw" : b_cw,
      "s_cw" : a_cw}


  def next(self,i:int,from_val:int) -> int:
    if self.clockwise[i]:
      return (from_val+1) % self.hands[i]
    else:
      val = (from_val-1)
      if val == -1:
        val = self.hands[i]-1
      return val

  def prev(self,i:int,from_val:int) -> int:
    if not self.clockwise[i]:
      return (from_val+1) % self.hands[i]
    else:
      val = (from_val-1)
      if val == -1:
        val = self.hands[i]-1
      return val
