from format_text import indent

def VHDLenum(list, indent_level = 0):
	hdl_code = ""
	i = 0
	for j in list:
		i = i+1
		if (i == len(list)):
			tmp = list[j].code()
			tmp = tmp.replace(";", "")
			tmp = tmp.replace(",", "")
			hdl_code = hdl_code + indent(indent_level) + tmp
		else:
			hdl_code = hdl_code + indent(indent_level) + \
					list[j].code()
	return hdl_code


def DictCode(DictInput, indent_level = 0):
    hdl_code = ""
    for j in DictInput:
        hdl_code = hdl_code + indent(indent_level) + DictInput[j].code()
    return hdl_code
