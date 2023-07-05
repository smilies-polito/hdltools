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
