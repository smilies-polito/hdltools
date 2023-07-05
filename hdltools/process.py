class SensitivityList:

	def __init__(self, signal_list = []):
		self.signal_dict = {
			signal : SingleCodeLine(signal, line_end = ", ")
			for signal in signal_list
		}

	def add(self, signal):
		self.signal_dict[signal] = SingleCodeLine(signal, 
			line_end = ", ")

	def code(self, indent_level = 0):
		return VHDLenum(self.signal_dict, indent_level)



class Process:

	def __init__(self, name = "", sensitivity_list = []):
		self.name = name
		self.sensitivity_list = SignalList(sensitivity_list)
		self.body = GenericCodeBlock()
	
	def code(self, indent_level = 0):

		hdl_code = ""

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

		hdl_code = hdl_code + "begin\n\n"

		hdl_code = hdl_code + self.body.code()

		hdl_code = hdl_code + "\nend process " + self.name + ";\n\n"

		return hdl_code
