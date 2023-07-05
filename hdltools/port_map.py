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
