from django import template

register = template.Library()

data = {
    'Cicla elíptica':'clica_eliptica',
    'Cicla estática' : 'cicla_estatica',
    'Caminadora':'caminadora',
    'Caminar':'caminar',
    'Cicla':'cicla',
    'Correr':'correr',
    'Patinar':'patinar',
    'Nadar':'nadar',
    'Kickboxing' : 'kickboxing',
    'Saltar cuerda' : 'cuerda',
    'Baile aeróbico' : 'baile_aerobico',
    'Aeróbicos acuáticos' : 'aerobico_acuatico',
    'Yoga':'yoga'
}

@register.filter
def img_ejercicio(value):
    try:
        return data[value]
    except:
        return 'defecto'