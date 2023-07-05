#################################################################################
# Copyright 2020 Ricardo F Tafas Jr

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#################################################################################
# Contributor list:
# 2020 - Ricardo F Tafas Jr - https://github.com/rftafas
# 2020 - T.P. Correa - https://github.com/tpcorrea

import sys
import os
import copy

# TODO:
# Process
# Procedures
# Block
# Protected Types

# ------------------- Custom Types -----------------------


class IncompleteTypeObj:
    def __init__(self, name):
        self.name = name

    def code(self):
        hdl_code = ""
        hdl_code = "type %s;\n" % self.name
        hdl_code = hdl_code + "\n"
        return hdl_code


class EnumerationTypeObj:
    def __init__(self, name, *args):
        self.name = name
        self.type = type
        self.typeElement = dict()
        self.newLine = False
        self.endLine = ", "

        if args:
            self.add(args[0])

    def SetNewLine(self, input):
        pass
        if input:
            self.newLine = True
            self.endLine = ",\n"
        else:
            self.newLine = False
            self.endLine = ", "
        for element in self.typeElement:
            self.typeElement[element].line_end = self.endLine

    def add(self, input):
        if isinstance(input, str):
            self.typeElement[input] = SingleCodeLine(input, self.endLine)
        else:
            for element in input:
                self.typeElement[element] = SingleCodeLine(element, self.endLine)

    def code(self, indent_level=1):
        hdl_code = ""
        if self.typeElement:
            hdl_code =  hdl_code + indent(indent_level) + "type %s is ( " % self.name
            if self.newLine:
                hdl_code = hdl_code + "\n"
                hdl_code = hdl_code + "%s" % VHDLenum(self.typeElement, indent_level+1)
                hdl_code = hdl_code + indent(indent_level)
            else:
                hdl_code = hdl_code + "%s" % VHDLenum(self.typeElement)
            hdl_code = hdl_code + ");\n"
            hdl_code = hdl_code + "\n"
        return hdl_code


class ArrayTypeObj:
    def __init__(self, name, *args):
        self.name = name
        self.arrayRange = args[0]
        self.arrayType = args[1]

    def code(self):
        hdl_code = ""
        hdl_code = indent(1) + "type %s is array (%s) of %s;\n" % (self.name, self.arrayRange, self.arrayType)
        hdl_code = hdl_code + "\n"
        return hdl_code


class RecordTypeObj:
    def __init__(self, name, *args):
        self.name = name

        if args:
            if isinstance(args[0], GenericList):
                self.element = args[0]
        else:
            self.element = GenericList()

    def add(self, name, type, init=None):
        self.element.add(name, type, init)

    def code(self):
        hdl_code = GenericCodeBlock()
        hdl_code.add("type %s is record" % self.name)
        for j in self.element:
            hdl_code.add(indent(1) + "%s : %s;" % (self.element[j].name, self.element[j].type) )
        hdl_code.add( "end record %s;" % self.name )
        return hdl_code.code()

class SubTypeObj:
    def __init__(self, name, *args):
        self.name = name
        self.ofType = args[0]
        self.element = GenericList()

    def add(self, name, type, init=None):
        self.element.add(name, type, init)

    def code(self):
        hdl_code = ""
        hdl_code = hdl_code + indent(1) + "subtype %s is %s (\n" % (self.name, self.ofType)
        i = 0
        for j in self.element:
            i += 1
            if (i == len(self.element)):
                hdl_code = hdl_code + indent(2) + "%s (%s)); \n" % (self.element[j].name, self.element[j].type)
            else:
                hdl_code = hdl_code + indent(2) + "%s (%s),\n" % (self.element[j].name, self.element[j].type)
        hdl_code = hdl_code + "\n"
        return hdl_code


