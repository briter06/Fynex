from django import template

register = template.Library()

@register.filter
def state_n(value):
    if value == 'A':
        return 'Activo'
    if value == 'I':
        return 'Inactivo'