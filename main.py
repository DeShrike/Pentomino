import os
import itertools
from svg.constants import *
from svg.layer import Layer
from svg.group import Group
from svg.path import Path
from svg.text import Text
from svg.ellipse import Ellipse
from svg.helpers import create_rounded_box, save, distance
from config import *

offset_x = 5
offset_y = 5

def create_teeth(g: Group, p: Path, horizontal: bool, forward: bool, x: int, y: int, data) -> Path:
	state = True
	attach_added = False
	pd = PINDEPTH if forward else -PINDEPTH
	for d in data:
		add_attach = (len(d) == 3)
		r = d[0]
		s = d[1] if forward else -d[1]
		ys = (pd if state != r else 0)
		ys = ys if state else -ys
		if horizontal:
			if add_attach and attach_added == False:
				attach_added = True
				ox = x + s
				x += s / 2
				x = x + ((ATTACH_WIDTH / 2) * (-1 if forward else 1))
				p.add_node(x, y)
				g.add_path(p)

				y = p.last_y()

				p = Path(p.id + "ATT", False)
				p.add_node(x, y)

				x = x + ((ATTACH_WIDTH) * (1 if forward else -1))
				p.add_node(x, y)
				p.color = MAGENTA
				g.add_path(p)

				p = Path(p.id + "X", False)
				p.add_node(x, y)
				x = ox
			else:	
				x += s
			y = y + ys
		else:
			y += s
			x = x + -ys
		state = r

		p.add_node(x, y)
	return p

def left_right_side(ox: int, oy: int) -> Group:
	outline = Group(f"OutlineLeftRight{ox}{oy}")

	points = [
		(True, 0), 
		(True, PINSIZE),
		(True, PINSIZE),

		(False, 0),
		(False, PINSIZE),

		(True,  0),
		(True, PINSIZE, "A"),

		(False, 0),
		(False, PINSIZE),

		(True,  0),
		(True, PINSIZE),
	]

	p = Path(f"outlineA{ox}{oy}", False)

	# p.add_node(ox,            oy)				# Corner 1
	p = create_teeth(outline, p, True, True, ox, oy, points)
	# p.add_node(ox + DICESIZE, oy)				# Corner 2
	p = create_teeth(outline, p, False, True, ox + DICESIZE, oy, points)
	# p.add_node(ox + DICESIZE, oy + DICESIZE)	# Corner 3
	p = create_teeth(outline, p, True, False, ox + DICESIZE, oy + DICESIZE, points)
	# p.add_node(ox,            oy + DICESIZE)	# Corner 4
	p = create_teeth(outline, p, False, False, ox, oy + DICESIZE, points)
	p.add_node(ox,            oy)				# Close to Corner 1

	outline.add_path(p)
	return outline

def front_back_side(ox: int, oy: int) -> Group:
	outline = Group(f"OutlineFrontBack{ox}{oy}")

	points = [
		(False, PINSIZE), 
		(False, PINSIZE), 
	] + [
		(True, 0),
		(True, PINSIZE, "A"),

		(False, 0),
		(False, PINSIZE), 
	] * 2

	p = Path(f"outlineA{ox}{oy}", False)

	# p.add_node(ox,            oy)				# Corner 1
	p = create_teeth(outline, p, True, True, ox, oy, points)
	# p.add_node(ox + DICESIZE, oy)				# Corner 2
	p = create_teeth(outline, p, False, True, ox + DICESIZE, oy, points)
	# p.add_node(ox + DICESIZE, oy + DICESIZE)	# Corner 3
	p = create_teeth(outline, p, True, False, ox + DICESIZE, oy + DICESIZE, points)
	# p.add_node(ox,            oy + DICESIZE)	# Corner 4
	p = create_teeth(outline, p, False, False, ox, oy + DICESIZE, points)

	outline.add_path(p)
	return outline


def top_bottom_side(ox: int, oy: int) -> Group:
	outline = Group(f"OutlineTopBottom{ox}{oy}")

	points = [
		(False, PINSIZE),
		(True, 0),
		(True, PINSIZE),
		(False, 0),

		(False, PINSIZE),
		(True, 0),
		(True, PINSIZE, "A"),
		(False, 0),

		(False, PINSIZE),
		(True, 0),
		(True, PINSIZE),
		(False, 0),
	]

	p = Path(f"outlineA{ox}{oy}", False)

	# p.add_node(ox,            oy)				# Corner 1
	p = create_teeth(outline, p, True, True, ox, oy, points)
	# p.add_node(ox + DICESIZE, oy)				# Corner 2
	p = create_teeth(outline, p, False, True, ox + DICESIZE, oy, points)
	# p.add_node(ox + DICESIZE, oy + DICESIZE)	# Corner 3
	p = create_teeth(outline, p, True, False, ox + DICESIZE, oy + DICESIZE, points)
	# p.add_node(ox,            oy + DICESIZE)	# Corner 4
	p = create_teeth(outline, p, False, False, ox, oy + DICESIZE, points)

	outline.add_path(p)
	return outline

