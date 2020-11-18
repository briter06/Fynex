from django import template

register = template.Library()

@register.filter
def date_get(value):
    return str(value)