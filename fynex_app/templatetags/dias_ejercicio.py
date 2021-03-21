from django import template

register = template.Library()

@register.filter
def dias_ejercicio(value):
    partes = value.split(',')
    return f'Entre {partes[0]} y {partes[1]} días'