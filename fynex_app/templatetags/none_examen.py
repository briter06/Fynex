from django import template

register = template.Library()

@register.filter
def none_examen(value):
    if value == 'None':
        return 'Pendiente'
    else:
        return value