from django.shortcuts import render, get_object_or_404, redirect

from .models import Component, Structural
from .forms import ComponentCreationForm, StructuralSelectionForm, StructuralMappingForm, StructuralFinalizeForm

import datetime
from .structural_functions import get_port_list, output_generation

def home(request):
    return render(request, 'home.html', {})

def component_creation(request):
    if request.POST:
        form = ComponentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            component = form.save(commit=False)
            component.save()
            return render(request, 'home.html', {})
    else:
        form = ComponentCreationForm()
        return render(request, 'component/creation.html', {
            'form': form
        })

def component_list(request):
    qs = Component.objects.all()

    return render(request, 'component/list.html', {
        'qs': qs
    })

def component_retrive(components):
    res = [get_object_or_404(Component, pk=element) for element in components]
    return res

def structural_selection(request):
    if request.POST:
        component_list=''
        form = StructuralSelectionForm(request.POST)
        
        post = request.POST
        components_list = post.getlist('component_list')
        components = component_retrive(components_list)
        # print(components[0].__dict__)
        # print(request.POST)
        if 'conferma' in post:
            structural = Structural()
            structural.name = post['name']
            
            str_components = str(components_list)
            str_components = str_components.replace('[', '').replace(']', '').replace("'", '')
            # print(str_components)

            structural.component_list = str_components
            structural.created_at = datetime.datetime.now()
            structural.save()

            return redirect(f"/structural/mapping/{structural.pk}")
            # salva component e naviga alla pagina corrispondete del mapping
        return render(request, 'structural/selection.html', {
            'form': form,
            'components': components
        })
    else:
        form = StructuralSelectionForm()
        return render(request, 'structural/selection.html', {
            'form': form
        })

def structural_mapping(request, pk = 0):
    structural = get_object_or_404(Structural, pk=pk)
    port_list = get_port_list(structural.component_list)

    if request.POST:
        # print(request.POST)
        post = request.POST
        select = post.getlist('porte')
        # print(len(select))
        # print(len(port_list))
        mappings = []
        for i in range(0, len(port_list)):
            res = []
            id_parent1 = port_list[i].split(' ')[-1].split(':')[-1]
            frst = port_list[i].split(' ')[0:3]
            id_parent2 = select[i].split(' ')[-1].split(':')[-1]
            snd = select[i].split(' ')[0:3]
            s_frst = ' '.join(frst) + ' ' + str(id_parent1)
            s_snd = ' '.join(snd) + ' ' + str(id_parent2)
            res = s_frst + ' => ' + s_snd
            # print(res)
            mappings.append(res)
        
        # print(mappings)
        c = 0
        c_mappings = []
        for s in mappings:
            if 'PORTA_ENTITA' in s:
                # print('----')
                replace_str = f"PORTA_ENTITA_N{c}"
                s = s.replace('PORTA_ENTITA', replace_str)
                # print(s)
                c += 1
            c_mappings.append(s)
        
        # print(mappings)
        str_mappings = '|SEP|'.join(c_mappings)
        structural.mappings = str_mappings
        structural.save()

        return redirect(F"/structural/finalize/{structural.pk}")
    else:
        # print(port_list)
        mapping_forms = []
        for port in port_list:
            d = {}

            new_port = port_list[:]
            id_parent = port.split(' ')[-1].split(':')[-1]
            # print(id_parent)
            i = new_port.index(port)
            # print(port)
            # new_port.remove(new_port[i])
            ids = []
            for p in new_port:
                if id_parent in p:
                    ids.append(new_port.index(p))
            
            c = 0
            for id in ids:
                new_port.remove(new_port[id - c])
                c += 1
            
            port_type = port.split(' ')[2]
            port_verse = port.split(' ')[1]
            system_port = 'PORTA_ENTITA ' + port_verse + ' ' + port_type
            new_port.append(system_port)
            
            form = StructuralMappingForm(port_list=new_port, identity=i)
            #print(port_list)
            # form.porte.choices = new_port
            # choices = [(e, e) for e in new_port]
            # form.fields['porte']._choices = choices
            # print(form.fields['porte']._choices)

            d['port'] = port
            d['form'] = form
            mapping_forms.append(d)
            #print(mapping_forms)

        return render(request, 'structural/mapping.html', {
            'structural': structural,
            'port_list': port_list,
            'mapping_forms': mapping_forms,
        })

def structural_finalize(request, pk = 0):
    structural = get_object_or_404(Structural, pk=pk)
    if request.POST:
        entity_name = request.POST['entity_name']
        architecture_name = request.POST['architecture_name']
        print(request.POST)
        print(entity_name, architecture_name)
        
        structural.entity_name = entity_name
        structural.architecture_name = architecture_name
        structural.save()

        return redirect(f'/structural/detail_view/{structural.pk}')

    else:
        form = StructuralFinalizeForm()
        return render(request, 'structural/finalize.html', {
            'structural': structural,
            'form': form,
        })

def structural_detail_view(request, pk = 0):
    structural = get_object_or_404(Structural, pk=pk)
    out = output_generation(structural)
    return render(request, 'structural/detail_view.html', {
        'structural': structural,
        'out': out
    })
