from django import template

register = template.Library()

def port_clean(value):
    new_value = value.split('|SEP|')
    res = ''
    for element in new_value:
        res += element + '<br>'
    return res

register.filter('port_clean', port_clean)