from django.contrib import admin

from vhdl.models import Component, Structural

class ComponentAdmin(admin.ModelAdmin):
    date_hierarchy='created_at'

    list_display = [
        'name',
        'file',
        'entity_name',
        'input_ports',
        'output_ports',
        'architecture_name',
        'created_at',
    ]

    fields = [
        'name',
        'file',
    ]

admin.site.register(Component, ComponentAdmin)

class StructuralAdmin(admin.ModelAdmin):
    date_hierarchy='created_at'

    list_display = [
        'name',
        'component_list',
        'created_at',
    ]

admin.site.register(Structural, StructuralAdmin)
