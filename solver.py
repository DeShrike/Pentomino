

WIDTH = 10
HEIGHT = 6

MAX_ROTATIONS = [2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0]

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

SHOW = "\033[?25h"
HIDE = "\033[?25l"

COLORS = [DIM, RED, GREEN, YELLOW, BLUE, VIOLET, BEIGE, WHITE, RED, GREEN, YELLOW, BLUE, VIOLET]

class Pento():
   def __init__(self, pento, max_rot: int) -> None:
      self.grid = pento
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

   def next_rotation(self) -> bool:
      self.rotate()
      return self.rotation >= self.max_rotations

class Solver():
   def __init__(self, w: int, h: int):
      self.width = w
      self.height = h
      self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
      self.next_ix = 0
      self.stack = []
      self.advances = 0
      self.pentos = [Pento(p, mr) for p, mr in zip(PENTOS, MAX_ROTATIONS)]
   
   def print(self) -> None:
      print(HIDE, end="")
      print(HOME, end="")
      print("-" * self.width * 4)
      for y in range(self.height):
         for x in range(self.width):
            print(COLORS[self.grid[y][x]], end="")
            print(f"{self.grid[y][x]:3} ", end="")
            print(RESET, end="")
         print("")
      print(SHOW, end="")

   def advance(self) -> None:
      self.next_ix = (self.next_ix + 1) % len(self.pentos)
      self.advances += 1

   def iscomplete(self) -> bool:
      return all( [all( [x != 0 for x in row]) for row in self.grid])

   def next_piece(self) -> Pento:
      while True:
         p = self.pentos[self.next_ix]
         if p.placed:
            self.advance()
            continue

         if p.next_rotation():
            p.reset()
            self.advance()
            continue

         return p

   def try_place_at(self, p: Pento, x: int, y: int) -> bool:
      # print(f"Try place #{p.id} (Size=({p.width}x{p.height})) at ({x},{y}) with rotations {p.rotation}")
      for yy in range(p.height):
         for xx in range(p.width):
            if self.grid[y + yy][x + xx] > 0 and p.grid[yy][xx] > 0:
               return False

      # print("Placing")
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
      
   def dostep(self) -> bool:
      self.advances = 0
      while True:
         p = self.next_piece()
         if self.try_place(p):
            self.stack.append(p)
            return True
         else:
            if self.advances >= 12:
               return False
            continue

   def remove_block(self, id: int) -> None:
      for y in range(self.height):
         for x in range(self.width):
            self.grid[y][x] = 0 if self.grid[y][x] == id else self.grid[y][x]

   def run(self):
      while (True):
         ret = self.dostep()
         self.print()
         print(f"Stack size: {len(self.stack)}   {ret}")
         for s in self.stack:
            print(s)
         #a = input()
         if self.iscomplete():
            print("Found One")
         if not ret:
            last = self.stack.pop()
            last.placed = False
            self.remove_block(last.id)
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

if __name__ == "__main__":
   s = Solver(WIDTH, HEIGHT)
   s.run()

