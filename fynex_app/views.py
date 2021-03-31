from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .recommender.HybridRecommender import HybridRecommender
from .recommender.ContentRecommenderExercise import ContentRecommenderExercise
from .classes.Administrator import Administrator
from .classes.CentroMedico import CentroMedicoHelper
from .classes.Medico import MedicoHelper
from .classes.Paciente import PacienteHelper
from .classes.Mensaje import MensajeHelper
from .classes.tools import Tools
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Sum
import datetime
import json
from fynex_app.forms import CaptchaTestModelForm
import math
from django.conf import settings


def download_test(request,file_name):
    nom = file_name.split('.')[0]
    cod_examen = int(nom.split('_')[1])
    if not (verify_auth(request,'medico') and verify_examen(request,cod_examen)) and not (verify_auth(request,'paciente') and verify_examen_paciente(request,cod_examen)):
        return render(request, 'File not found')
    file = Tools.cos_download.Object('fynex', file_name).get()
    response = HttpResponse(file['Body'].read(), content_type=file['ContentType'])
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    return response

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

def login_user(request, template_name):
    form = CaptchaTestModelForm(request.POST)
    if form.is_valid() or not settings.CAPTCHA:
        username = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(
                request, 'El usuario o la contraseña son incorrectos')
        else:
            login(request, user)
        return HttpResponseRedirect(reverse(template_name))
    else:
        messages.error(
                request, 'Por favor complete el Captcha')
        return HttpResponseRedirect(reverse(template_name))

def verify_auth(request,group_name):
    if not request.user.groups.filter(name=group_name).exists():
        return False
    return True


def recuperar_clave(request):
    if request.method == 'POST':
        if 'recuperar' in request.POST:
            email = request.POST['email']
            usuario = Tools.getUser(email)
            if usuario is None:
                messages.error(request, 'El correo no se encuentra registrado')
            else:
                try:
                    Tools.recuperarClave(usuario)
                    messages.success(request, f'Se ha envíado una contraseña temporal al correo {email}')
                except:
                    messages.error(request, 'Ha ocurrido un error')

            return HttpResponseRedirect(reverse('Fynex-recuperar')) 
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
            return render(request, 'fynex_app/forgot_password.html')

def index(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            return login_user(request, 'Fynex-index')
        if 'solicitar' in request.POST:
            try:
                email = request.POST['email']
                Tools.sendInformacion(email)
                messages.success(request, f'Se ha envíado información sobre Fynex al correo {email}')
            except:
                messages.error(request, 'Ha ocurrido un error')
            return HttpResponseRedirect(reverse('Fynex-index'))
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
            form = CaptchaTestModelForm(use_required_attribute=settings.CAPTCHA)
            return render(request, 'fynex_app/index.html', {'form': form})

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
                Tools.auditar(request,f'Se ha editado el centro médico {username}')
                messages.success(request, 'El centro médico se ha editado correctamente')
            return HttpResponseRedirect(reverse('Administrator-index'))
        elif 'add' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            centro = admin.registrar_centro(username,Tools.get_random_string(10),first_name,direccion,telefono)
            if centro == None:
                messages.error(request, 'El centro médico no se ha agregado correctamente')
            else:
                Tools.auditar(request,f'Se ha creado el centro médico: {username}')
                messages.success(request, 'El centro médico se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Administrator-index'))
        elif 'delete' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            centro = admin.eliminar_centro(id_prev)
            if centro == False:
                messages.error(request, 'El centro médico no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado el centro médico {id_prev}')
                messages.success(request, 'El centro médico se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Administrator-index'))
    else:
        context = {}
        admin = Administrator(request.user)
        context['centros'] = admin.getCentrosMedicos()
        return render(request,'fynex_app/administrator/administrator_index.html',context)

