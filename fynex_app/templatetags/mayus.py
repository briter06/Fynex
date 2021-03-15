from django import template

register = template.Library()

@register.filter
def mayus(value):
    return value.upper()