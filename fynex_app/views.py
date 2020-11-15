from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .recommender.HybridRecommender import HybridRecommender
from .classes.Administrator import Administrator
from .classes.CentroMedico import CentroMedicoHelper
from .classes.Medico import MedicoHelper

def page_not_found(request, *args, **argv):
    response = render(request, 'fynex_app/404.html')
    response.status_code = 404
    return response


def server_error(request, *args, **argv):
    response = render(request, 'fynex_app/500.html')
    response.status_code = 500
    return response

def privacy_policy(request):
    return render(request, 'fynex_app/privacy-policy.html')

# Create your views here.

def login_user(request, template_name):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        messages.error(
            request, 'El usuario o la contraseña son incorrectos')
    else:
        login(request, user)
    return HttpResponseRedirect(reverse(template_name))

def verify_auth(request,group_name):
    if not request.user.groups.filter(name=group_name).exists():
        return False
    return True

def index(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            return login_user(request, 'Fynex-index')
    else:
        if request.user.is_authenticated:
            if request.user.groups.filter(name='administrator').exists():
                return HttpResponseRedirect(reverse('Administrator-index'))
            elif request.user.groups.filter(name='centro_medico').exists():
                return HttpResponseRedirect(reverse('CentroMedico-index'))
            elif request.user.groups.filter(name='medico').exists():
                return HttpResponseRedirect(reverse('Medico-index'))
            else:
                return logout_user(request)
        else:
            return render(request, 'fynex_app/index.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Fynex-index'))

def administrator_index(request):
    if not verify_auth(request,'administrator'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        admin = Administrator(request.user)
        if 'edit' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            username = request.POST['username']
            first_name = request.POST['first_name']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            centro = admin.modificar_centro(id_prev,username,first_name,direccion,telefono)
            if centro == None:
                messages.error(request, 'El centro médico no se ha editado correctamente')
            else:
                messages.success(request, 'El centro médico se ha editado correctamente')
            return HttpResponseRedirect(reverse('Administrator-index'))
        elif 'add' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            centro = admin.registrar_centro(username,username.split('@')[0],first_name,direccion,telefono)
            if centro == None:
                messages.error(request, 'El centro médico no se ha agregado correctamente')
            else:
                messages.success(request, 'El centro médico se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Administrator-index'))
        elif 'delete' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            centro = admin.eliminar_centro(id_prev)
            if centro == False:
                messages.error(request, 'El centro médico no se ha eliminado correctamente')
            else:
                messages.success(request, 'El centro médico se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Administrator-index'))
    else:
        context = {}
        admin = Administrator(request.user)
        context['centros'] = admin.getCentrosMedicos()
        return render(request,'fynex_app/administrator/administrator_index.html',context)


def centroMedico_index(request):
    if not verify_auth(request,'centro_medico'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        centro = CentroMedicoHelper(request.user)
        if 'edit' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            username = request.POST['username']
            first_name = request.POST['first_name']
            documento_identificacion = request.POST['identificacion']
            especialidad = request.POST['especialidad']
            telefono = request.POST['telefono']
            medico = centro.modificar_medico(id_prev,username,first_name,documento_identificacion,especialidad,telefono)
            if medico == None:
                messages.error(request, 'El médico no se ha editado correctamente')
            else:
                messages.success(request, 'El médico se ha editado correctamente')
            return HttpResponseRedirect(reverse('CentroMedico-index'))
        elif 'add' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            documento_identificacion = request.POST['identificacion']
            especialidad = request.POST['especialidad']
            telefono = request.POST['telefono']
            medico = centro.registrar_medico(username,username.split('@')[0],first_name,documento_identificacion,especialidad,telefono)
            if medico == None:
                messages.error(request, 'El médico no se ha agregado correctamente')
            else:
                messages.success(request, 'El médico se ha agregado correctamente')
            return HttpResponseRedirect(reverse('CentroMedico-index'))
        elif 'delete' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            medico = centro.eliminar_medico(id_prev)
            if medico == False:
                messages.error(request, 'El médico no se ha eliminado correctamente')
            else:
                messages.success(request, 'El médico se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('CentroMedico-index'))
    else:
        context = {}
        centro = CentroMedicoHelper(request.user)
        context['medicos'] = centro.getMedicos()
        return render(request,'fynex_app/centro_medico/centro_medico_index.html',context)


def medico_index(request):
    if not verify_auth(request,'medico'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'edit' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            username = request.POST['username']
            first_name = request.POST['first_name']
            documento_identificacion = request.POST['identificacion']
            telefono = request.POST['telefono']
            paciente = medico.modificar_paciente(id_prev,username,first_name,documento_identificacion,telefono)
            if paciente == None:
                messages.error(request, 'El paciente no se ha editado correctamente')
            else:
                messages.success(request, 'El paciente se ha editado correctamente')
            return HttpResponseRedirect(reverse('Medico-index'))
        elif 'add' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            documento_identificacion = request.POST['identificacion']
            telefono = request.POST['telefono']
            paciente = medico.registrar_paciente(username,username.split('@')[0],first_name,documento_identificacion,telefono)
            if paciente == None:
                messages.error(request, 'El paciente no se ha agregado correctamente')
            else:
                messages.success(request, 'El paciente se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Medico-index'))
        elif 'delete' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            paciente = medico.eliminar_paciente(id_prev)
            if paciente == False:
                messages.error(request, 'El paciente no se ha eliminado correctamente')
            else:
                messages.success(request, 'El paciente se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-index'))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['pacientes'] = medico.getPacientes()
        return render(request,'fynex_app/medico/medico_index.html',context)




        
'''
def administrator_index(request):
    if not verify_auth(request,'administrator'):
        return HttpResponseRedirect(reverse('Fynex-index'))

    heartRate = 60
    glucose = 180
    height = 1.65
    weight = 85
    age = 55

    hr = HybridRecommender()

    result = hr.predictNutrition(heartRate,glucose,height,weight,age)
    print(result)
    return render(request,'fynex_app/administrator/administrator_index.html',{"result":result['recommendations'].to_html(classes='table table-responsive')})
'''