from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .recommender.HybridRecommender import HybridRecommender
from .recommender.ContentRecommenderExercise import ContentRecommenderExercise
from .classes.Administrator import Administrator
from .classes.CentroMedico import CentroMedicoHelper
from .classes.Medico import MedicoHelper
from .classes.Paciente import PacienteHelper
import datetime


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
            elif request.user.groups.filter(name='paciente').exists():
                return HttpResponseRedirect(reverse('Paciente-index'))
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
            fecha_nac = request.POST['fecha_nacimiento']
            fecha_nacimiento = datetime.datetime.strptime(fecha_nac, "%Y-%m-%d").date()
            documento_identificacion = request.POST['identificacion']
            telefono = request.POST['telefono']
            paciente = medico.modificar_paciente(id_prev,username,first_name,fecha_nacimiento,documento_identificacion,telefono)
            if paciente == None:
                messages.error(request, 'El paciente no se ha editado correctamente')
            else:
                messages.success(request, 'El paciente se ha editado correctamente')
            return HttpResponseRedirect(reverse('Medico-index'))
        elif 'add' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            fecha_nac = request.POST['fecha_nacimiento']
            fecha_nacimiento = datetime.datetime.strptime(fecha_nac, "%Y-%m-%d").date()
            documento_identificacion = request.POST['identificacion']
            telefono = request.POST['telefono']
            paciente = medico.registrar_paciente(username,username.split('@')[0],first_name,fecha_nacimiento,documento_identificacion,telefono)
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

def verify_paciente(request,cod_paciente):
    medico = MedicoHelper(request.user)
    res = medico.verifyPaciente(cod_paciente)
    return res.count() != 0

def verify_planNutricional(request,cod_paciente,cod_plan):
    medico = MedicoHelper(request.user)
    res = medico.verifyPlanNutricional(cod_paciente,cod_plan)
    return res.count() != 0

def medico_paciente(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        return render(request,'fynex_app/medico/medico_paciente.html',context)




def medico_variables(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'edit' in request.POST:
            id_prev = request.POST['id']
            nombre = request.POST['nombre']
            intervalo_referencia = request.POST['intervalo_referencia']
            unidad = request.POST['unidad']
            paciente = medico.getPaciente(cod_paciente)
            paciente = medico.modificarVariable(id_prev,nombre,intervalo_referencia,unidad)
            if paciente == None:
                messages.error(request, 'La variable no se ha editado correctamente')
            else:
                messages.success(request, 'La variable se ha editado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-index', kwargs={'cod_paciente': cod_paciente}))
        elif 'add' in request.POST:
            nombre = request.POST['nombre']
            intervalo_referencia = request.POST['intervalo_referencia']
            unidad = request.POST['unidad']
            paciente = medico.getPaciente(cod_paciente)
            variable = medico.addVariableSeguimiento(nombre,intervalo_referencia,unidad,paciente,0)
            if variable == None:
                messages.error(request, 'La variable no se ha agregado correctamente')
            else:
                messages.success(request, 'La variable se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-index', kwargs={'cod_paciente': cod_paciente}))
        elif 'delete' in request.POST:
            id_prev = request.POST['id']
            variable = medico.eliminarVariable(id_prev)
            if variable == False:
                messages.error(request, 'La variable no se ha eliminado correctamente')
            else:
                messages.success(request, 'La variable se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['variables'] = medico.getVariablesSeguimiento(cod_paciente)
        return render(request,'fynex_app/medico/medico_variables.html',context)

def medico_variable_historico(request,cod_paciente,cod_variable):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'edit' in request.POST:
            id_prev = request.POST['id']
            fech = request.POST['fecha']
            fecha = datetime.datetime.strptime(fech, "%Y-%m-%d").date()
            valor = request.POST['valor']
            variable = medico.getVariable(cod_variable)
            historico = medico.modificarHistorialVariable(id_prev,fecha,valor)
            if historico == None:
                messages.error(request, 'El valor no se ha editado correctamente')
            else:
                messages.success(request, 'El valor se ha editado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-historial-index', kwargs={'cod_paciente': cod_paciente,'cod_variable':cod_variable}))
        elif 'add' in request.POST:
            fech = request.POST['fecha']
            fecha = datetime.datetime.strptime(fech, "%Y-%m-%d").date()
            valor = request.POST['valor']
            variable = medico.getVariable(cod_variable)
            historico = medico.guardarHistorialVariable(variable,fecha,valor)
            if historico == None:
                messages.error(request, 'El valor no se ha agregado correctamente')
            else:
                messages.success(request, 'El valor se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-historial-index', kwargs={'cod_paciente': cod_paciente,'cod_variable':cod_variable}))
        elif 'delete' in request.POST:
            id_prev = request.POST['id']
            historico = medico.eliminarHistorialVariable(id_prev)
            if historico == False:
                messages.error(request, 'El valor no se ha eliminado correctamente')
            else:
                messages.success(request, 'El valor se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-historial-index', kwargs={'cod_paciente': cod_paciente,'cod_variable':cod_variable}))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        variable = medico.getVariable(cod_variable)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['variable'] = variable
        context['historico'] = medico.getHistoricoVariable(variable)
        return render(request,'fynex_app/medico/medico_variable_historial.html',context)


