from django import template

register = template.Library()

@register.filter
def tiempo_ejercicio(value):
    partes = value.split(',')
    if partes[0] == 'inf':
        return f'Menos de {partes[1]} minutos diarios'
    elif partes[1] == 'inf':
        return f'Más de {partes[0]} minutos diarios'
    else:
        return f'Entre {partes[0]} y {partes[1]} minutos diarios'