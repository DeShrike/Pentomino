###########################
# Definitions
###########################

# all lengths are in mm

PAPER_WIDTH = 600
PAPER_HEIGHT = 450

# Material Thickness
THICKNESS = 3.00

FACTOR = 1

DICESIZE = 21 * FACTOR  # should be multiple of THICKNESS and 7
GUTTER = 5              # spacing between sides
DOTRADIUS = 1.5

ATTACH_WIDTH = 1           # width of the attach line
TIGHTSIZE = 0.1

PINCOUNT = 3 * FACTOR
PINSIZE = (DICESIZE / 7) # / FACTOR
PINDEPTH = THICKNESS

PLATESIZE_X = (DICESIZE * 3) + (GUTTER * 4)
PLATESIZE_Y = (DICESIZE * 2) + (GUTTER * 3)

OUTPUT_FOLDER = "./out"
