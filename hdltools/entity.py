class Entity:

	def __init__(self, name):
		self.name = name
		self.generic = GenericList()
		self.port = PortList()

	def code(self, indent_level=0):

		hdl_code = indent(0) + ("entity %s is\n" % self.name)

		if (self.generic):
			hdl_code = hdl_code + indent(1) + ("generic (\n")
			hdl_code = hdl_code + self.generic.code(2)
			hdl_code = hdl_code + indent(1) + (");\n")

		else:
			hdl_code = hdl_code + indent(1) + ("--generic (\n")
			hdl_code = hdl_code + indent(2) + ("--generic_declaration_tag\n")
			hdl_code = hdl_code + indent(1) + ("--);\n")

		if (self.port):
			hdl_code = hdl_code + indent(1) + ("port (\n")
			hdl_code = hdl_code + self.port.code(2)
			hdl_code = hdl_code + indent(1) + (");\n")

		else:
			hdl_code = hdl_code + indent(1) + ("--port (\n")
			hdl_code = hdl_code + indent(2) + ("--port_declaration_tag\n")
			hdl_code = hdl_code + indent(1) + ("--);\n")
			hdl_code = hdl_code + indent(0) + ("end %s;\n" % self.name)
			hdl_code = hdl_code + "\n"

		return hdl_code
