from constant import ConstantList
from component import ComponentList
from text import GenericCodeBlock
from process import ProcessList
from instance import InstanceList
from signals import SignalList
from format_text import indent

class Architecture:

	def __init__(self, name, entity_name):
		self.name = name
		self.entityName = entity_name
		self.signal = SignalList()
		self.constant = ConstantList()
		self.component = ComponentList()
		self.declarationHeader = GenericCodeBlock()
		self.declarationFooter = GenericCodeBlock()
		self.bodyCodeHeader = GenericCodeBlock()
		self.processes = ProcessList()
		self.instances = InstanceList()
		self.bodyCodeFooter = GenericCodeBlock()

	def code(self, indent_level=0):

		hdl_code = ""
		hdl_code = indent(0) + ("architecture %s of %s is\n" % (self.name, self.entityName))
		hdl_code = hdl_code + "\n"
		hdl_code = hdl_code + "\n"

		if (self.declarationHeader):
			hdl_code = hdl_code + self.declarationHeader.code(1)
			hdl_code = hdl_code + "\n"

		if (self.constant):
			hdl_code = hdl_code + self.constant.code()
			hdl_code = hdl_code + "\n"

		if (self.component):
			hdl_code = hdl_code + self.component.code()
			hdl_code = hdl_code + "\n"

		if (self.signal):
			hdl_code = hdl_code + self.signal.code()
			hdl_code = hdl_code + "\n"


		hdl_code = hdl_code + indent(0) + ("begin\n\n")

		if (self.declarationFooter):
			hdl_code = hdl_code + self.declarationFooter.code(1)
			hdl_code = hdl_code + "\n"
			hdl_code = hdl_code + "\n"
			hdl_code = hdl_code + "\n"

		if (self.bodyCodeHeader):
			hdl_code = hdl_code + self.bodyCodeHeader.code(1)
			hdl_code = hdl_code + "\n"
			
		if self.processes:
			hdl_code = hdl_code + self.processes.code(indent_level +
					1)
			hdl_code = hdl_code + "\n"

		if (self.instances):
			hdl_code = hdl_code + self.instances.code()
			hdl_code = hdl_code + "\n"

		if (self.bodyCodeFooter):
			hdl_code = hdl_code + self.bodyCodeFooter.code(1)
			hdl_code = hdl_code + "\n"

		hdl_code = hdl_code + indent(0) + ("end architecture %s;\n" % self.name)
		hdl_code = hdl_code + "\n"

		return hdl_code
