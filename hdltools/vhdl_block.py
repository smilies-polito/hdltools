from text import GenericCodeBlock
from library_vhdl import LibraryList, PackageList
from entity import Entity
from architecture import Architecture
from instance import Instance
from license_text import LicenseText

import os

class VHDLblock:
	def __init__(self, entity_name, architecture_name = "behavior"):
		self.fileHeader = GenericCodeBlock()
		self.fileHeader.add(LicenseText)
		self.library = LibraryList()
		self.work = PackageList()
		self.entity = Entity(entity_name)
		self.architecture = Architecture(architecture_name, entity_name)

	def dec_object(self):
		self.component = ComponentObj(self.entity.name)
		self.component.generic = self.entity.generic
		self.component.port = self.entity.port
		return self.component

	def declaration(self):
		return self.dec_object()

	def write_file(self, output_dir = "output"):
		hdl_code = self.code()

		if (not os.path.exists(output_dir)):
			os.makedirs(output_dir)

		output_file_name = output_dir + "/" + self.entity.name+".vhd"

		with open(output_file_name, "w+") as fp:

			for line in hdl_code:
				fp.write(line)

		return True

	def code(self, indent_level=0):
		hdl_code = ""
		hdl_code = hdl_code + self.fileHeader.code()
		hdl_code = hdl_code + self.library.code()
		hdl_code = hdl_code + self.work.code()
		hdl_code = hdl_code + self.entity.code()
		hdl_code = hdl_code + self.architecture.code()

		return hdl_code