def medico_nutricion(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'delete' in request.POST:
            id_prev = request.POST['id']
            plan = medico.eliminarPlanNutricional(id_prev)
            if plan == False:
                messages.error(request, 'El plan nutricional no se ha eliminado correctamente')
            else:
                messages.success(request, 'El plan nutricional se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['planes'] = medico.getPlanesNutricionales(cod_paciente)
        return render(request,'fynex_app/medico/nutrition_recommendations_index.html',context)
    


def medico_generar_nutricion(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'save' in request.POST:
            id_p = request.POST['id']
            rating = request.POST['rate'] if 'rate' in request.POST else 0
            estado = "A" if 'estado' in request.POST else "I"
            plan = medico.modificarPlanNutricional(id_p,rating,estado)
            if plan == False:
                messages.error(request, 'El plan nutricional no se ha modificado correctamente')
            else:
                messages.success(request, 'El plan nutricional se ha modificado correctamente')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        medico = MedicoHelper(request.user)

        heartRate = medico.getRitmoCardiaco(cod_paciente)
        if heartRate == None:
            messages.error(request, 'Por favor registre un valor en la variable: Ritmo cardíaco')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            heartRate = heartRate.valor
        glucose = medico.getGlucosa(cod_paciente)
        if glucose == None:
            messages.error(request, 'Por favor registre un valor en la variable: Nivel de glucosa')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            glucose = glucose.valor
        height = medico.getAltura(cod_paciente)
        if height == None:
            messages.error(request, 'Por favor registre un valor en la variable: Altura')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            height = height.valor
        weight = medico.getPeso(cod_paciente)
        if weight == None:
            messages.error(request, 'Por favor registre un valor en la variable: Peso')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            weight = weight.valor
        age = medico.getEdad(cod_paciente)
        

        hr = HybridRecommender()
        result = hr.predictNutrition(heartRate,glucose,height,weight,age)
        
        plan = medico.guardarRecomendacionNutricion(result['recommendations'],cod_paciente)
        context = {}
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['plan'] = plan
        context['partes'] = medico.getPartesDePlanNutricional(plan)
        context['heartRate'] = heartRate
        context['glucose'] = glucose
        context['height'] = height
        context['weight'] = weight
        context['age'] = age
        context['nueva'] = True
        context['diseases'] = result['diseases']
        return render(request,'fynex_app/medico/nutrition_recommendations_generation.html',context)

def medico_detail_nutricion(request,cod_paciente,cod_plan):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente) or not verify_planNutricional(request,cod_paciente,cod_plan):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'save' in request.POST:
            id_p = request.POST['id']
            rating = request.POST['rate'] if 'rate' in request.POST else 0
            estado = "A" if 'estado' in request.POST else "I"
            plan = medico.modificarPlanNutricional(id_p,rating,estado)
            if plan == False:
                messages.error(request, 'El plan nutricional no se ha modificado correctamente')
            else:
                messages.success(request, 'El plan nutricional se ha modificado correctamente')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        medico = MedicoHelper(request.user)
        context = {}
        plan = medico.getPlanNutricional(cod_plan)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['plan'] = plan
        context['partes'] = medico.getPartesDePlanNutricional(plan)
        return render(request,'fynex_app/medico/nutrition_recommendations_generation.html',context)




def medico_chat(request, cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    
    medico = MedicoHelper(request.user)
    paciente = medico.getPaciente(cod_paciente)
    return render(request, 'fynex_app/chat.html', {
        'room_name': str(cod_paciente),
        'sender_name' : request.user.first_name,
        'receiver_name' : paciente.user.first_name
    })

def paciente_chat(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    
    pacienteHelper = PacienteHelper(request.user)
    paciente = pacienteHelper.paciente
    return render(request, 'fynex_app/chat.html', {
        'room_name': str(paciente.id),
        'sender_name' : paciente.user.first_name,
        'receiver_name' : paciente.medico.user.first_name
    })


def paciente_index(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        pacienteHelper = PacienteHelper(request.user)
        context['paciente'] = pacienteHelper.paciente
        return render(request,'fynex_app/paciente/paciente_index.html',context)

def paciente_nutricion(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        pacienteHelper = PacienteHelper(request.user)
        context['paciente'] = pacienteHelper.paciente
        context['planes'] = pacienteHelper.getPlanesNutricionales()
        return render(request,'fynex_app/paciente/nutrition_recommendations_index.html',context)

def paciente_detail_nutricion(request,cod_plan):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    
    pacienteHelper = PacienteHelper(request.user)
    paciente = pacienteHelper.paciente
    context = {}
    plan = pacienteHelper.getPlanNutricional(cod_plan)
    if plan==None:
        return HttpResponseRedirect(reverse('Fynex-index'))
    context['paciente'] = paciente
    context['plan'] = plan
    context['partes'] = pacienteHelper.getPartesDePlanNutricional(plan)
    return render(request,'fynex_app/paciente/nutrition_recommendations_generation.html',context)