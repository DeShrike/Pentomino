import os
import itertools
from svg.constants import *
from svg.layer import Layer
from svg.group import Group
from svg.path import Path
from svg.text import Text
from svg.ellipse import Ellipse
from svg.helpers import create_rounded_box, save, add_rounded_corner
from config import *

offset_x = 5
offset_y = 5

x_squares = 10
y_squares = 6

def add_hline(x1: int, y1: int, x2: int, y2: int, cut: bool) -> Path:
   p = Path(f"line_{x1}_{y1}_{x2}_{y2}", False)
   p.color = BLACK if cut else CYAN
   xx1 = offset_x + (x1 * SQUARE_SIZE) + LEFT_BORDER + CORNER_RADIUS
   yy1 = offset_y + (y1 * SQUARE_SIZE) + TOP_BORDER
   xx2 = offset_x + (x2 * SQUARE_SIZE) + LEFT_BORDER - CORNER_RADIUS
   yy2 = offset_y + (y2 * SQUARE_SIZE) + TOP_BORDER
   p.add_node(xx1, yy1)
   p.add_node(xx2, yy2)
   return p

def add_vline(x1: int, y1: int, x2: int, y2: int, cut: bool) -> Path:
   p = Path(f"line_{x1}_{y1}_{x2}_{y2}", False)
   p.color = BLACK if cut else CYAN
   xx1 = offset_x + (x1 * SQUARE_SIZE) + LEFT_BORDER
   yy1 = offset_y + (y1 * SQUARE_SIZE) + TOP_BORDER + CORNER_RADIUS
   xx2 = offset_x + (x2 * SQUARE_SIZE) + LEFT_BORDER
   yy2 = offset_y + (y2 * SQUARE_SIZE) + TOP_BORDER - CORNER_RADIUS
   p.add_node(xx1, yy1)
   p.add_node(xx2, yy2)
   return p

def add_corners(x: int, y: int, sides: str) -> Path:
   # sides: 1 = BR, 2 = BL, 3 = TR, 4 = TL

   p = Path(f"corners_{x}_{y}_{sides}", False)
   p.color = BLACK
   
   xx = offset_x + (x * SQUARE_SIZE) + LEFT_BORDER
   yy = offset_y + (y * SQUARE_SIZE) + TOP_BORDER
   
   for side in sides:
      if side == "1":
         add_rounded_corner(p, xx, yy, CORNER_RADIUS, "TL")
      if side == "2":
         add_rounded_corner(p, xx, yy, CORNER_RADIUS, "TR")
      if side == "3":
         add_rounded_corner(p, xx, yy, CORNER_RADIUS, "BR")
      if side == "4":
         add_rounded_corner(p, xx, yy, CORNER_RADIUS, "BL")

   return p
      

def create_box(layer):
   box_group = Group(f"box")
   layer.groups.append(box_group)

   outer_width = RIGHT_BORDER + LEFT_BORDER + (x_squares * SQUARE_SIZE)
   outer_height = TOP_BORDER + BOTTOM_BORDER + (y_squares * SQUARE_SIZE)

   p = create_rounded_box(0, 0, outer_width, outer_height, BIG_CORNER_RADIUS, RED)
   p.move((offset_x, offset_y))

   box_group.paths.append(p)

   inner_width = (x_squares * SQUARE_SIZE)
   inner_height = (y_squares * SQUARE_SIZE)

   p = create_rounded_box(LEFT_BORDER, TOP_BORDER, inner_width, inner_height, CORNER_RADIUS, RED)
   p.move((offset_x, offset_y))

   box_group.paths.append(p)

   text_x = LEFT_BORDER + (y_squares * SQUARE_SIZE) / 2
   text_y = TOP_BORDER + (y_squares * SQUARE_SIZE) + TOP_BORDER

   t = Text(offset_x + text_x, offset_y + text_y, MAGENTA, "Makerslab RSLopPOST")
   t.fontsize = 4
   t.color = None
   t.fillcolor = BLUE
   box_group.add_text(t)


def create_bottom(layer):
   bottom_group = Group(f"bottom")
   layer.groups.append(bottom_group)

   bottom_width = RIGHT_BORDER + LEFT_BORDER + (x_squares * SQUARE_SIZE)
   bottom_height = TOP_BORDER + BOTTOM_BORDER + (y_squares * SQUARE_SIZE)

   p = create_rounded_box(0, 0, bottom_width, bottom_height, BIG_CORNER_RADIUS, RED)
   p.move((offset_x, offset_y + bottom_height + 10))

   bottom_group.paths.append(p)


