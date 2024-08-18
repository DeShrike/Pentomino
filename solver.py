

WIDTH = 10
HEIGHT = 6

MAX_ROTATIONS = [2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1]

PENTOS = [
   [
      [1, 1, 1, 1, 1],
   ],
   [
      [2, 2, 0],
      [0, 2, 0],
      [0, 2, 2],
   ],
   [
      [3, 3, 3],
      [3, 0, 0],
      [3, 0, 0],
   ],
   [
      [4, 0, 0],
      [4, 4, 4],
      [0, 4, 0],
   ],
   [
      [5, 5, 5],
      [0, 5, 0],
      [0, 5, 0],
   ],
   [
      [6, 6, 6, 6],
      [0, 6, 0, 0],
   ],
   [
      [7, 7],
      [7, 7],
      [7, 0],
   ],
   [
      [8, 8, 8, 8],
      [0, 0, 0, 8],
   ],
   [
      [9, 9, 0, 0],
      [0, 9, 9, 9],
   ],
   [
      [10, 10, 10],
      [10,  0, 10],
   ],
   [
      [ 0, 11, 11],
      [11, 11,  0],
      [11,  0,  0],
   ],
   [
      [ 0, 12,  0],
      [12, 12, 12],
      [ 0, 12,  0],
   ],
]

RESET = "\033[0m"
DIM = "\033[90m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
VIOLET = "\033[95m"
BEIGE = "\033[96m"
WHITE = "\033[97m"

HOME = "\033[1;1f"
CLS = "\033[2J"

SHOW = "\033[?25h"
HIDE = "\033[?25l"

COLORS = [DIM, RED, GREEN, YELLOW, BLUE, VIOLET, BEIGE, WHITE, RED, GREEN, YELLOW, BLUE, VIOLET]

class Pento():
   def __init__(self, pento, max_rot: int) -> None:
      self.grid = [row[:] for row in pento]
      self.orig_grid = [row[:] for row in pento]
      self.max_rotations = max_rot
      self.reset()
      self.width = len(self.grid[0])
      self.height = len(self.grid)
      for x in self.grid[0]:
         if x > 0: 
            self.id = x
            break

   def __repr__(self):
      return f"#{self.id} {self.placed} ({self.x}, {self.y})"

   def rotate(self) -> None:
      self.grid = list(zip(*self.grid[::-1]))
      self.width = len(self.grid[0])
      self.height = len(self.grid)
      self.rotation += 1

   def reset(self) -> None:
      self.rotation = -1
      self.x = -1
      self.y = -1
      self.placed = False
      self.grid = [row[:] for row in self.orig_grid]

   def next_rotation(self) -> bool:
      self.rotate()
      if self.rotation >= self.max_rotations:
         #print(f" #{self.id} R {self.rotation} >= {self.max_rotations}")
         #a = input()
         self.reset()
         return False
      return True