class CustomTypeList(dict):
    def add(self, name, type, *args):
        if "Array" in type:
            self[name] = ArrayTypeObj(name, *args)
        elif "Enumeration" in type:
            self[name] = EnumerationTypeObj(name, *args)
        elif "Record" in type:
            self[name] = RecordTypeObj(name, *args)
        elif "SubType" in type:
            self[name] = SubTypeObj(name, *args)
        else:
            self[name] = IncompleteTypeObj(name)

    def code(self, indent_level=0):
        return DictCode(self)


# ------------------- Custom Type Constant List -----------------------


class RecordConstantObj(RecordTypeObj):
    def __init__(self, name, record):
        self.name = name
        if isinstance(record,RecordTypeObj):
            self.element = record.element
            self.recordName  = record.name
        else:
            print("Error: object must be of record type.")

    def code(self):
        hdl_code = ""
        hdl_code = hdl_code + "constant %s : %s := (\n" % (self.name, self.recordName)
        i = 0
        for j in self.element:
            i += 1
            if self.element[j].init is None:
                init = "'0'"
            else:
                init = self.element[j].init
            if (i == len(self.element)):
                hdl_code = hdl_code + indent(1) + "%s => %s\n" % (self.element[j].name, init)
            else:
                hdl_code = hdl_code + indent(1) + "%s => %s,\n" % (self.element[j].name, init)
        hdl_code = hdl_code + ");\n"
        hdl_code = hdl_code + "\n"
        return hdl_code

class CustomTypeConstantList(dict):
    def add(self, name, type, value):
        if isinstance(type,RecordTypeObj):
            self[name] = RecordConstantObj(name,type)
        else:
            self[name] = GenericObj(name,type,value)

    def code(self, indent_level=0):
        return DictCode(self)


# ------------------- Signals -----------------------


class SignalObj:
    def __init__(self, name, type, *args):
        self.name = name
        self.type = type
        if args:
            self.value = args[0]
        else:
            self.value = ""

    def code(self, indent_level=0):
        if self.value:
            return indent(indent_level + 1) + ("signal %s : %s := %s;\n" % (self.name, self.type, self.value))
        else:
            return indent(indent_level + 1) + ("signal %s : %s;\n" % (self.name, self.type))


class SignalList(dict):
    def add(self, name, type, *args):
        self[name] = SignalObj(name, type, *args)

    def code(self, indent_level=0):
        return DictCode(self)


# ------------------- Variables -----------------------


class VariableObj:
    def __init__(self, name, type, *args):
        self.name = name
        self.type = type
        if args:
            self.init = args[0]
        else:
            self.init = "undefined"

    def code(self, indent_level=0):
        if self.init != "undefined":
            return indent(1) + ("variable %s : %s := %s;\n" % (self.name, self.type, self.init))
        else:
            return indent(1) + ("variable %s : %s;\n" % (self.name, self.type))


class VariableList(dict):
    def add(self, name, type, *args):
        self[name] = VariableObj(name, type, *args)

    def code(self, indent_level=0):
        return DictCode(self)


# ------------------- Functions & Procedures -----------------------


