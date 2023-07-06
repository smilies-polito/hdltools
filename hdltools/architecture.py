class Architecture:

	def __init__(self, name, entity_name):
		self.name = name
		self.entityName = entity_name
		self.signal = SignalList()
		self.constant = ConstantList()
		self.component = ComponentList()
		self.subPrograms = SubProgramList()
		self.customTypes = CustomTypeList()
		self.customTypesConstants = CustomTypeConstantList()
		self.declarationHeader = GenericCodeBlock()
		self.declarationFooter = GenericCodeBlock()
		self.bodyCodeHeader = GenericCodeBlock()
		self.instances = InstanceList()
		self.blocks = ""
		self.process = ""
		self.bodyCodeFooter = GenericCodeBlock()

	def code(self, indent_level=0):

		hdl_code = ""
		hdl_code = indent(0) + ("architecture %s of %s is\n" % (self.name, self.entityName))
		hdl_code = hdl_code + "\n"
		hdl_code = hdl_code + indent(1) + ("--architecture_declaration_tag\n")
		hdl_code = hdl_code + "\n"

		if (self.declarationHeader):
			hdl_code = hdl_code + self.declarationHeader.code(1)
			hdl_code = hdl_code + "\n"

		if (self.constant):
			hdl_code = hdl_code + self.constant.code()
			hdl_code = hdl_code + "\n"

		if (self.customTypes):
			hdl_code = hdl_code + self.customTypes.code()
			hdl_code = hdl_code + "\n"
			
		if (self.customTypesConstants):
			hdl_code = hdl_code + self.customTypesConstants.code()
			hdl_code = hdl_code + "\n"

		if (self.component):
			hdl_code = hdl_code + self.component.code()
			hdl_code = hdl_code + "\n"

		if (self.signal):
			hdl_code = hdl_code + self.signal.code()
			hdl_code = hdl_code + "\n"

		if (self.declarationFooter):
			hdl_code = hdl_code + self.declarationFooter.code(1)
			hdl_code = hdl_code + "\n"
			hdl_code = hdl_code + indent(0) + ("begin\n")
			hdl_code = hdl_code + "\n"
			hdl_code = hdl_code + indent(1) + ("--architecture_body_tag.\n")
			hdl_code = hdl_code + "\n"

		if (self.bodyCodeHeader):
			hdl_code = hdl_code + self.bodyCodeHeader.code(1)
			hdl_code = hdl_code + "\n"
			
		if (self.instances):
			hdl_code = hdl_code + self.instances.code()
			hdl_code = hdl_code + "\n"

		if (self.bodyCodeFooter):
			hdl_code = hdl_code + self.bodyCodeFooter.code(1)
			hdl_code = hdl_code + "\n"
			hdl_code = hdl_code + indent(0) + ("end %s;\n" % self.name)
			hdl_code = hdl_code + "\n"

		return hdl_code