class Solver():
   def __init__(self, w: int, h: int):
      self.width = w
      self.height = h
      self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
      self.floodfill_grid = None
      self.stack = []
      self.pentos = [Pento(p, mr) for p, mr in zip(PENTOS, MAX_ROTATIONS)]
      self.next_ix = 0
      self.last_popped_id = -1
      self.advances = 0

   def print(self) -> None:
      # print(HIDE, end="")
      print("-" * self.width * 4)
      for y in range(self.height):
         for x in range(self.width):
            ix = self.grid[y][x]
            print(COLORS[ix], end="")
            print(f"{self.grid[y][x]:3} ", end="")
            print(RESET, end="")
         print("")
      #print(SHOW, end="")

   def iscomplete(self) -> bool:
      return all( [all( [x != 0 for x in row]) for row in self.grid])

   def ff_neighbours(self, x: int, y: int):
      nn = [(1, 0), (-1, 0), (0, 1), (0, -1)]
      for n in nn:
         xx = x + n[0]
         yy = y + n[1]
         if xx < 0 or yy < 0 or xx >= self.width or yy >= self.height:
            continue
         yield (xx, yy)
         
   def do_floodfill(self, x: int, y: int) -> int:
      stak = [(x, y)]
      points = [(x, y)]
      self.floodfill_grid[y][x] = 100
      while len(stak) > 0:
         s = stak.pop()
         for n in self.ff_neighbours(s[0], s[1]):
            if self.floodfill_grid[n[1]][n[0]] == 0:
               self.floodfill_grid[n[1]][n[0]] = 100
               points.append(n)
               stak.append(n)
               
      return len(points)

   def check_floodfill(self, p: Pento, x: int, y: int) -> bool:
      self.floodfill_grid = [row[:] for row in self.grid]
      for yy in range(p.height):
         for xx in range(p.width):
            if self.floodfill_grid[yy][xx] > 0:
               self.floodfill_grid[y + yy][x + xx] = p.grid[yy][xx]

      for yy in range(self.height):
         for xx in range(self.width):
            if self.floodfill_grid[yy][xx] == 0:
               count = self.do_floodfill(xx, yy)
               if count % 5 != 0:
                  return False

      return True

   def try_place_at(self, p: Pento, x: int, y: int) -> bool:
      for yy in range(p.height):
         for xx in range(p.width):
            if self.grid[y + yy][x + xx] > 0 and p.grid[yy][xx] > 0:
               return False

      if not self.check_floodfill(p, x, y):
         return False

      p.placed = True
      p.x = x
      p.y = y
      for yy in range(p.height):
         for xx in range(p.width):
            if p.grid[yy][xx] > 0:
               self.grid[y + yy][x + xx] = p.grid[yy][xx]

      return True

   def try_place(self, p: Pento) -> bool:
      for y in range(self.height - p.height + 1):
         for x in range(self.width - p.width + 1):
            if self.try_place_at(p, x, y):
               return True
      return False

   def advance(self):
      self.next_ix = (self.next_ix + 1) % len(self.pentos)
      self.advances += 1

   def next_piece(self) -> Pento:
      while True:
         p = self.pentos[self.next_ix]
         if p.placed:
            self.advance()
            if self.advances > 12:
               self.advances = 0
               return None
            continue
         if not p.next_rotation():
            self.advance()
            if self.advances > 12:
               self.advances = 0
               return None
            continue

         return p

   def show_status(self) -> None:
      for p in self.pentos:
         if p.id != self.last_popped_id and p.placed == False:
            print(RED + f"{p.id:2} " + RESET, end="")
         elif p.placed:
            print(GREEN + f"{p.id:2} " + RESET, end="")
         else:
            print(WHITE + f"{p.id:2} " + RESET, end="")
      print("")
      for p in self.pentos:
         if p.id == self.next_ix + 1:
            print(RED + f" ^ " + RESET, end="")
         else:
            print(WHITE + f"   " + RESET, end="")
      print("")

   def init_step(self) -> None:
      for p in self.pentos:
         if p.id != self.last_popped_id and p.placed == False:
            p.reset()
      self.show_status()
      self.last_popped_id = -1

   def dostep(self) -> bool:
      print(CLS + HOME, end="")

      self.init_step()

      print("Trying: ", end="")
      while True:
         p = self.next_piece()
         if p is None:
            print(" NONE")
            self.show_status()
            return False

         print(f"#{p.id}({p.rotation}) ", end="")
         if self.try_place(p):
            self.advance()
            self.stack.append(p)
            print("Ok")
            self.show_status()
            return True
         else:
            #self.advance()
            pass

   def remove_block(self, id: int) -> None:
      for y in range(self.height):
         for x in range(self.width):
            self.grid[y][x] = 0 if self.grid[y][x] == id else self.grid[y][x]

   def show_stack(self, ret: bool) -> None:
      print(f"Stack: Len = {len(self.stack)}   ", end="")
      for s in self.stack:
         print(f"{s.id}({s.rotation}) ", end="")
      print(f"  {ret}")

   def run(self):
      while (True):
         ret = self.dostep()
         self.print()
         self.show_stack(ret)
         if self.iscomplete():
            print("Found One")
         if not ret:
            last = self.stack.pop()
            last.placed = False
            print(f"Popped: #{last.id}({last.rotation})")
            self.last_popped_id = last.id
            self.next_ix = last.id - 1
            self.remove_block(last.id)
            self.show_stack(ret)
            """
            while True:
               last = self.stack.pop()
               last.placed = False
               self.remove_block(last.id)
               if last.next_rotation():
                  last.reset()
                  self.advance()
                  self.advances = 0
               else:
                  break
            """
         a = input()

if __name__ == "__main__":
   s = Solver(WIDTH, HEIGHT)
   s.run()

