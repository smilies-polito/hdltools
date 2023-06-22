import vhdl_gen

adder = vhdl_gen.BasicVHDL("adder", "behavior")

adder.library.add("ieee")
adder.library["ieee"].package.add("std_logic_1164")
adder.library["ieee"].package.add("numeric_std")

adder.entity.generic.add("bit_width", "integer", "8")

adder.entity.port.add("in0", "in", "signed(bit_width-1 downto 0)")
adder.entity.port.add("in1", "in", "signed(bit_width-1 downto 0)")
adder.entity.port.add("add_out", "out", "signed(bit_width-1 downto 0)")


adder.architecture.bodyCodeHeader.add("add_out <= in0 + in1;")

adder.write_file()
