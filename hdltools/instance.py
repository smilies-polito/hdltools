from format_text import indent
from dict_code import VHDLenum
from text import SingleCodeLine

from map_signals import MapList

class Instance():

	def __init__(self, component, instance_name):
		self.instance_name = instance_name
		self.name = component.name
		self.generic_list = component.generic
		self.port_list = component.port
		self.g_map = {}
		self.p_map = {}

	
	def generic_map(self, mode = "auto", *args, **kwargs):
		self.g_map = MapList(self.generic_list, mode, *args, **kwargs)

	def port_map(self, mode = "auto", *args, **kwargs):
		self.p_map = MapList(self.port_list, mode, *args, **kwargs)

	def code(self, indent_level = 0):

		hdl_code = ""

		if self.p_map:

			hdl_code = indent(indent_level) + self.instance_name + \
					" : " + self.name + "\n"

			if self.g_map:
				hdl_code = hdl_code + \
					indent(indent_level + 1) + \
					"generic map(\n"

				hdl_code = hdl_code + \
					self.g_map.code(indent_level + 2)

				hdl_code = hdl_code + indent(indent_level + 1) \
						+ ")\n"

			hdl_code = hdl_code + indent(indent_level + 1) + \
					"port map(\n"


			hdl_code = hdl_code + self.p_map.code(indent_level + 2)

			hdl_code = hdl_code + indent(indent_level + 1) + \
					");\n\n"


		return hdl_code
					




from component import ComponentObj

adder = ComponentObj("adder")
adder.generic.add("bit_width0", "integer", "8")
adder.generic.add("bit_width1", "integer", "8")
adder.generic.add("bit_width2", "integer", "8")

adder.port.add("in0", "in", "st_logic")
adder.port.add("in1", "in", "st_logic")

print(adder.code())


a = Instance(adder, "adder_0")
a.generic_map()
a.port_map()

print(a.code())
