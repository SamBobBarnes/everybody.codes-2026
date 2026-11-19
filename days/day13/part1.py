from fractions import Fraction

from days.base_part import BasePart

def mod_one(x:float) -> float:
  return ((x % 1.0) + 1.0) % 1.0

class Part1(BasePart):
  def __init__(self):
    super().__init__(13,1)
    input = self.get_input_lines()
    self.hands = list(map(lambda x: int(x),input[0][6:].split(":")))
    self.clockwise = list(map(lambda x: x == "CW",input[1][10:].split(":")))
    self.pos = list(map(lambda x: int(x),input[2][8:].split(":")))
    self.moves = list(map(lambda x: int(x),input[3][5:].split(":")))

  def run(self) -> str:

    total = 0
    for t in range(0,max(self.moves)):

      for a_i in range(0,len(self.hands)-1):
        for b_i in range(a_i+1,len(self.hands)):
          a_stopped = self.moves[a_i] <= t
          b_stopped = self.moves[b_i] <= t
          if a_stopped and b_stopped: #both stopped
            print(f"{t}s ({total}): {a_i+1} and {b_i+1} are both stopped.S")
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
            total += 1
          ttp = self.time_to_pass(starting_gap,a_speed,b_speed,a_cw,b_cw)
          if starting_gap > 0 and 0 < ttp < 1:
            total += 1
          if t == max(self.moves)-1 and ttp == 1:
            total +=1

          print(f"{t}s ({total}): {a_i+1} and {b_i+1} are {str(starting_gap.numerator).rjust(2)}/{str(starting_gap.denominator).ljust(2)}u apart. TTP: {ttp.real}s")

      for i in range(0,len(self.hands)):
        if self.moves[i] <= t:
          continue
        self.pos[i] = self.next(i,self.pos[i])


          


        
    return f"{total}"  

  @staticmethod
  def calc_gap(a_start:Fraction,b_start:Fraction,a_speed:Fraction,b_speed:Fraction,a_cw:bool,b_cw:bool)->Fraction:

    sorted = Part1.max_speed(a_start,b_start,a_speed,b_speed,a_cw,b_cw)

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
    sorted = Part1.max_speed(Fraction(0),Fraction(0),a_speed,b_speed,a_cw,b_cw)
    if a_cw == b_cw:
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
