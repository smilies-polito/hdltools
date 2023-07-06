from format_text import indent
from dict_code import VHDLenum

class GenericMapObj:

	def __init__(self, port, signal):
		self.port = port
		self.signal = signal

	def code(self, indent_level = 0):
		return self.port + " => " + self.signal + ",\n"

class GenericMapList(dict):

	def __init__(self, generic_list, mode = "auto", *args, **kwargs):

		if mode == "auto":
		
			index = 0

			for key in generic_list:

				name = generic_list[key].name

				self[index] = GenericMapObj(name, name)
				index = index + 1
			

	def code(self, indent_level = 0):
		return VHDLenum(self, indent_level)
