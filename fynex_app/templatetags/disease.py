from django import template

register = template.Library()

@register.filter
def disease(value):
    if value == 'anorexy':
        return 'Anorexia Nerviosa'
    if value == 'obesity':
        return 'Obesidad'
    if value == 'diabetes':
        return 'Diabetes'
    if value == 'hypertension':
        return 'Hipertensión arterial'