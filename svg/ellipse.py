from . import constants
import uuid

class Ellipse():
	def __init__(self, x:float, y:float, r:float, color:str):
		self.x = x
		self.y = y
		self.rx = r
		self.ry = r
		self.color = color
		self.fillcolor = None
		self.id = "ellipse_" + str(uuid.uuid4())
		self.delta = (0, 0)

	def move(self, delta):
		self.delta = delta

	def write_to_file(self, fd):
		print(f"    Writing Ellipse: {self.id}")
		xml = constants.ELLIPSE_XML
		xml = xml.replace("{{ID}}", self.id)
		xml = xml.replace("{{X}}", str(self.x + self.delta[0]))
		xml = xml.replace("{{Y}}", str(self.y + self.delta[1]))
		xml = xml.replace("{{RX}}", str(self.rx))
		xml = xml.replace("{{RY}}", str(self.ry))
		xml = xml.replace("{{COLOR}}", self.color if self.color else constants.WHITE)
		xml = xml.replace("{{FILLCOLOR}}", self.fillcolor if self.fillcolor else constants.WHITE)
		xml = xml.replace("{{COLORCLASS}}", constants.to_color_class(self.color, self.fillcolor))
		fd.write(xml)
