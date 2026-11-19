from days.base_part import BasePart

def mod_one(x:float) -> float:
  return ((x % 1.0) + 1.0) % 1.0

class Part1(BasePart):
  def __init__(self):
    super().__init__(13,1,True)
    input = self.get_input_lines()
    self.hands = list(map(lambda x: int(x),input[0][6:].split(":")))
    self.clockwise = list(map(lambda x: x == "CW",input[1][10:].split(":")))
    self.pos = list(map(lambda x: int(x),input[2][8:].split(":")))
    self.moves = list(map(lambda x: int(x),input[3][5:].split(":")))

  def run(self) -> str:

    total = 0
    for t in range(0,max(self.moves)):
      movements:list[tuple[int,int,bool]] = [] # (current,total,stopped)
      for i in range(0,len(self.hands)):
        if self.moves[i] <= t:
          movements.append((self.pos[i],self.hands[i],True))
          continue
        self.pos[i] = self.next(i,self.pos[i])
        movements.append((self.pos[i],self.hands[i],False))

      for a_i in range(0,len(movements)-1):
        for b_i in range(a_i+1,len(movements)):
          a = movements[a_i]
          b = movements[b_i]
          if a[2] and b[2]: #both stopped
            continue

          a_min = self.prev(a_i,a[0])
          a_max = a[0]
          a_start = a_min/a[1]
          a_end = a_max/a[1]
          a_cw = self.clockwise[a_i]
          a_speed = 1/a[1]
          

          b_min = self.prev(b_i,b[0])
          b_max = b[0]
          b_start = b_min/b[1]
          b_end = b_max/b[1]
          b_cw = self.clockwise[b_i]
          b_speed = 1/b[1]

          if a[2]:
            a_speed = 0
            a_start = a_end
            if (b_cw and (mod_one(a_start - b_start) / b_speed) < 1.0) or (not b_cw and (mod_one(b_start - a_start) / b_speed) < 1.0):
              total += 1
              continue
          
          if b[2]:
            b_speed = 0
            b_start = b_end
            if (a_cw and (mod_one(b_start - a_start) / a_speed) < 1.0) or (not a_cw and (mod_one(a_start - b_start) / a_speed) < 1.0):
              total += 1
              continue
          

          if a_speed > b_speed:
            f_speed = a_speed
            s_speed = b_speed
            f_start = a_start
            s_start = b_start
          else:
            f_speed = b_speed
            s_speed = a_speed
            f_start = b_start
            s_start = a_start
          
          starting_gap = self.calc_gap(a_start,b_start,a_speed,b_speed,a_cw,b_cw)
          


        
    return f"{total}"  

  @staticmethod
  def calc_gap(a_start:float,b_start:float,a_speed:float,b_speed:float,a_cw:bool,b_cw:bool)->float:

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
  def time_to_pass(gap:float,a_speed:float,b_speed:float,a_cw:bool,b_cw:bool)->float:
    sorted = Part1.max_speed(0,0,a_speed,b_speed,a_cw,b_cw)
    if a_cw == b_cw:
      return gap/(sorted["f_speed"] - sorted["s_speed"])
    else:
      return gap/(sorted["f_speed"] + sorted["s_speed"])

  @staticmethod
  def max_speed(a_start:float,b_start:float,a_speed:float,b_speed:float,a_cw:bool,b_cw:bool):
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
