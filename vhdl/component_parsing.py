class Component:
    def __init__(self):
        self.entity_name = ''
        self.input_port = ''
        self.output_port = ''
        self.architecture_name = ''
    
    def __str__(self):
        return f"Componente: { self.entity_name }, { self.input_port }, \
        { self.output_port }, { self.architecture_name }"

class Port:
    def __init__(self):
        self.name = ''
        self.verse = ''
        self.type = ''
    
    def __str__(self):
        return f"{self.name} {self.verse} {self.type}"

def get_entity(lines):
    """
    Funzione che ritorna il nome dell'entity del componente VHDL
    """
    for line in lines:
        if ('entity' in line) and ('is' in line):
            new_line = line.strip().split(' ')
            return new_line[1]

def get_ports(lines):
    """
    Funzione che ritorna un vettore contenente le porte di input
    """
    port = False

    ins = []
    outs = []

    for line in lines:
        if 'port' in line and '(' in line:
            port = True
        if ');' in line and port:
            break
        if ':' in line and ('in' in line or 'out' in line):
            new_line = line.strip().split(' ')
            port = Port()
            # print(new_line)
            port.name = new_line[0]
            port.verse = new_line[2]
            port.type = new_line[3]

            if ';' in port.type:
                port.type = port.type.replace(';', '')

            if port.verse == 'in':
                ins.append(port)
            elif port.verse == 'out':
                outs.append(port)
    str_ins = ''
    str_outs = ''
    for element in ins:
        string = ''
        string += element.name
        string += ' '
        string += element.verse
        string += ' '
        string += element.type
        string += ' '
        string += '|SEP|'
        str_ins += string
    for element in outs:
        string = ''
        string += element.name
        string += ' '
        string += element.verse
        string += ' '
        string += element.type
        string += ' '
        string += '|SEP|'
        str_outs += string
    
    # print(str_ins, str_outs)
    return str_ins, str_outs

def get_architecture(lines, component_name):
    """
    Funzione che ritorna il nome dell'architettura del componente VHDL
    """
    for line in lines:
        if 'architecture' in line and component_name in line:
            new_line = line.strip().split(' ')
            return new_line[1]

def parsing(obj):
    with open(obj.file.path, 'r') as file:
        component = Component()
        lines = file.read().lower().splitlines()

        component.entity_name = get_entity(lines)
        component.input_port, component.output_port = get_ports(lines)
        component.input_port = component.input_port.strip()
        component.output_port = component.output_port.strip()
        component.architecture_name = get_architecture(lines, component.entity_name)

        # print(component.input_port)

        obj.entity_name = component.entity_name
        obj.input_ports = component.input_port
        obj.output_ports = component.output_port
        obj.architecture_name = component.architecture_name
        obj.save()
            