class FunctionObj:
    def __init__(self, name):
        self.name = name
        # todo: generic types here.
        self.customTypes = CustomTypeList()
        self.generic = GenericList()
        # function parameters in VHDL follow the same fashion as
        # generics on a portmap. name : type := init value;
        self.parameter = GenericList()
        self.variable = VariableList()
        self.functionBody = GenericCodeBlock()
        self.returnType = "return_type_here"
        self.genericInstance = InstanceObjList()

    def new(self, newName):
        hdl_code = "function %s is new %s\n" % (newName, self.name)
        hdl_code = hdl_code + indent(1)+"generic (\n"
        # todo: generic types here.
        if not self.genericInstance:
            for item in self.genericInstance:
                self.genericInstance.add(item, "<new value>")
        hdl_code = hdl_code + self.genericInstance.code()
        hdl_code = hdl_code + indent(1)+");\n"

    def declaration(self):
        hdl_code = self._code()
        hdl_code = hdl_code + indent(0) + ("return %s;\n" % self.returnType)
        return hdl_code

    def _code(self):
        hdl_code = indent(0) + ("function %s" % self.name)
        if (self.generic | self.customTypes):
            hdl_code = hdl_code + ("\n")
            hdl_code = hdl_code + indent(1) + ("generic (\n")
            if (self.customTypes):
                hdl_code = hdl_code + self.customTypes.code()
            if (self.generic):
                hdl_code = hdl_code + self.generic.code()
            hdl_code = hdl_code + indent(1) + (")\n")
            hdl_code = hdl_code + indent(1) + ("parameter")
        if (self.parameter):
            hdl_code = hdl_code + indent(1) + (" (\n")
            hdl_code = hdl_code + self.parameter.code()
            hdl_code = hdl_code + indent(1) + (")\n")
        return hdl_code

    def code(self):
        hdl_code = self._code()
        hdl_code = hdl_code + indent(0) + ("return %s is\n")
        hdl_code = hdl_code + self.variable.code()
        hdl_code = hdl_code + indent(0) + ("begin\n")
        hdl_code = hdl_code + self.functionBody.code(1)
        hdl_code = hdl_code + indent(0) + ("end %s;\n" % self.name)
        return hdl_code


class ProcedureObj:
    def __init__(self, name):
        self.name = name

    def new(self):
        hdl_code = "--Not implemented."
        return hdl_code

    def declaration(self):
        hdl_code = "--Procedure Declaration not Implemented."
        return hdl_code

    def code(self):
        hdl_code = "--Procedure Code not Implemented."
        return hdl_code


class SubProgramList(dict):
    def add(self, name, type):
        if type == "Function":
            self[name] = FunctionObj(name)
        elif type == "Procedure":
            self[name] = ProcedureObj(name)
        else:
            print("Error. Select \"Function\" or \"Procedure\". Keep the quotes.")

    def declaration(self, indent_level=0):
        hdl_code = ""
        for j in self:
            hdl_code = hdl_code + self[j].declaration()
        return hdl_code

    def code(self, indent_level=0):
        hdl_code = ""
        for j in self:
            hdl_code = hdl_code + self[j].code()
        return hdl_code

# ------------------- Component -----------------------


class ComponentObj:
    def __init__(self, name):
        self.name = name
        self.generic = GenericList()
        self.port = PortList()
        self.filename = ""

    def code(self, indent_level=0):
        hdl_code = ""
        hdl_code = hdl_code + indent(1) + ("component %s is\n" % self.name)
        if (self.generic):
            hdl_code = hdl_code + indent(2) + ("generic (\n")
            hdl_code = hdl_code + self.generic.code(3)
            hdl_code = hdl_code + indent(2) + (");\n")
        else:
            hdl_code = hdl_code + indent(2) + ("--generic (\n")
            hdl_code = hdl_code + indent(3) + ("--generic_declaration_tag\n")
            hdl_code = hdl_code + indent(2) + ("--);\n")
        if (self.port):
            hdl_code = hdl_code + indent(2) + ("port (\n")
            hdl_code = hdl_code + self.port.code(3)
            hdl_code = hdl_code + indent(2) + (");\n")
        else:
            hdl_code = hdl_code + indent(2) + ("--port (\n")
            hdl_code = hdl_code + indent(3) + ("--port_declaration_tag\n")
            hdl_code = hdl_code + indent(2) + ("--);\n")
        hdl_code = hdl_code + indent(1) + ("end component;\n")
        hdl_code = hdl_code + "\n"
        return hdl_code


class ComponentList(dict):
    def add(self, name):
        self[name] = ComponentObj(name)

    def append(self, component_obj):
        if isinstance(component_obj, ComponentObj):
            self[component_obj.name] = component_obj

    def code(self, indent_level=0):
        return DictCode(self)

