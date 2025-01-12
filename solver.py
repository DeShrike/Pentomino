# Pentomino Solver

WITH_FLIP = False

# 110 solutions without flip
# 4678 solutions with flip
WIDTH = 10
HEIGHT = 6

# 40 solutions without flip
# 2020 solutions with flip
# WIDTH = 12
# HEIGHT = 5

# 16 solutions without flip
# 736 solutions with flip
#WIDTH = 15
#HEIGHT = 4

# No solutions without flip
# 4 solutions with flip
#WIDTH = 20
#HEIGHT = 3

# 4 solutions without flip
# 260 solutions with flip
#WIDTH = 8
#HEIGHT = 8

MAX_ROTATIONS = [2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1]

CANFLIP = [False, False, False, True, False, True, True, True, True, False, False, False]

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
   def __init__(self, grid, max_rot: int, canflip: bool) -> None:
      self.grid = [row[:] for row in grid]
      self.orig_grid = [row[:] for row in grid]
      self.max_rotations = max_rot
      self.can_flip = canflip
      self.width = len(self.grid[0])
      self.height = len(self.grid)
      for x in self.grid[0]:
         if x > 0: 
            self.id = x
            break

   def __repr__(self):
      return f"Pento #{self.id} "

   def flip(self) -> None:
      self.grid = self.grid[::-1]
      self.width = len(self.grid[0])
      self.height = len(self.grid)

   def rotate(self) -> None:
      self.grid = list(zip(*self.grid[::-1]))
      self.width = len(self.grid[0])
      self.height = len(self.grid)

   def set_rotation(self, r: int) -> None:
      self.grid = [row[:] for row in self.orig_grid]
      self.width = len(self.grid[0])
      self.height = len(self.grid)
      for _ in range(r):
         self.rotate()

   def orientations(self) -> "Pento":
      self.grid = [row[:] for row in self.orig_grid]
      self.width = len(self.grid[0])
      self.height = len(self.grid)
      for r in range(self.max_rotations):
         self.set_rotation(r)
         yield self

      if WITH_FLIP and self.can_flip:
         for r in range(self.max_rotations):
            self.set_rotation(r)
            self.flip()
            yield self


class StackItem():
   def __init__(self, id: int, x: int, y: int, rotation: int) -> None:
      self.id = id
      self.x = x
      self.y = y
      self.rotation = rotation

   def __str__(self):
      return f"#{self.id}|{self.x},{self.y}|{self.rotation}"


class Solver():
   def __init__(self, w: int, h: int):
      self.width = w
      self.height = h
      self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
      self.floodfill_grid = None
      self.pentos = [Pento(p, mr, cf) for p, mr, cf in zip(PENTOS, MAX_ROTATIONS, CANFLIP)]
      self.stepcount = 0
      self.solutions = 0
      if self.width == 8 and self.height == 8:
         self.grid[3][3] = 99
         self.grid[3][4] = 99
         self.grid[4][3] = 99
         self.grid[4][4] = 99

   def print(self, thegrid) -> None:
      # print(HIDE, end="")
      print("-" * self.width * 4)
      for y in range(self.height):
         for x in range(self.width):
            ix = thegrid[y][x]
            color = COLORS[ix] if ix < 99 else DIM
            print(color, end="")
            print(f"{thegrid[y][x]:3} ", end="")
            print(RESET, end="")
         print("")
      print("-" * self.width * 4)
      #print(SHOW, end="")

   def print_floodfill(self) -> None:
      # print(HIDE, end="")
      print("-" * self.width * 4)
      for y in range(self.height):
         for x in range(self.width):
            ix = self.floodfill_grid[y][x]
            color = COLORS[ix] if ix < 99 else DIM
            print(color, end="")
            print(f"{ix:3} ", end="")
            print(RESET, end="")
         print("")
      #print(SHOW, end="")

   def iscomplete(self, thegrid) -> bool:
      return all([all([x != 0 for x in row]) for row in thegrid])

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

   def check_floodfill(self, thegrid, p: Pento, x: int, y: int) -> bool:
      if x + p.width > self.width:
         return False

      if y + p.height > self.height:
         return False

      self.floodfill_grid = [row[:] for row in thegrid]
      for yy in range(p.height):
         for xx in range(p.width):
            if self.floodfill_grid[y + yy][x + xx] == 0:
               self.floodfill_grid[y + yy][x + xx] = p.grid[yy][xx]

      for yy in range(self.height):
         for xx in range(self.width):
            if self.floodfill_grid[yy][xx] == 0:
               count = self.do_floodfill(xx, yy)
               if count % 5 != 0:
                  return False

      return True

   def try_place_at(self, thegrid, p: Pento, x: int, y: int) -> bool:
      offset = 0
      while p.grid[0][offset] == 0:
         offset += 1
         
      if x - offset < 0:
         return False
      
      x -= offset
      
      if x + p.width > self.width:
         return False

      if y + p.height > self.height:
         return False

      for yy in range(p.height):
         for xx in range(p.width):
            if thegrid[y + yy][x + xx] > 0 and p.grid[yy][xx] > 0:
               return False

      if not self.check_floodfill(thegrid, p, x, y):
         return False

      for yy in range(p.height):
         for xx in range(p.width):
            if p.grid[yy][xx] > 0:
               thegrid[y + yy][x + xx] = p.grid[yy][xx]

      return True

   def remove_piece(self, thegrid, id: int):
      for y in range(self.height):
         for x in range(self.width):
            if thegrid[y][x] == id:
               thegrid[y][x] = 0

   def find_next_spot(self, thegrid) -> (int, int):
      for y in range(self.height):
         for x in range(self.width):
            if thegrid[y][x] == 0:
               return (x, y)

      return None

   def do_step(self, thegrid, thestack: [StackItem]) -> None:
      # print(CLS + HOME, end="")
      self.stepcount += 1
      
      next_spot = self.find_next_spot(thegrid)
      if next_spot is None:
         self.solutions += 1
         print(f"Solution {self.solutions}  (after {self.stepcount} steps):")
         self.print(thegrid)
         self.show_stack(thestack)
         print("-" * self.width * 4)
         # a = input()
         return

      x, y = next_spot
      for p in self.pentos:
         if any([ s.id == p.id for s in thestack ]):
            continue

         for pp in p.orientations():
            if self.try_place_at(thegrid, pp, x, y):
               # self.print(thegrid)
               newstack = thestack[:]
               newstack.append(StackItem(pp.id, x, y, 0))
               newgrid = [row[:] for row in thegrid]
               #print(f"{self.stepcount}")
               #self.show_stack(newstack)
               #a = input()
               self.do_step(newgrid, newstack)
               self.remove_piece(thegrid, pp.id)

   def show_stack(self, thestack: [StackItem]) -> None:
      print("Stack: ", end="")
      for s in thestack:
         print(f"{s} ", end="")
      print("")

   def run(self):
      print(CLS + HOME, end="")
      thegrid = [row[:] for row in self.grid]
      thestack = []
      self.do_step(thegrid, thestack)


if __name__ == "__main__":
   s = Solver(WIDTH, HEIGHT)
   s.run()

