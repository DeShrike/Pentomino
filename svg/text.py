from . import constants
import uuid

class Text():
	def __init__(self, x:int, y:int, color:str, text:str):
		self.x = x
		self.y = y
		self.text = text
		self.color = color
		self.fillcolor = None
		self.fontsize = 6
		self.id = "text_" + str(uuid.uuid4())
		self.rotation_degrees = 0

	def write_to_file(self, fd):
		# print(f"Writing: {self.id}")
		xml = constants.TEXT_XML
		xml = xml.replace("{{ID}}", self.id)
		xml = xml.replace("{{X}}", str(self.x))
		xml = xml.replace("{{Y}}", str(self.y))
		xml = xml.replace("{{TEXT}}", self.text)
		xml = xml.replace("{{COLOR}}", self.color if self.color else constants.WHITE)
		xml = xml.replace("{{FILLCOLOR}}", self.fillcolor if self.fillcolor else constants.WHITE)
		xml = xml.replace("{{FONTSIZE}}", str(self.fontsize))
		xml = xml.replace("{{COLORCLASS}}", constants.to_color_class(self.color, self.fillcolor))
		transform = ""
		if self.rotation_degrees != 0:
			transform = f"transform=\"rotate({self.rotation_degrees})\""
		xml = xml.replace("{{TRANSFORM}}", transform)

		fd.write(xml)