# ------------------- Instance -----------------------
class InstanceObj:
    class _GenericObj(GenericObj):
        def assign(self,assign_value):
            self.assign_value = assign_value

    class _PortObj(PortObj):
        def assign(self,assign_value):
            self.assign_value = assign_value

    class _PortList(PortList):
        def add(self, name, direction, type, value=None):
            self[name] = InstanceObj._PortObj(name, direction, type, value)
        def _listcopy(self, port):
            for port_name in port:
                _element = port[port_name]
                self.add(_element.name, _element.direction, _element.type, _element.value)

    class _GenericList(GenericList):
        def add(self, name, type, value):
            self[name] = InstanceObj._GenericObj(name, type, value)
        def _listcopy(self, generic):
            for generic_name in generic:
                _element = generic[generic_name]
                self.add(_element.name, _element.type, _element.value)

    def __init__(self, inst_name, comp_name):
        self.instance_name = inst_name
        self.component_name = comp_name
        self.port = self._PortList()
        self.generic = self._GenericList()

        if isinstance(comp_name, BasicVHDL):
            self.component_name = comp_name.entity.name
            self.generic._listcopy(comp_name.entity.generic)
            self.port._listcopy(comp_name.entity.port)

        elif isinstance(comp_name, Entity):
            self.component_name = comp_name.name
            self.generic._listcopy(comp_name.generic)
            self.port._listcopy(comp_name.port)

        elif isinstance(comp_name, ComponentObj):
            self.component_name = comp_name.name
            self.generic._listcopy(comp_name.generic)
            self.port._listcopy(comp_name.port)

    def code(self, indent_level=2):
        assign_gen_code = GenericCodeBlock()
        assign_port_code = GenericCodeBlock()
        hdl_code = indent(indent_level) + ("%s : %s\n" % (self.instance_name, self.component_name) )
        if (self.generic):
            hdl_code = hdl_code + indent(indent_level+1) + ("generic map (\n")
            for j in self.generic:
                assign_gen_code.add(indent(indent_level+2) + j + " => " + self.generic[j].assign_value,",\n")
            hdl_code = hdl_code + VHDLenum(assign_gen_code)

        if (self.port):
            hdl_code = hdl_code + indent(indent_level+1) + (")\n")
            hdl_code = hdl_code + indent(indent_level+1) + ("port map (\n")
            for j in self.port:
                assign_port_code.add(indent(indent_level+2) + j + " => " + self.port[j].assign_value,",\n")
            hdl_code = hdl_code + VHDLenum(assign_port_code)
        hdl_code = hdl_code + indent(2) + (");\n")
        hdl_code = hdl_code + "\n"
        return hdl_code

class InstanceList(dict):
    def add(self, instance_name, component_name):
        self[instance_name] = InstanceObj(instance_name,component_name)

    def append(self, input):
        if isinstance(input,InstanceObj):
            self[input.instance_name] = input

    def code(self, indent_level=0):
        return DictCode(self)


# ------------------- If statement -----------------------

class Condition:
	
	def __init__(self, condition, _type_ = None):
		self.condition = condition
		self._type_ = _type_

	def code(self):

		if self._type_ == None:
			hdl_code = self.condition

		elif self._type_ == "and":
			hdl_code = "and " + self.condition

		elif self._type_ == "or":
			hdl_code = "or " + self.condition

		else:
			print("Types of if condition not supported. Supported "
					"types are \"and\" and \"or\"\n")
			exit(-1)


		return hdl_code

class ConditionsList(list):
	def add(self, condition, _type_ = None):
		self.append(Condition(condition, _type_))

	def code(self):

		hdl_code = ""

		for condition in self:
			hdl_code = hdl_code + " " + condition.code()

		return hdl_code


