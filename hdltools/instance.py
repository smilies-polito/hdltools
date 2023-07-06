from dict_code import VHDLenum
from text import SingleCodeLine

class Instance():

	def __init__(self, component):
		self.name = component.name
		self.generic = component.generic
		self.port = component.port
		self.g_map = {}
		self.p_map = {}

	
	def generic_map(self, mode = "auto", mappings = None):

		if mode == "auto":

			index = 0
			
			for key in self.generic:

				self.g_map[index] = SingleCodeLine(self.generic[key].name + \
					" => " + self.generic[key].name + ",\n")
				index = index + 1

	def code(self, indent_level = 0):

		return VHDLenum(self.g_map, indent_level)
					




from component import ComponentObj

adder = ComponentObj("adder")
adder.generic.add("bit_width0", "integer", "8")
adder.generic.add("bit_width1", "integer", "8")
adder.generic.add("bit_width2", "integer", "8")

print(adder.code())


a = Instance(adder)
a.generic_map()

print(a.code(1))