def create_pentominos(layer):
   pentomino_group = Group(f"pentominos")
   layer.groups.append(pentomino_group)

   # Top row
   for x in range(1, 10):
      c = add_corners(x, 0, "21")
      pentomino_group.paths.append(c)
   
   for y in range(1, 6):
      for x in range(1, 10):
         if x == 2 and y == 1:
            continue
         c = add_corners(x, y, "4321")
         pentomino_group.paths.append(c)

   # Bottom row
   for x in range(1, 10):
      c = add_corners(x, 6, "43")
      pentomino_group.paths.append(c)

   # Left column
   for y in range(1, 6):
      c = add_corners(0, y, "14")
      pentomino_group.paths.append(c)

   # Right column
   for y in range(1, 6):
      c = add_corners(10, y, "32")
      pentomino_group.paths.append(c)

   lines_group = Group(f"lines")
   layer.groups.append(lines_group)

   # Vertical lines
   x = 1
   l = add_vline(x, 0, x, 1, True)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, True)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, True)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, True)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, True)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, False)
   lines_group.paths.append(l)

   x = 2
   l = add_vline(x, 0, x, 2, False)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, True)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, True)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, True)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, False)
   lines_group.paths.append(l)

   x = 3
   l = add_vline(x, 0, x, 1, True)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, True)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, True)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, True)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, False)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, True)
   lines_group.paths.append(l)

   x = 4
   l = add_vline(x, 0, x, 1, False)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, True)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, False)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, True)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, True)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, False)
   lines_group.paths.append(l)

   x = 5
   l = add_vline(x, 0, x, 1, False)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, True)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, True)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, False)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, False)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, True)
   lines_group.paths.append(l)

   x = 6
   l = add_vline(x, 0, x, 1, False)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, False)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, True)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, False)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, True)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, False)
   lines_group.paths.append(l)

   x = 7
   l = add_vline(x, 0, x, 1, True)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, False)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, False)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, True)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, True)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, False)
   lines_group.paths.append(l)

   x = 8
   l = add_vline(x, 0, x, 1, False)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, False)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, True)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, True)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, False)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, True)
   lines_group.paths.append(l)

   x = 9
   l = add_vline(x, 0, x, 1, False)
   lines_group.paths.append(l)
   l = add_vline(x, 1, x, 2, True)
   lines_group.paths.append(l)
   l = add_vline(x, 2, x, 3, True)
   lines_group.paths.append(l)
   l = add_vline(x, 3, x, 4, False)
   lines_group.paths.append(l)
   l = add_vline(x, 4, x, 5, True)
   lines_group.paths.append(l)
   l = add_vline(x, 5, x, 6, False)
   lines_group.paths.append(l)

   # Horizontal lines
   y = 1
   l = add_hline(0, y, 1, y, False)
   lines_group.paths.append(l)
   l = add_hline(1, y, 3, y, False)
   lines_group.paths.append(l)
   l = add_hline(3, y, 4, y, True)
   lines_group.paths.append(l)
   l = add_hline(4, y, 5, y, False)
   lines_group.paths.append(l)
   l = add_hline(5, y, 6, y, True)
   lines_group.paths.append(l)
   l = add_hline(6, y, 7, y, True)
   lines_group.paths.append(l)
   l = add_hline(7, y, 8, y, True)
   lines_group.paths.append(l)
   l = add_hline(8, y, 9, y, True)
   lines_group.paths.append(l)
   l = add_hline(9, y, 10, y, False)
   lines_group.paths.append(l)

   y = 2
   l = add_hline(0, y, 1, y, False)
   lines_group.paths.append(l)
   l = add_hline(1, y, 2, y, False)
   lines_group.paths.append(l)
   l = add_hline(2, y, 3, y, True)
   lines_group.paths.append(l)
   l = add_hline(3, y, 4, y, False)
   lines_group.paths.append(l)
   l = add_hline(4, y, 5, y, True)
   lines_group.paths.append(l)
   l = add_hline(5, y, 6, y, True)
   lines_group.paths.append(l)
   l = add_hline(6, y, 7, y, True)
   lines_group.paths.append(l)
   l = add_hline(7, y, 8, y, True)
   lines_group.paths.append(l)
   l = add_hline(8, y, 9, y, False)
   lines_group.paths.append(l)
   l = add_hline(9, y, 10, y, False)
   lines_group.paths.append(l)

   y = 3
   l = add_hline(0, y, 1, y, False)
   lines_group.paths.append(l)
   l = add_hline(1, y, 2, y, True)
   lines_group.paths.append(l)
   l = add_hline(2, y, 3, y, True)
   lines_group.paths.append(l)
   l = add_hline(3, y, 4, y, False)
   lines_group.paths.append(l)
   l = add_hline(4, y, 5, y, True)
   lines_group.paths.append(l)
   l = add_hline(5, y, 6, y, False)
   lines_group.paths.append(l)
   l = add_hline(6, y, 7, y, True)
   lines_group.paths.append(l)
   l = add_hline(7, y, 8, y, False)
   lines_group.paths.append(l)
   l = add_hline(8, y, 9, y, True)
   lines_group.paths.append(l)
   l = add_hline(9, y, 10, y, True)
   lines_group.paths.append(l)

   y = 4
   l = add_hline(0, y, 1, y, False)
   lines_group.paths.append(l)
   l = add_hline(1, y, 2, y, False)
   lines_group.paths.append(l)
   l = add_hline(2, y, 3, y, False)
   lines_group.paths.append(l)
   l = add_hline(3, y, 4, y, True)
   lines_group.paths.append(l)
   l = add_hline(4, y, 5, y, True)
   lines_group.paths.append(l)
   l = add_hline(5, y, 6, y, True)
   lines_group.paths.append(l)
   l = add_hline(6, y, 7, y, False)
   lines_group.paths.append(l)
   l = add_hline(7, y, 8, y, False)
   lines_group.paths.append(l)
   l = add_hline(8, y, 9, y, True)
   lines_group.paths.append(l)
   l = add_hline(9, y, 10, y, False)
   lines_group.paths.append(l)

   y = 5
   l = add_hline(0, y, 1, y, True)
   lines_group.paths.append(l)
   l = add_hline(1, y, 2, y, False)
   lines_group.paths.append(l)
   l = add_hline(2, y, 3, y, True)
   lines_group.paths.append(l)
   l = add_hline(3, y, 4, y, False)
   lines_group.paths.append(l)
   l = add_hline(4, y, 5, y, True)
   lines_group.paths.append(l)
   l = add_hline(5, y, 6, y, False)
   lines_group.paths.append(l)
   l = add_hline(6, y, 7, y, True)
   lines_group.paths.append(l)
   l = add_hline(7, y, 8, y, True)
   lines_group.paths.append(l)
   l = add_hline(8, y, 9, y, True)
   lines_group.paths.append(l)
   l = add_hline(9, y, 10, y, False)
   lines_group.paths.append(l)

