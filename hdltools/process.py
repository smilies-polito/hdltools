from text import SingleCodeLine, GenericCodeBlock
from dict_code import VHDLenum, DictCode
from format_text import indent
from if_statement import IfList
from for_statement import ForList
from case_statement import CaseList

class SensitivityList(dict):

	def __init__(self, *args):

		self.index = 0
		
		for signal in args:
			self[self.index] = SingleCodeLine(signal, 
					line_end = ", ")
			
			self.index = self.index + 1

	def add(self, signal):
		self[self.index] = SingleCodeLine(signal, 
			line_end = ", ")

		self.index = self.index + 1

	def code(self, indent_level = 0):
		return VHDLenum(self, indent_level)


class Process:

	def __init__(self, name = "", *args):
		self.name = name
		self.sensitivity_list = SensitivityList(*args)
		self.body = GenericCodeBlock()
		self.if_list = IfList()
		self.for_list = ForList()
		self.case_list = CaseList()
	
	def code(self, indent_level = 0):

		hdl_code = ""

		if self.body or self.if_list or self.for_list or self.case_list:
			if(self.name == ""):
				hdl_code = hdl_code + indent(indent_level) + \
						"process(" + \
						self.sensitivity_list.code() + \
						")\n"

			else:
				hdl_code = hdl_code + indent(indent_level) + \
						self.name + " : process(" + \
						self.sensitivity_list.code() + \
						")\n"

			hdl_code = hdl_code + indent(indent_level) + "begin\n\n"

			hdl_code = hdl_code + self.if_list.code(indent_level \
						+ 1)
			hdl_code = hdl_code + self.for_list.code(indent_level \
						+ 1)
			hdl_code = hdl_code + self.case_list.code(indent_level \
						+ 1)
			hdl_code = hdl_code + self.body.code(indent_level + 1)

			hdl_code = hdl_code + indent(indent_level) + \
					"end process " + self.name + ";\n\n"

		return hdl_code

class ProcessList(dict):

	def add(self, name : str = "", *args):
		self[name] = Process(name, *args)

	def code(self, indent_level : int = 0):
		return DictCode(self, indent_level)
