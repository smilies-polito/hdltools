from format_text import indent
from dict_code import VHDLenum

class MapObj:

	def __init__(self, port, signal, conn_range = ""):
		self.port = port
		self.signal = signal
		self.conn_range = conn_range

	def code(self, indent_level = 0):
		return self.port + self.conn_range + " => " + \
			self.signal + ",\n"

class MapList(dict):

	def __init__(self, elements_list, mode = "auto", *args, **kwargs):

		self.elements_list = elements_list

		if mode == "auto":
		
			for key in self.elements_list:

				name = self.elements_list[key].name

				self[name] = MapObj(name, name)

		elif mode == "pos":

			if len(args) != len(self.elements_list):
				print("Error, wrong number of elements in"
						" signals mapping\n")
				exit(-1)

			else:

				for source, target in zip(args, self.elements_list):

					if type(source) == str:
						source_name = source

					elif hasattr(source, "name"):
						source_name = source.name

					else:
						print("Error, wrong source in"
							" signal mapping\n")

					target_name = self.elements_list[target].name

					self[target_name] = MapObj(target_name,
							source_name)

		elif mode == "key":

			if len(kwargs) != len(self.elements_list):
				print("Error, wrong number of elements in"
						" signals mapping\n")
				exit(-1)

			
			for target in self.elements_list:

				if self.elements_list[target].name in kwargs:

					if type(kwargs[target]) == str:
						source_name = kwargs[target]

					elif hasattr(kwargs[target], "name"):
						source_name = \
							kwargs[target].name

					else:
						print("Error, wrong source in"
							" signal mapping\n")

					target_name = self.elements_list[target].name

					self[target_name] = MapObj(target_name,
							source_name)

				else:
					print("Error, signal not mapped\n")
					exit(-1)


		elif mode == "no":
			pass

		else:
			print("Wrong instance mode\n")
			exit(-1)


	def add(self, target_name, source, conn_range = ""):

		present = False

		for target in self.elements_list:
			if target_name == self.elements_list[target].name:
				present = True

		if present:

			if conn_range and target_name in self:
				print(self.code())
				del self[target_name]

			if type(source) == str:
				self[target_name + conn_range] = \
					MapObj(target_name, source, conn_range)

			elif hasattr(source, "name"):
				self[target_name + conn_range] = \
					MapObj(target_name, source.name,
					conn_range)

			else:
				print("Error, wrong source in signal mapping\n")
				exit(-1)


		else:
			print("Signal not present in component\n")





	def code(self, indent_level = 0):
		return VHDLenum(self, indent_level)