def create_it():
   plate = Layer("Plate")

   create_box(plate)
   create_pentominos(plate)
   create_bottom(plate)


   save(plate, os.path.join(OUTPUT_FOLDER, "pentomino.svg"), "PENTOMINO", PAPER_WIDTH, PAPER_HEIGHT)


# def add_r(g: Group):
#     """
#     <path
#        class="filcyan str0"
#        d="m 135.7374,142.79676 c -23.00236,-11.49018 -23.16939,-11.59428 -23.97234,-14.94134 -0.35545,-1.48168 -0.33379,-2.09036 0.13129,-3.69017 0.83225,-2.86285 2.40944,-4.11538 6.95611,-5.52419 6.75399,-2.09276 15.21154,-6.94253 20.02372,-11.4821 9.9135,-9.351888 10.78706,-21.265948 2.18438,-29.791688 -3.1022,-3.07444 -6.10555,-4.936529 -10.0808,-6.250117 -3.95034,-1.305355 -9.70961,-1.374792 -13.56675,-0.163567 -10.40236,3.266564 -16.02113,9.998214 -19.186301,22.986424 -0.49648,2.03729 -1.55093,7.276048 -2.34323,11.641668 -3.21639,17.72255 -5.46903,24.67666 -10.341939,31.9264 -3.254255,4.84157 -8.720716,9.14602 -13.904387,10.94872 -9.430442,3.27959 -19.195281,2.2781 -30.587606,-3.13706 -6.913901,-3.28642 -12.444705,-7.16823 -13.592989,-9.54026 -2.602216,-5.37547 1.999899,-11.39983 7.867617,-10.29904 0.674635,0.12657 2.788128,1.28059 4.69665,2.56451 8.4573,5.68946 16.978195,8.48878 22.9967,7.55497 5.985461,-0.92867 9.165506,-3.30326 12.109429,-9.04229 2.797789,-5.45414 3.952149,-9.71542 6.637927,-24.50373 2.337478,-12.870508 4.181306,-19.137728 7.524623,-25.576388 5.005145,-9.639067 14.056606,-16.775298 25.109696,-19.79666 3.19201,-0.872534 4.0986,-0.964931 9.52501,-0.970764 5.08961,-0.0055 6.41598,0.109745 8.7643,0.761315 7.48092,2.075673 13.05368,5.225371 18.23213,10.304719 3.73082,3.65942 5.79587,6.481728 7.60052,10.38768 4.36979,9.45784 3.83952,20.4192 -1.45784,30.135428 -3.58265,6.57117 -10.90154,13.73276 -18.4342,18.03801 -1.18818,0.67909 -2.16504,1.31591 -2.17081,1.41514 -0.006,0.0992 5.56669,2.95673 12.38325,6.35001 6.81656,3.39327 13.0035,6.60401 13.74875,7.13499 5.33785,3.80309 2.7779,12.41671 -3.83232,12.89485 l -2.03516,0.14721 z"
#        id="RoeselareR"
#        sodipodi:nodetypes="ssssssssssssssssssssscssssscssscs" />
# 	"""


def main():
   create_it()

if __name__ == "__main__":
   main()
