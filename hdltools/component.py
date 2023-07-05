from generic import GenericList
from port import PortList
from format_text import indent
from dict_code import DictCode

class ComponentObj:

	"""
	VHDL component definition.

	Methods:
	--------
	code(indent_level = 0)	: generate the string to declare the component

	"""


	def __init__(self, name : str):

		"""
		Parameters:
		-----------
		name		: str
			Name of the component
		"""

		self.name = name
		self.generic = GenericList()
		self.port = PortList()


	def code(self, indent_level : int = 0):

		"""
		Generate the string to declare the component

		Parameters:
		----------
		indent_level	: int
			Level of indentation to insert before the string
		"""


		hdl_code = ""
		hdl_code = hdl_code + indent(indent_level) + \
				("component %s is\n" % self.name)

		if (self.generic):
			hdl_code = hdl_code + \
					indent(indent_level+1) + \
					("generic (\n")
			hdl_code = hdl_code + \
					self.generic.code(indent_level + 2)
			hdl_code = hdl_code + \
					indent(indent_level+1) + (");\n")
		else:
			hdl_code = hdl_code + \
					indent(indent_level+1) + \
					("--generic (\n")
			hdl_code = hdl_code + \
					indent(indent_level+2) + \
					("--generic_declaration_tag\n")
			hdl_code = hdl_code + \
					indent(indent_level+1) + ("--);\n")
		if (self.port):
			hdl_code = hdl_code + \
					indent(indent_level+1) + ("port (\n")
			hdl_code = hdl_code + \
					self.port.code(indent_level+2)
			hdl_code = hdl_code + \
					indent(indent_level+1) + (");\n")
		else:
			hdl_code = hdl_code + \
					indent(indent_level+1) + ("--port (\n")
			hdl_code = hdl_code + \
					indent(indent_level+2) + \
					("--port_declaration_tag\n")
			hdl_code = hdl_code + \
					indent(indent_level+1) + ("--);\n")

		hdl_code = hdl_code + \
				indent(indent_level) + \
				("end component;\n")
		hdl_code = hdl_code + "\n"

		return hdl_code



class ComponentList(dict):

	"""
	Dictionary of VHDL components.

	Methods:
	--------
	add(name)		: add a port object to the dictionary
	code(indent_level = 0)	: generate the string to declare all the ports
	"""

	def add(self, name : str):
		"""
		Add a component object to the dictionary.

		Parameters:
		-----------
		name		: str
			Name of the port
		"""

		self[name] = ComponentObj(name)

	def code(self, indent_level : int = 0):

		"""
		Generate the string to declare all the components

		Parameters:
		----------
		indent_level	: int
			Level of indentation to insert before the string
		"""

		return DictCode(self, indent_level)


a = ComponentList()

a.add("adder")

a["adder"].generic.add("N", "integer", "8")

a["adder"].port.add("in0", "in", "std_logic_vector(N downto 0)")
a["adder"].port.add("in1", "in", "std_logic_vector(N downto 0)")

a["adder"].port.add("add_out", "out", "std_logic_vector(N downto 0)")

a.add("subtractor")

a["subtractor"].generic.add("N", "integer", "8")

a["subtractor"].port.add("in0", "in", "std_logic_vector(N downto 0)")
a["subtractor"].port.add("in1", "in", "std_logic_vector(N downto 0)")

a["subtractor"].port.add("add_out", "out", "std_logic_vector(N downto 0)")


print(a.code())
