import vhdl_gen

class Adder(vhdl_gen.BasicVHDL):

	def __init__(self, entity_name, architecture_name, bit_width):
		vhdl_gen.BasicVHDL.__init__(self, entity_name, architecture_name)
		self.bit_width = bit_width

		self.library.add("ieee")
		self.library["ieee"].package.add("std_logic_1164")
		self.library["ieee"].package.add("numeric_std")

		self.entity.generic.add("bit_width", "integer", self.bit_width)

		self.entity.port.add("in0", "in", "signed(bit_width-1 downto 0)")
		self.entity.port.add("in1", "in", "signed(bit_width-1 downto 0)")
		self.entity.port.add("add_out", "out", "signed(bit_width-1 downto 0)")


		self.architecture.bodyCodeHeader.add("add_out <= in0 + in1;")

		self.write_file()

adder = Adder(
	entity_name 		= "adder",
	architecture_name 	= "behavior",
	bit_width		= 10
)