def create_side(g: Group, x: int, y: int):
	side = Group(f"SIDE{x}{y}")

	ix = y * 3 + x + 1

	o_x = GUTTER + (x * GUTTER) + (x * DICESIZE)
	o_y = GUTTER + (y * GUTTER) + (y * DICESIZE)

	outline = None
	if ix == 1 or ix == 6:
		outline = top_bottom_side(o_x, o_y)
	elif ix == 2 or ix == 5:
		outline = left_right_side(o_x, o_y) 
	elif ix == 3 or ix == 4:
		outline = front_back_side(o_x, o_y) 

	for p in outline.paths:
		p.move((offset_x, offset_y))

	side.add_group(outline)

	if ix == 1 or ix == 3 or ix == 5:
		pos_x = o_x + DICESIZE / 2
		pos_y = o_y + DICESIZE / 2
		e = Ellipse(pos_x, pos_y, DOTRADIUS, RED)
		e.fillcolor = RED
		e.color = None
		e.move((offset_x, offset_y))
		side.add_ellipse(e)

	if ix == 2 or ix == 3 or ix == 5 or ix == 4 or ix == 6:
		pos_x = o_x + DICESIZE / 2 - (DOTRADIUS * 2)
		pos_y = o_y + DICESIZE / 2 - (DOTRADIUS * 2)
		if ix == 6:
			pos_x -= 1
		e = Ellipse(pos_x, pos_y, DOTRADIUS, RED)
		e.fillcolor = RED
		e.color = None
		e.move((offset_x, offset_y))
		side.add_ellipse(e)

		pos_x = o_x + DICESIZE / 2 + (DOTRADIUS * 2)
		pos_y = o_y + DICESIZE / 2 + (DOTRADIUS * 2)
		if ix == 6:
			pos_x += 1
		e = Ellipse(pos_x, pos_y, DOTRADIUS, RED)
		e.fillcolor = RED
		e.color = None
		e.move((offset_x, offset_y))
		side.add_ellipse(e)

	if ix == 4 or ix == 5 or ix == 6:
		pos_x = o_x + DICESIZE / 2 + (DOTRADIUS * 2)
		pos_y = o_y + DICESIZE / 2 - (DOTRADIUS * 2)
		if ix == 6:
			pos_x += 1
		e = Ellipse(pos_x, pos_y, DOTRADIUS, RED)
		e.fillcolor = RED
		e.color = None
		e.move((offset_x, offset_y))
		side.add_ellipse(e)

		pos_x = o_x + DICESIZE / 2 - (DOTRADIUS * 2)
		pos_y = o_y + DICESIZE / 2 + (DOTRADIUS * 2)
		if ix == 6:
			pos_x -= 1
		e = Ellipse(pos_x, pos_y, DOTRADIUS, RED)
		e.fillcolor = RED
		e.color = None
		e.move((offset_x, offset_y))
		side.add_ellipse(e)

	if ix == 6:
		pos_x = o_x + DICESIZE / 2
		pos_y = o_y + DICESIZE / 2 - (DOTRADIUS * 2)
		e = Ellipse(pos_x, pos_y, DOTRADIUS, RED)
		e.fillcolor = RED
		e.color = None
		e.move((offset_x, offset_y))
		side.add_ellipse(e)

		pos_x = o_x + DICESIZE / 2
		pos_y = o_y + DICESIZE / 2 + (DOTRADIUS * 2)
		e = Ellipse(pos_x, pos_y, DOTRADIUS, RED)
		e.fillcolor = RED
		e.color = None
		e.move((offset_x, offset_y))
		side.add_ellipse(e)

	if ix == 1 or ix == 4:
		for e in side.ellipses:
			e.color = None
			e.fillcolor = RED
	elif ix == 2 or ix == 5:
		for e in side.ellipses:
			e.color = None
			e.fillcolor = GREEN
	elif ix == 3 or ix == 6:
		for e in side.ellipses:
			e.color = None
			e.fillcolor = BLUE

	g.add_group(side)

def create_it():
	plate = Layer("Plate")

	dice = Group(f"dice")
	plate.groups.append(dice)

	p = create_rounded_box(0, 0, PLATESIZE_X, PLATESIZE_Y, 5, CYAN)
	p.move((offset_x, offset_y))

	plate.paths.append(p)

	for x, y in itertools.product(range(3), range(2)):
		create_side(dice, x, y)

	t = Text(offset_x + DICESIZE - 1, offset_y + PLATESIZE_Y - 1, MAGENTA, "Makerslab RSLopPOST")
	t.fontsize = 4
	t.color = MAGENTA
	t.fillcolor = None
	dice.add_text(t)


	save(plate, os.path.join(OUTPUT_FOLDER, "dice.svg"), "DICE", PAPER_WIDTH, PAPER_HEIGHT)


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
