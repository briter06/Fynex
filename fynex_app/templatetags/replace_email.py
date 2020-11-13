from django import template

register = template.Library()

@register.filter
def replace_email(value):
    return value.replace("@",":")