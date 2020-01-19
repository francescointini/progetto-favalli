from django import forms

from .models import Component, Structural

class ComponentCreationForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = [
            'name',
            'file',
        ]

class StructuralSelectionForm(forms.ModelForm):
    component_list = forms.ModelChoiceField(
        queryset=Component.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    conferma = forms.ChoiceField(
        required=False,
        choices=[(False, 'No'), (True, 'Si')],
    )

    class Meta:
        model = Structural
        fields = (
            'name',
            'component_list',
        )

class StructuralMappingForm(forms.Form):
    porte = forms.ChoiceField(
        choices=[('port1', 'port1'), ('port2', 'port2'), ('port3', 'port3')],
        required=True,
        label='Mapping'
    )

    def __init__(self, *args, **kwargs):
        # port_list !C identity
        port_list = kwargs.pop('port_list')
        identity = kwargs.pop('identity')
        # print(self.fields['porte'])
        port_list = [(e, e) for e in port_list]
        # print(port_list)
        self.declared_fields['porte'].choices = port_list
        super(StructuralMappingForm, self).__init__(*args, **kwargs)
        
class StructuralFinalizeForm(forms.Form):
    entity_name = forms.CharField(
        max_length=50,
    )
    architecture_name = forms.CharField(
        max_length=50
    )