def administrator_auditoria(request):
    if not verify_auth(request,'administrator'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        context['auditoria'] = Tools.getAuditoria()
        return render(request,'fynex_app/administrator/auditoria.html',context)

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
                Tools.auditar(request,f'Se ha editado el médico: {username}')
                messages.success(request, 'El médico se ha editado correctamente')
            return HttpResponseRedirect(reverse('CentroMedico-index'))
        elif 'add' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            documento_identificacion = request.POST['identificacion']
            especialidad = request.POST['especialidad']
            telefono = request.POST['telefono']
            medico = centro.registrar_medico(username,Tools.get_random_string(10),first_name,documento_identificacion,especialidad,telefono)
            if medico == None:
                messages.error(request, 'El médico no se ha agregado correctamente')
            else:
                Tools.auditar(request,f'Se ha creado el médico: {username}')
                messages.success(request, 'El médico se ha agregado correctamente')
            return HttpResponseRedirect(reverse('CentroMedico-index'))
        elif 'delete' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            medico = centro.eliminar_medico(id_prev)
            if medico == False:
                messages.error(request, 'El médico no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado el médico {id_prev}')
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
                Tools.auditar(request,f'Se ha editado el paciente: {username}')
                messages.success(request, 'El paciente se ha editado correctamente')
            return HttpResponseRedirect(reverse('Medico-index'))
        elif 'add' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            fecha_nac = request.POST['fecha_nacimiento']
            fecha_nacimiento = datetime.datetime.strptime(fecha_nac, "%Y-%m-%d").date()
            documento_identificacion = request.POST['identificacion']
            telefono = request.POST['telefono']
            paciente = medico.registrar_paciente(username,Tools.get_random_string(10),first_name,fecha_nacimiento,documento_identificacion,telefono)
            if paciente == None:
                messages.error(request, 'El paciente no se ha agregado correctamente')
            else:
                Tools.auditar(request,f'Se ha creado el paciente: {username}')
                messages.success(request, 'El paciente se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Medico-index'))
        elif 'delete' in request.POST:
            id_prev = request.POST['id'].replace(':','@')
            paciente = medico.eliminar_paciente(id_prev)
            if paciente == False:
                messages.error(request, 'El paciente no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado el paciente: {id_prev}')
                messages.success(request, 'El paciente se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-index'))
    else:
        context = {}
        medico = MedicoHelper(request.user)

        context['pacientes'] = medico.getPacientes()
        return render(request,'fynex_app/medico/medico_index.html',context)

