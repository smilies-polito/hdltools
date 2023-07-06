class VHDLblock:
	def __init__(self, entity_name, architecture_name):
		self.fileHeader = GenericCodeBlock()
		self.fileHeader.add(license_text)
		self.library = LibraryList()
		self.work = PackageList()
		self.entity = Entity(entity_name)
		self.architecture = Architecture(architecture_name, entity_name)
		self.instance_name = self.entity.name+"_u"
		self.instance = InstanceObj(self.instance_name,self.entity)

	def dec_object(self):
		self.component = ComponentObj(self.entity.name)
		self.component.generic = self.entity.generic
		self.component.port = self.entity.port
		return self.component

	def declaration(self):
		return self.dec_object()

	def instanciation(self, inst_name = ""):
		self.instance = InstanceObj(self.instance_name,self.entity)
		instance = InstanceObj(self.instance_name,self.entity)
		if (inst_name):
		instance.instance_name = inst_name
		return instance

	def write_file(self):
		hdl_code = self.code()

		if (not os.path.exists("output")):
			os.makedirs("output")

			output_file_name = "output/"+self.entity.name+".vhd"
			# to do: check if file exists. If so, emit a warning and
			# check if must clear it.
			output_file = open(output_file_name, "w+")
		for line in hdl_code:
			output_file.write(line)

			output_file.close()
		return True

	def code(self, indent_level=0):
		hdl_code = ""
		hdl_code = hdl_code + self.fileHeader.code()
		hdl_code = hdl_code + self.library.code()
		hdl_code = hdl_code + self.work.code()
		hdl_code = hdl_code + self.entity.code()
