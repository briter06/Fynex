from django import template

register = template.Library()

@register.filter
def tipo_ejercicio(value):
    if value == 'aerobic':
        return "Aeróbico"
    else:
        return value