class If_block:
	def __init__(self):
		self.conditions = ConditionsList()
		self.body = GenericCodeBlock()


	def code(self, indent_level = 0):

		hdl_code = ""

		hdl_code = hdl_code + indent(indent_level) + "if(" + self.conditions.code() + ")\n"
		hdl_code = hdl_code + indent(indent_level) + "then\n\n"
		hdl_code = hdl_code + indent(indent_level) + indent(1) + self.body.code()
		hdl_code = hdl_code + "\n"

		return hdl_code


class Elsif_block:
	def __init__(self):
		self.conditions = ConditionsList()
		self.body = GenericCodeBlock()


	def code(self, indent_level = 0):

		hdl_code = ""

		hdl_code = hdl_code + indent(indent_level) + "elsif(" + self.conditions.code() + ")\n"
		hdl_code = hdl_code + indent(indent_level) + "then\n\n"
		hdl_code = hdl_code + indent(indent_level) + indent(1) + self.body.code()
		hdl_code = hdl_code + "\n"

		return hdl_code


class Else_block:
	def __init__(self):
		self.body = GenericCodeBlock()


	def code(self, indent_level = 0):

		hdl_code = ""

		hdl_code = hdl_code + indent(indent_level) + "else\n"
		hdl_code = hdl_code + indent(indent_level) + indent(1) + self.body.code()
		hdl_code = hdl_code + "\n"

		return hdl_code

class Else_list(dict):
	def __init__(self):
		self.index = 0

	def add(self):
		self[self.index] = Else_block()
		self.index = self.index + 1

	def code(self, indent_level = 0):
		return DictCode(self, indent_level)

a = Else_list()
a.add()
a[0].body.add("a <= '1';\n")

print(a.code())

class If(GenericCodeBlock):

	def code(self, indent_level = 0):

		hdl_code = ""

		hdl_code = hdl_code + indent(indent_level) + self._if_.code()
		hdl_code = hdl_code + indent(indent_level) + self._elsif_.code()
		hdl_code = hdl_code + indent(indent_level) + self._else_.code()

		hdl_code = hdl_code + "end if;\n"

		return hdl_code

# ------------------- For loop -----------------------

class For:
	def __init__(self, name = "", start = 0, stop = 1, iter_name = "i",
			direction = "up"):
		self.name = name
		self.start = start
		self.stop = stop
		self.iter_name = iter_name
		self.direction = direction
		self.body = GenericCodeBlock()

	def code(self, indent_level = 0):

		hdl_code = ""


		if(self.name == ""):
			hdl_code = hdl_code + indent(indent_level) + "for(" + \
					self.iter_name + " in "

		else:
			hdl_code = hdl_code + indent(indent_level) + \
					self.name + " : for(" + \
					self.iter_name + " in "

		if(self.direction == "down"):
			hdl_code = hdl_code + str(self.start) + " downto " + \
					str(self.stop) + ")\n"

		else:
			hdl_code = hdl_code + str(self.start) + " to " + \
					str(self.stop) + ")\n"

		

		hdl_code = hdl_code + indent(indent_level) + "loop\n" 

		hdl_code = hdl_code + indent(indent_level + 1) + \
				self.body.code() + "\n"

		hdl_code = hdl_code + indent(indent_level) + "end loop " + \
				self.name + ";\n"

		return hdl_code

# ------------------- Process -----------------------
class SignalList:

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

# ------------------- Entity -----------------------


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

# ------------------- Architecture -----------------------


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
        # blocks will come here.
        # process will come here.
        if (self.instances):
            hdl_code = hdl_code + self.instances.code()
            hdl_code = hdl_code + "\n"
        if (self.bodyCodeFooter):
            hdl_code = hdl_code + self.bodyCodeFooter.code(1)
            hdl_code = hdl_code + "\n"
        hdl_code = hdl_code + indent(0) + ("end %s;\n" % self.name)
        hdl_code = hdl_code + "\n"
        return hdl_code


class BasicVHDL:
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
        hdl_code = hdl_code + self.architecture.code()
        return hdl_code