def medico_grafo(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        medico = MedicoHelper(request.user)

        paciente = medico.getPaciente(cod_paciente)
        similares = medico.getMostSimilar(cod_paciente,10)
        result = []
        info = {}
        max_radious = 50
        color_p = '#DF7600'
        color_m = '#1B6697'
        color_n_m = '#47C36F'
        nodos = [{'id':paciente.user.username,'color':color_p,'marker':{'radius':max_radious}}]
        info[paciente.user.username] = {'nombre':paciente.user.first_name,'medico':{'nombre':paciente.medico.user.first_name,'correo':paciente.medico.user.username}}
        for s in similares:
            aux = {}
            p = medico.getPaciente(s.user2)
            aux['from'] = paciente.user.username
            aux['to'] = p.user.username
            aux['weight'] = Tools.getPercentage(s.similitud,2)
            info[p.user.username] = {'propio':0,'id':p.id,'nombre':p.user.first_name,'medico':{'nombre':p.medico.user.first_name,'correo':p.medico.user.username}}
            color_nodo = color_n_m
            if p.medico == paciente.medico:
                color_nodo = color_m
                info[p.user.username]['propio'] = 1
            section_size = 4
            residuo = Tools.getPercentage(s.similitud,0)/(100/section_size)
            residuo = max(math.ceil(residuo),1)
            nodos.append({'id':p.user.username,'color':color_nodo,'marker':{'radius':int(max_radious*(residuo/section_size))}})
            result.append(aux)
        context['paciente'] = paciente
        context['data'] = result
        context['info'] = info
        context['nodos'] = nodos
        context['color_m'] = color_m
        context['color_n_m'] = color_n_m
        return render(request,'fynex_app/medico/medico_graph.html',context)


def verify_paciente(request,cod_paciente):
    medico = MedicoHelper(request.user)
    res = medico.verifyPaciente(cod_paciente)
    return res.count() != 0

def verify_examen(request,cod_examen):
    medico = MedicoHelper(request.user)
    res = medico.verifyExamen(cod_examen)
    return res.count() != 0

def verify_examen_paciente(request,cod_examen):
    paciente = PacienteHelper(request.user)
    res = paciente.verifyExamen(cod_examen)
    return res.count() != 0


def verify_planNutricional(request,cod_paciente,cod_plan):
    medico = MedicoHelper(request.user)
    res = medico.verifyPlanNutricional(cod_paciente,cod_plan)
    return res.count() != 0

def verify_planEjercicio(request,cod_paciente,cod_plan):
    medico = MedicoHelper(request.user)
    res = medico.verifyPlanEjercicio(cod_paciente,cod_plan)
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


def medico_grafico_variables(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        vars = {}
        variables = medico.getVariablesSeguimiento(cod_paciente)
        for v in variables:
            historico = medico.getHistoricoVariable(v.id)
            values = []
            dates = []
            for h in historico:
                values.append(h.valor)
                dates.append(str(h.fecha))
            vars[v.nombre] = [values,dates,v.unidad]
        context['variables'] = vars
        context['is_medico'] = True
        return render(request,'fynex_app/grafico_variables.html',context)

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
            variable = medico.modificarVariable(id_prev,nombre,intervalo_referencia,unidad)
            if variable == None:
                messages.error(request, 'La variable no se ha editado correctamente')
            else:
                Tools.auditar(request,f'Se ha editado la variable {nombre} para {paciente.user.username}')
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
                Tools.auditar(request,f'Se ha creado la variable {nombre} para {paciente.user.username}')
                messages.success(request, 'La variable se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-index', kwargs={'cod_paciente': cod_paciente}))
        elif 'delete' in request.POST:
            id_prev = request.POST['id']
            paciente = medico.getPaciente(cod_paciente)
            variable = medico.eliminarVariable(id_prev)
            if variable == False:
                messages.error(request, 'La variable no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado una variable para {paciente.user.username}')
                messages.success(request, 'La variable se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['variables'] = medico.getVariablesSeguimiento(cod_paciente)
        return render(request,'fynex_app/medico/medico_variables.html',context)


def medico_examenes(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'edit' in request.POST:
            id_prev = request.POST['id']
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            paciente = medico.getPaciente(cod_paciente)
            examen = medico.modificarExamen(id_prev,nombre,descripcion)
            if examen == None:
                messages.error(request, 'El examen no se ha editado correctamente')
            else:
                Tools.auditar(request,f'Se ha editado el exámen {nombre} para {paciente.user.username}')
                messages.success(request, 'El examen se ha editado correctamente')
            return HttpResponseRedirect(reverse('Medico-examenes-index', kwargs={'cod_paciente': cod_paciente}))
        elif 'add' in request.POST:
            nombre = request.POST['nombre']
            descripcion = request.POST['descripcion']
            fecha_peticion = Tools.getToday()
            paciente = medico.getPaciente(cod_paciente)
            examen = medico.addExamen(nombre,descripcion,fecha_peticion,paciente)
            if examen == None:
                messages.error(request, 'El examen no se ha agregado correctamente')
            else:
                Tools.auditar(request,f'Se ha creado el exámen {nombre} para {paciente.user.username}')
                messages.success(request, 'El examen se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Medico-examenes-index', kwargs={'cod_paciente': cod_paciente}))
        elif 'delete' in request.POST:
            id_prev = request.POST['id']
            paciente = medico.getPaciente(cod_paciente)
            examen = medico.eliminarExamen(id_prev)
            if examen == False:
                messages.error(request, 'El examen no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado un exámen para {paciente.user.username}')
                messages.success(request, 'El examen se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-examenes-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['examenes'] = medico.getExamenes(cod_paciente)
        return render(request,'fynex_app/medico/examenes.html',context)

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
                Tools.auditar(request,f'Se ha editado un valor de la variable {variable.nombre} para {variable.paciente.user.username}')
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
                Tools.auditar(request,f'Se ha creado un valor a la variable {variable.nombre} para {variable.paciente.user.username}')
                messages.success(request, 'El valor se ha agregado correctamente')
            return HttpResponseRedirect(reverse('Medico-variables-historial-index', kwargs={'cod_paciente': cod_paciente,'cod_variable':cod_variable}))
        elif 'delete' in request.POST:
            id_prev = request.POST['id']
            paciente = medico.getPaciente(cod_paciente)
            historico = medico.eliminarHistorialVariable(id_prev)
            if historico == False:
                messages.error(request, 'El valor no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado el valor de una variable para {paciente.user.username}')
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
            paciente = medico.getPaciente(cod_paciente)
            plan = medico.eliminarPlanNutricional(id_prev)
            if plan == False:
                messages.error(request, 'El plan nutricional no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado un plan nutricional para {paciente.user.username}')
                messages.success(request, 'El plan nutricional se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-nutricion-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['planes'] = medico.getPlanesNutricionales(cod_paciente)
        return render(request,'fynex_app/medico/nutrition_recommendations_index.html',context)

def medico_ejercicio(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'delete' in request.POST:
            id_prev = request.POST['id']
            paciente = medico.getPaciente(cod_paciente)
            plan = medico.eliminarPlanEjercicio(id_prev)
            if plan == False:
                messages.error(request, 'El plan de ejercicio no se ha eliminado correctamente')
            else:
                Tools.auditar(request,f'Se ha eliminado un plan de ejercicio para {paciente.user.username}')
                messages.success(request, 'El plan de ejercicio se ha eliminado correctamente')
            return HttpResponseRedirect(reverse('Medico-ejercicio-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        context = {}
        medico = MedicoHelper(request.user)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['planes'] = medico.getPlanesEjercicio(cod_paciente)
        return render(request,'fynex_app/medico/exercise_recommendations_index.html',context)

def medico_generar_ejercicio(request,cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'save' in request.POST:
            id_p = request.POST['id']
            rating = request.POST['rate'] if 'rate' in request.POST else 0
            estado = "A" if 'estado' in request.POST else "I"
            plan = medico.modificarPlanEjercicio(id_p,rating,estado)
            if plan == False:
                messages.error(request, 'El plan de ejercicio no se ha modificado correctamente')
            else:
                messages.success(request, 'El plan de ejercicio se ha modificado correctamente')
            return HttpResponseRedirect(reverse('Medico-ejercicio-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        medico = MedicoHelper(request.user)

        heartRate = medico.getRitmoCardiaco(cod_paciente)
        if heartRate == None:
            messages.error(request, 'Por favor registre un valor en la variable: Ritmo cardíaco')
            return HttpResponseRedirect(reverse('Medico-ejercicio-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            heartRate = heartRate.valor
        glucose = medico.getGlucosa(cod_paciente)
        if glucose == None:
            messages.error(request, 'Por favor registre un valor en la variable: Nivel de glucosa')
            return HttpResponseRedirect(reverse('Medico-ejercicio-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            glucose = glucose.valor
        height = medico.getAltura(cod_paciente)
        if height == None:
            messages.error(request, 'Por favor registre un valor en la variable: Altura')
            return HttpResponseRedirect(reverse('Medico-ejercicio-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            height = height.valor
        weight = medico.getPeso(cod_paciente)
        if weight == None:
            messages.error(request, 'Por favor registre un valor en la variable: Peso')
            return HttpResponseRedirect(reverse('Medico-ejercicio-index', kwargs={'cod_paciente': cod_paciente}))
        else:
            weight = weight.valor
        age = medico.getEdad(cod_paciente)
        
        content = medico.getMemoryOrContentExe(cod_paciente)
        plan = None
        context = {}
        context['diseases'] = None
        if content:
            hr = HybridRecommender()
            result = hr.predictExercise(heartRate,glucose,height,weight,age)
            plan = medico.guardarRecomendacionEjercicio(result['recommendations'],cod_paciente)
            context['diseases'] = result['diseases']
        else:
            plan = medico.getMemoryRecommendationExercise(cod_paciente)
            if plan == None:
                hr = HybridRecommender()
                result = hr.predictExercise(heartRate,glucose,height,weight,age)
                plan = medico.guardarRecomendacionEjercicio(result['recommendations'],cod_paciente)
                context['diseases'] = result['diseases']
        
        paciente = medico.getPaciente(cod_paciente)
        context['paciente'] = paciente
        context['plan'] = plan
        context['heartRate'] = heartRate
        context['glucose'] = glucose
        context['height'] = height
        context['weight'] = weight
        context['age'] = age
        context['nueva'] = True
        context['imagen'] = Tools.getEjercicioImg(plan.ejercicio)
        Tools.auditar(request,f'Se ha generado un nuevo plan de ejercicio para {paciente.user.username}')
        return render(request,'fynex_app/medico/exercise_recommendations_generation.html',context)
    
def medico_detail_ejercicio(request,cod_paciente,cod_plan):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente) or not verify_planEjercicio(request,cod_paciente,cod_plan):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        medico = MedicoHelper(request.user)
        if 'save' in request.POST:
            id_p = request.POST['id']
            rating = request.POST['rate'] if 'rate' in request.POST else 0
            estado = "A" if 'estado' in request.POST else "I"
            plan = medico.modificarPlanEjercicio(id_p,rating,estado)
            if plan == False:
                messages.error(request, 'El plan de ejercicio no se ha modificado correctamente')
            else:
                messages.success(request, 'El plan de ejercicio se ha modificado correctamente')
            return HttpResponseRedirect(reverse('Medico-ejercicio-index', kwargs={'cod_paciente': cod_paciente}))
    else:
        medico = MedicoHelper(request.user)
        context = {}
        plan = medico.getPlanEjercicio(cod_plan)
        context['paciente'] = medico.getPaciente(cod_paciente)
        context['plan'] = plan
        context['imagen'] = Tools.getEjercicioImg(plan.ejercicio)
        return render(request,'fynex_app/medico/exercise_recommendations_generation.html',context)

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
        
        content = medico.getMemoryOrContentNutri(cod_paciente)
        plan = None
        context = {}
        context['diseases'] = None
        if content:
            hr = HybridRecommender()
            result = hr.predictNutrition(heartRate,glucose,height,weight,age)
            
            plan = medico.guardarRecomendacionNutricion(result['recommendations'],result['diff'],cod_paciente)
            context['diseases'] = result['diseases']
        else:
            plan = medico.getMemoryRecommendationNutrition(cod_paciente)
            if plan == None:
                hr = HybridRecommender()
                result = hr.predictNutrition(heartRate,glucose,height,weight,age)
                
                plan = medico.guardarRecomendacionNutricion(result['recommendations'],result['diff'],cod_paciente)
                context['diseases'] = result['diseases']

        paciente = medico.getPaciente(cod_paciente)
        context['paciente'] = paciente
        context['plan'] = plan
        partes = medico.getPartesDePlanNutricional(plan)
        res = {}
        totals_proteinas = json.loads(plan.dif_proteinas)
        totals_carbohidratos = json.loads(plan.dif_carbohidratos)
        totals_grasas = json.loads(plan.dif_grasas)
        for x in partes:
            if not x.parte in res:
                res[x.parte] = {}
                res[x.parte]['totals'] = {'proteinas':totals_proteinas[x.parte],'carbohidratos':totals_carbohidratos[x.parte],'grasas':totals_grasas[x.parte]}
                res[x.parte]['objects'] = []
            res[x.parte]['objects'].append(x)
        context['partes'] = res
        context['heartRate'] = heartRate
        context['glucose'] = glucose
        context['height'] = height
        context['weight'] = weight
        context['age'] = age
        context['nueva'] = True
        Tools.auditar(request,f'Se ha generado un nuevo plan de nutrición para {paciente.user.username}')
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
        partes = medico.getPartesDePlanNutricional(plan)
        res = {}
        totals_proteinas = json.loads(plan.dif_proteinas)
        totals_carbohidratos = json.loads(plan.dif_carbohidratos)
        totals_grasas = json.loads(plan.dif_grasas)
        for x in partes:
            if not x.parte in res:
                res[x.parte] = {}
                res[x.parte]['totals'] = {'proteinas':totals_proteinas[x.parte],'carbohidratos':totals_carbohidratos[x.parte],'grasas':totals_grasas[x.parte]}
                res[x.parte]['objects'] = []
            res[x.parte]['objects'].append(x)
        context['partes'] = res

        return render(request,'fynex_app/medico/nutrition_recommendations_generation.html',context)




def medico_chat(request, cod_paciente):
    if not verify_auth(request,'medico') or not verify_paciente(request,cod_paciente):
        return HttpResponseRedirect(reverse('Fynex-index'))
    
    medico = MedicoHelper(request.user)
    paciente = medico.getPaciente(cod_paciente)
    mensajesHelper = MensajeHelper()
    mensajes = mensajesHelper.getMensajesMedico(request.user,paciente)
    return render(request, 'fynex_app/chat.html', {
        'room_name': str(cod_paciente),
        'sender_name' : request.user.first_name,
        'receiver_name' : paciente.user.first_name,
        'paciente_sender' : False,
        'mensajes' : mensajes,
        'is_paciente' : False 
    })

def paciente_chat(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    
    pacienteHelper = PacienteHelper(request.user)
    paciente = pacienteHelper.paciente
    mensajesHelper = MensajeHelper()
    mensajes = mensajesHelper.getMensajesPaciente(request.user)
    return render(request, 'fynex_app/chat.html', {
        'room_name': str(paciente.id),
        'sender_name' : paciente.user.first_name,
        'receiver_name' : paciente.medico.user.first_name,
        'paciente_sender' : True,
        'mensajes' : mensajes,
        'is_paciente' : True 
    })

def admin_perfil(request):
    if not verify_auth(request,'administrator'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        if 'pass' in request.POST:
            curr_pass = request.POST['current_password']
            new_pass = request.POST['new_password']
            new_pass2 = request.POST['new_password2']
            if new_pass!=new_pass2:
                messages.error(request, 'Las contraseñas no coinciden')
                return HttpResponseRedirect(reverse('Administrator-perfil'))
            if not Tools.checkPassword(new_pass):
                messages.error(request, 'La contraseña no cumple con las reglas definidas')
                return HttpResponseRedirect(reverse('Administrator-perfil'))
            if request.user.check_password(curr_pass):
                try:
                    request.user.set_password(new_pass)
                    request.user.save()
                    messages.success(request, 'La contraseña ha sido modificada con éxito')
                    return HttpResponseRedirect(reverse('Administrator-perfil'))
                except:
                    messages.error(request, 'Ha ocurrido un error')
                    return HttpResponseRedirect(reverse('Administrator-perfil'))
            else:
                messages.error(request, 'La contraseña actual es incorrecta')
                return HttpResponseRedirect(reverse('Administrator-perfil'))
    else:
        context = {}
        admin = Administrator(request.user)
        context['user'] = admin.user
        return render(request,'fynex_app/administrator/administrator_perfil.html',context)

def centro_perfil(request):
    if not verify_auth(request,'centro_medico'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        if 'pass' in request.POST:
            curr_pass = request.POST['current_password']
            new_pass = request.POST['new_password']
            new_pass2 = request.POST['new_password2']
            if new_pass!=new_pass2:
                messages.error(request, 'Las contraseñas no coinciden')
                return HttpResponseRedirect(reverse('CentroMedico-perfil'))
            if not Tools.checkPassword(new_pass):
                messages.error(request, 'La contraseña no cumple con las reglas definidas')
                return HttpResponseRedirect(reverse('CentroMedico-perfil'))
            if request.user.check_password(curr_pass):
                try:
                    request.user.set_password(new_pass)
                    request.user.save()
                    messages.success(request, 'La contraseña ha sido modificada con éxito')
                    return HttpResponseRedirect(reverse('CentroMedico-perfil'))
                except:
                    messages.error(request, 'Ha ocurrido un error')
                    return HttpResponseRedirect(reverse('CentroMedico-perfil'))
            else:
                messages.error(request, 'La contraseña actual es incorrecta')
                return HttpResponseRedirect(reverse('CentroMedico-perfil'))
    else:
        context = {}
        centroHelper = CentroMedicoHelper(request.user)
        context['centro'] = centroHelper.centro
        return render(request,'fynex_app/centro_medico/centro_perfil.html',context)

def medico_perfil(request):
    if not verify_auth(request,'medico'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        if 'pass' in request.POST:
            curr_pass = request.POST['current_password']
            new_pass = request.POST['new_password']
            new_pass2 = request.POST['new_password2']
            if new_pass!=new_pass2:
                messages.error(request, 'Las contraseñas no coinciden')
                return HttpResponseRedirect(reverse('Medico-perfil'))
            if not Tools.checkPassword(new_pass):
                messages.error(request, 'La contraseña no cumple con las reglas definidas')
                return HttpResponseRedirect(reverse('Medico-perfil'))
            if request.user.check_password(curr_pass):
                try:
                    request.user.set_password(new_pass)
                    request.user.save()
                    messages.success(request, 'La contraseña ha sido modificada con éxito')
                    return HttpResponseRedirect(reverse('Medico-perfil'))
                except:
                    messages.error(request, 'Ha ocurrido un error')
                    return HttpResponseRedirect(reverse('Medico-perfil'))
            else:
                messages.error(request, 'La contraseña actual es incorrecta')
                return HttpResponseRedirect(reverse('Medico-perfil'))
    else:
        context = {}
        medicoHelper = MedicoHelper(request.user)
        context['medico'] = medicoHelper.medico
        return render(request,'fynex_app/medico/medico_perfil.html',context)


def paciente_index(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        if 'pass' in request.POST:
            curr_pass = request.POST['current_password']
            new_pass = request.POST['new_password']
            new_pass2 = request.POST['new_password2']
            if new_pass!=new_pass2:
                messages.error(request, 'Las contraseñas no coinciden')
                return HttpResponseRedirect(reverse('Paciente-index'))
            if not Tools.checkPassword(new_pass):
                messages.error(request, 'La contraseña no cumple con las reglas definidas')
                return HttpResponseRedirect(reverse('Paciente-index'))
            if request.user.check_password(curr_pass):
                try:
                    request.user.set_password(new_pass)
                    request.user.save()
                    messages.success(request, 'La contraseña ha sido modificada con éxito')
                    return HttpResponseRedirect(reverse('Paciente-index'))
                except:
                    messages.error(request, 'Ha ocurrido un error')
                    return HttpResponseRedirect(reverse('Paciente-index'))
            else:
                messages.error(request, 'La contraseña actual es incorrecta')
                return HttpResponseRedirect(reverse('Paciente-index'))
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
    partes = pacienteHelper.getPartesDePlanNutricional(plan)
    res = {}
    totals_proteinas = json.loads(plan.dif_proteinas)
    totals_carbohidratos = json.loads(plan.dif_carbohidratos)
    totals_grasas = json.loads(plan.dif_grasas)
    for x in partes:
        if not x.parte in res:
            res[x.parte] = {}
            res[x.parte]['totals'] = {'proteinas':totals_proteinas[x.parte],'carbohidratos':totals_carbohidratos[x.parte],'grasas':totals_grasas[x.parte]}
            res[x.parte]['objects'] = []
        res[x.parte]['objects'].append(x)
    context['partes'] = res
    return render(request,'fynex_app/paciente/nutrition_recommendations_generation.html',context)

def paciente_variables(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        pacienteHelper = PacienteHelper(request.user)
        context['paciente'] = pacienteHelper.paciente
        vars = {}
        variables = pacienteHelper.getVariablesSeguimiento()
        for v in variables:
            historico = pacienteHelper.getHistoricoVariable(v.id)
            values = []
            dates = []
            for h in historico:
                values.append(h.valor)
                dates.append(str(h.fecha))
            vars[v.nombre] = [values,dates,v.unidad]
        context['variables'] = vars
        context['is_medico'] = False
        return render(request,'fynex_app/grafico_variables.html',context)

def paciente_examenes(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        paciente = PacienteHelper(request.user)
        if 'file' in request.POST:
            try:
                file = request.FILES['myfile']
                contents = ['application/pdf','image/png','image/jpeg','image/jpg']
                if file.content_type in contents:
                    exten = (file._name).split('.')
                    id_prev = request.POST['id']
                    if file.size > 15728640:
                        messages.error(request, 'El límite de tamaño del archivo es de 15 MB')
                        return HttpResponseRedirect(reverse('Paciente-examenes-index'))
                    file_content = file.read()
                    key = f'Fynex_{id_prev}_{paciente.paciente.documento_identificacion}.{exten[len(exten)-1]}'
                    Tools.cos_upload.put_object(Body=file_content,Bucket='fynex',Key=str(key))
                    examen = paciente.subirArchivo(id_prev,key)
                    if examen == None:
                        messages.error(request, 'El examen no se ha subido correctamente')
                    else:
                        Tools.auditar(request,f'Se ha subido un exámen {paciente.paciente.user.username}')
                        messages.success(request, 'El examen se ha subido correctamente')
                    return HttpResponseRedirect(reverse('Paciente-examenes-index'))
                else:
                    messages.error(request, 'Solo se aceptan imagenes PNG, JEPG, JPG o archivos PDF')
                    return HttpResponseRedirect(reverse('Paciente-examenes-index'))
            except:
                messages.success(request, 'El examen no se ha subido correctamente')
                return HttpResponseRedirect(reverse('Paciente-examenes-index'))
    else:
        context = {}
        paciente = PacienteHelper(request.user)
        context['examenes'] = paciente.getExamenes()
        return render(request,'fynex_app/paciente/examenes.html',context)
def paciente_nueva_nutricion(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    try:
        paciente = PacienteHelper(request.user)
        Tools.sendEmailNewRecommendationFood(paciente.paciente)
        messages.success(request, 'Solicitud realizada')
    except:
        messages.error(request, 'Ha ocurrido un error')
    return HttpResponseRedirect(reverse('Paciente-nutrition-index'))

def paciente_ejercicio(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        context = {}
        paciente = PacienteHelper(request.user)
        context['paciente'] = paciente.paciente
        context['planes'] = paciente.getPlanesEjercicio()
        return render(request,'fynex_app/paciente/exercise_recommendations_index.html',context)

def paciente_detail_ejercicio(request,cod_plan):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method == 'POST':
        pass
    else:
        pacienteHelper = PacienteHelper(request.user)
        paciente = pacienteHelper.paciente
        context = {}
        plan = pacienteHelper.getPlanEjercicio(cod_plan)
        if plan==None:
            return HttpResponseRedirect(reverse('Fynex-index'))
        context['paciente'] = paciente
        context['plan'] = plan
        context['imagen'] = Tools.getEjercicioImg(plan.ejercicio)
        return render(request,'fynex_app/paciente/exercise_recommendations_generation.html',context)

def paciente_nueva_ejercicio(request):
    if not verify_auth(request,'paciente'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    try:
        paciente = PacienteHelper(request.user)
        Tools.sendEmailNewRecommendationExercise(paciente.paciente)
        messages.success(request, 'Solicitud realizada')
    except:
        messages.error(request, 'Ha ocurrido un error')
    return HttpResponseRedirect(reverse('Paciente-ejercicio-index'))