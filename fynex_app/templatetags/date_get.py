from django import template

register = template.Library()

@register.filter
def date_get(value):
    try:
        return str(value.date())
    except:
        return str(value)