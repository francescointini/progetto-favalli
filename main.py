import os

class Library:
    # struttura dati atta a contenere le librerie di un file vhdl
    # per convenzione queste vanno esclusivamente sulle prime due
    # righe del file
    def __init__(self):
        self.first_line = '',
        self.second_line = '',
    
    def __str__(self):
        return "%s %s" % (self.first_line, self.second_line)


class Entity:
    # struttura dati per le entity
    # salva nome della entity e i nomi
    # delle porte, non mi interessa il tipo
    # da richiesta devono essere solo std_logic
    def __init__(self):
        self.name = '',
        self.input_port1 = '',
        self.input_port2 = '',
        self.output_port1 = '',
        self.output_port2 = '',
    
    def __str__(self):
        return "%s, in: %s %s, out: %s %s" % \
            (
                self.name,
                self.input_port1,
                self.input_port2,
                self.output_port1,
                self.output_port2
            )


class Architcture:
    def __init__(self):
        self.name = '',
    
    def __str__(self):
        return "%s" % self.name


class SignalMask:
    def __init__(self, entity):
        self.input_port1 = entity.input_port1.upper() + '_SGN'
        self.input_port2 = entity.input_port2.upper() + '_SGN'
        self.output_port1 = entity.output_port1.upper() + '_SGN'
        self.output_port2 = entity.output_port2.upper() + '_SGN'


# funzioni
def clean_list(list):
    # ritorna una lista priva di elementi vuoti
    res = []
    for element in list:
        if element != '':
            res.append(element)
    return res


# var di sistema
file_vhdl = 'test.vhdl'

# variabili di flag
component = False
# inizio del componente

# istanze
library = Library()
entity = Entity()
architecture = Architcture()

with open(file_vhdl, 'r') as file:
    # lettura del file .vhdl riga per riga
    lines = file.read().splitlines()
    for line in lines:
        # line ripulita dai ; e trasformata
        # tutta in minuscolo serve facilitare il 
        # riconoscimento dei pattern testuali
        c_line = line.replace(';', '').lower()
        # print(c_line)
        # non si può fare patternmatching su linee vuote
        if len(c_line) > 0:
            if 'library' in c_line:
                library.first_line = c_line
                continue
            if lines.index(line) == 1:
                library.second_line = c_line
                continue
            # fine lettura librerie
            # lettura entity
            if 'entity' in c_line:
                # ricavo il nome della entity
                n_line = c_line.split(' ')
                # print(n_line)
                entity.name = n_line[1].upper()
                continue
            if 'std_logic' in c_line:
                # ricavo il nome delle porte
                n_line = c_line.replace(',', '')
                n_line = n_line.split(' ')
                # print(n_line)
                if 'in' in n_line:
                    temp_line = clean_list(n_line)
                    # print(temp_line)
                    entity.input_port1 = temp_line[0].upper()
                    entity.input_port2 = temp_line[1].upper()
                    continue
                if 'out' in n_line:
                    temp_line = clean_list(n_line)
                    # print(temp_line)
                    entity.output_port1 = temp_line[0].upper()
                    entity.output_port2 = temp_line[1].upper()
                    continue
            if 'architecture' in c_line:
                # architecture name
                n_line = c_line.split(' ')
                architecture.name = n_line[1].upper()
                continue
        # print(len(c_line))
        # print(line)
print(library)
print(entity)
print(architecture)

# test bench funzionale
file_tb_vhdl = file_vhdl.replace('.', '_tb.')
mask = SignalMask(entity)

with open(file_tb_vhdl, 'w') as file:
    # creazione del file testbench_TB.VHDL e scrittura della testbench
    file.write(library.first_line + ';\n')
    file.write(library.second_line + ';\n\n')
    file.write('entity ' + entity.name + '_TB is\n')
    file.write('end ' + entity.name + '_TB;\n\n')
    file.write('architecture ' + architecture.name + '_TB of ' + entity.name.upper() + '_TB is\n')
    file.write('\tsignal ' + mask.input_port1 + ' : std_logic;\n')
    file.write('\tsignal ' + mask.input_port2 + ' : std_logic;\n')
    file.write('\tsignal ' + mask.output_port1 + ' : std_logic;\n')
    file.write('\tsignal ' + mask.output_port2 + ' : std_logic;\n\n')
    file.write("\tcomponent " + entity.name + " is\n")
    file.write("\tport (\n")
    file.write("\t\t" + entity.input_port1 + ", " + entity.input_port2 + " : in std_logic,\n")
    file.write("\t\t" + entity.output_port1 + ', ' + entity.output_port2 + ' : out std_logic);\n')
    file.write("\tend component;\n")
    file.write("begin\n")
    file.write("\t" + architecture.name + ' : ' + entity.name + " port map ( " + mask.input_port1 + ', ' + mask.input_port2 + ', ' + mask.output_port1 + ', ' + mask.output_port2  + " )\n")
    file.write("\n\t" + architecture.name + '_TB : process\n')
    file.write("\t\tQUI VANNO I PROCESSI\n")
    file.write("\tend process;\n")
    file.write("end " + architecture.name + "_TB;\n")
