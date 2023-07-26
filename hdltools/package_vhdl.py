from custom_types import CustomTypeList
import os

class PackageDeclaration():

	def __init__(self, name):
		self.name = name
		self.type_list = CustomTypeList()

	def code(self, indent_level = 0):

		hdl_code = ""

		hdl_code += "package " + self.name + " is\n\n"

		if self.type_list:
			hdl_code += self.type_list.code(indent_level + 1)

		hdl_code += "end package " + self.name + ";\n"

		return hdl_code

class Package():

	def __init__(self, name):
		self.name = name
		self.pkg_dec = PackageDeclaration(name)

	def code(self, indent_level = 0):

		hdl_code = ""

		hdl_code += self.pkg_dec.code(indent_level)

		return hdl_code

	def write_file(self, output_dir = "output"):

		hdl_code = self.code()

		if (not os.path.exists(output_dir)):
			os.makedirs(output_dir)

		output_file_name = output_dir + "/" + self.name+".vhd"

		with open(output_file_name, "w+") as fp:

			for line in hdl_code:
				fp.write(line)

		return True
