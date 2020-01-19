from django.shortcuts import get_object_or_404

from .models import Component, Structural

def get_port_list(components):
    components_list = str(components).replace(',', '').strip().split(' ')
    port_list = []
    for c in components_list:
        component = get_object_or_404(Component, pk=c)
        ports = component.input_ports + component.output_ports
        p_list = ports.strip().split('|SEP|')
        p_list = p_list[:-1]

        c_list = []
        for p in p_list:
            n_string = str(p) + ' ID padre:' + str(c)
            c_list.append(n_string)

        port_list.append(c_list)
    # print(port_list)

    flat_port = []
    def removeNest(list_element):
        for element in list_element:
            if type(element) == list:
                removeNest(element)
            else:
                flat_port.append(element)
    removeNest(port_list)
    # print(flat_port)

    return flat_port

def get_sys_ports(mappings):
    l_mappings = mappings.split('|SEP|')

    res = []
    for m in l_mappings:
        if 'PORTA_ENTITA' in m:
            sys_port = m.split()[5:-1]
            sys_port = ' '.join(sys_port)
            res.append(sys_port)
    # print(res)
    return res

def clean_list(list):
    res = []
    for element in list:
        if len(element) == 0:
            continue
        else:
            res.append(element)
    return res

def get_component(pk):
    component = get_object_or_404(Component, pk=pk)
    
    port_c = 0
    name = component.entity_name
    ports = ''
    in_ports = component.input_ports.strip().split('|SEP|')
    in_ports = clean_list(in_ports)
    for i in in_ports:
        if len(i) > 1:
            i = i.strip().split(' ')
            ports += i[0] + ' : ' + i[1] + ' ' + i[2] + ';<br>'
    
    out_ports = component.output_ports.strip().split('|SEP|')
    out_ports = clean_list(out_ports)
    for o in out_ports:
        if len(o) > 1:
            if o == out_ports[-1]:
                end = True
            else:
                end = False
            o = o.strip().split(' ')
            ports += o[0] + ' : ' + o[1] + ' ' + o[2]
            if end:
                ports += '<br>'
            else:
                ports += ';<br>'
    port_c += len(in_ports) + len(out_ports)
    return name, ports, port_c

def signals_mapping(structural):
    component_ids = structural.component_list.replace(',', '').split(' ')

    mappings = structural.mappings.strip().lower().split('|sep|')
    mapp_source = []
    mapp_dest = []

    signal_c = 0
    signal_list = []
    m_list = []

    for m in mappings:
        new_l = m.split(' => ')
        mapp_source.append(new_l[0])
        mapp_dest.append(new_l[1])
    
    # print(mapp_dest)
    # print(mapp_source)
    # print('B')
    for i in range(0, len(mapp_source)):
        if 'porta_entita' in mapp_dest[i]:
            # print(mapp_source[i])
            # print(mappings[i])
            s_str = mapp_source[i]
            s_list = s_str.split(' ')
            d_list = mapp_dest[i].split(' ')
            li = [s_list[3], s_list[0], d_list[0]]
            m_list.append(li)
            continue
        else:
            # print('HIT')
            # print(mapp_source[i])
            # print(mapp_dest[i])
            # print(mappings[i])
            s_str = mapp_source[i]
            s_list = s_str.split(' ')
            d_str = mapp_dest[i]
            d_list = d_str.split(' ')

            signal = 'segnale' + str(signal_c)
            sig_l = [signal, s_list[2]]
            signal_list.append(sig_l)

            list1 = [s_list[3], s_list[0], signal]
            list2 = [d_list[3], d_list[0], signal]
            # print('LISTS')
            # print(list1)
            # print(list2)
            m_list.append(list1)
            m_list.append(list2)

            signal_c += 1
    # print(m_list)
    # print(signal_list)
    return m_list, signal_list
            
def get_signal_text(sig):
    res = ''

    for s in sig:
        res += s[0] + ' : ' + s[1] + ';<br>'
    return res

# def clean_mappings(mapping_signals):


def component_init(component_list, mapping_signals):
    c = 0
    for component in component_list:
        # print(component)
        print(mapping_signals)
        m = [li for li in mapping_signals if li[0] == component['pk']]
        # print(m)
        mapping_text = ''
        # clean_mappings(mapping_signals)
        # print('PORTE')
        # print(m)
        for e in m:
            text = e[1] + ' => ' + e[2] + ',<br>'
            mapping_text += text
        
        component['mapping_text'] = mapping_text
        map_str = component['entity'][0] + str(c) + ' : ' + component['entity']
        component['map_str'] = map_str
        #print()
        #print(component['mapping_text'])
        mapping_text = ''

def output_generation(structural):
    res = {}

    library = 'LIBRARY ieee;<br>USE ieee.std_logic_1164.ALL;<br>LIBRARY adk;<br>USE adk.all;<br>'.lower()
    res['library'] = library

    entity_r1 = f"entity {structural.entity_name} is<br>"
    res['entity_r1'] = entity_r1.lower()
    port_r1 = 'port (<br>'
    res['port_r1'] = port_r1.lower()

    sys_ports = get_sys_ports(structural.mappings)
    port_body = ''
    port_list = []
    
    for sys in sys_ports:
        s = sys.split(' ')
        str_port = s[0] + ' : ' + s[1] + ' ' + s[2] + ';<br>'

        port_list.append(str_port)
    
    for p in port_list:
        if 'in' in p:
            port_body = p + port_body
        elif 'out' in p:
            port_body += p
    port_body = port_body[0:-5] + port_body[-4:]
    res['port_body'] = port_body.lower()

    port_rl = ');<br>'
    res['port_rl'] = port_rl

    entity_rl = f'end entity {structural.entity_name};<br>'.lower()
    res['entity_rl'] = entity_rl

    arch_r1 = f'architecture {structural.architecture_name} of {structural.entity_name} is<br>'.lower()
    res['arch_r1'] = arch_r1

    mapping_signals, sig = signals_mapping(structural)

    sig_declaration = 'signal<br>'
    res['sig_declaration'] = sig_declaration

    s_text = get_signal_text(sig)
    res['signal_text'] = s_text

    components = structural.component_list
    components = components.replace(',', '').split(' ')
    component_list = []
    for c in components:
        d = {}
        name, ports, port_counter = get_component(c)

        name_str = f"component {name}<br>"
        d['pk'] = c
        d['entity'] = name
        d['name_c'] = name_str
        d['ports'] = ports
        d['port_counter'] = port_counter
        component_list.append(d)
    
    res['component_list'] = component_list

    component_rl = 'end component;<br>'
    res['component_rl'] = component_rl

    begin = 'begin<br>'
    res['begin'] = begin

    component_init(component_list, mapping_signals)
    res['component_list'] = component_list

    map_satement = 'port map(<br>'
    res['map_statement'] = map_satement

    arch_rl = f'end {structural.architecture_name};<br>'
    res['arch_rl'] = arch_rl

    return res
    