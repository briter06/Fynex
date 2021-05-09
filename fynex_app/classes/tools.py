from django.core.mail import EmailMessage
import random
import string
from django.conf import settings
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from django.templatetags.static import static
from django.conf import settings
import pytz
import datetime
from django.contrib.auth.models import User
from ..models import Auditoria
import re

class Tools:

    cos_download = ibm_boto3.resource("s3",
        ibm_api_key_id=settings.COS_API_KEY_ID,
        ibm_service_instance_id=settings.COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=settings.COS_ENDPOINT
    )
    cos_upload = ibm_boto3.client("s3",
        ibm_api_key_id=settings.COS_API_KEY_ID,
        ibm_service_instance_id=settings.COS_INSTANCE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=settings.COS_ENDPOINT
    )

    data_ejercicio = {
        'Cicla elíptica':'clica_eliptica', #Listo
        'Cicla estática' : 'cicla_estatica', #Listo
        'Caminadora':'caminadora', #Listo
        'Caminar':'caminar', #Listo
        'Cicla':'cicla', #Listo
        'Correr':'correr', #Listo
        'Patinar':'patinar', #Listo
        'Nadar':'nadar', #Listo
        'Saltar cuerda' : 'cuerda', #Listo
        'Baile aeróbico' : 'baile_aerobico', #Listo
        'Aeróbicos acuáticos' : 'aerobico_acuatico', #Listo
        'Yoga':'yoga' #Yoga
    }

    @staticmethod
    def checkPassword(password):
        rgx = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?!.* ).{8,}')
        return rgx.fullmatch(password) and len(password) >= 8

    @staticmethod
    def auditar(request,descripcion):
        try:
            audit = Auditoria()
            audit.fecha = Tools.getToday(time=True)
            audit.descripcion = descripcion
            audit.direccion_ip = Tools.get_client_ip(request)
            audit.correo_usuario = request.user.username
            audit.tipo_usuario = request.user.groups.first()
            audit.save()
        except Exception as e:
            print(e)
            pass
    
    @staticmethod
    def getAuditoria():
        return Auditoria.objects.all().order_by('-fecha')
    
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def getEjercicioImg(ejercicio):
        try:
            return Tools.data_ejercicio[ejercicio]
        except:
            return 'defecto'

    @staticmethod
    def getUser(email):
        try:
            return User.objects.all().get(username=email)
        except:
            return None
    
    @staticmethod
    def recuperarClave(user):
        new_pass = Tools.get_random_string(10)
        user.set_password(new_pass)
        user.save()
        Tools.sendEmailUserPasswd(user,new_pass)

    @staticmethod
    def getPercentage(x,dec):
        return round(x*100,dec)

    @staticmethod
    def getToday(time=False):
        date = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
        if time:
            return date
        else:
            return date.date()
    
    @staticmethod
    def getTodayStr(str_date):
        dat = datetime.datetime.strptime(str_date,'%Y-%m-%dT%H:%M:%S.%fZ')
        utc_now = pytz.utc.localize(dat)
        pst_now = utc_now.astimezone(pytz.timezone(settings.TIME_ZONE))
        return pst_now
    

    @staticmethod
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    
    @staticmethod
    def sendEmail(user,subject, body):
        try:
            email = EmailMessage(
                subject, body,from_email=settings.DEFAULT_FROM_EMAIL, to=[user.username])
            email.content_subtype = "html"
            email.send()
            return True
        except:
            return False
    @staticmethod
    def sendEmailRaw(email,subject, body):
        try:
            email = EmailMessage(
                subject, body,from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
            email.content_subtype = "html"
            email.send()
            return True
        except:
            return False
    @staticmethod
    def sendEmailUserAdded(user,password):
        subject = 'Bienvenido - Fynex'
        body = f'''
                <div style="width:100%;background-color:#D5D5D5;padding-top: 30px;padding-bottom: 30px;">
                    <div style="width: 500px;margin: auto auto;background-color:white;border-style: double;">
                        <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" style="width: 100%" align="left">
                        <br>
                        <br><br><br><br>
                        <h1><strong style="color:#1C54F7"><font font="verdana"><i><b><p align="center">Bienvenido {user.first_name}</b></i></font></strong></h1></p>
                        <div style="width:100%;text-align:center">
                            <img src="https://i.pinimg.com/originals/7e/69/ec/7e69eca344ca1465da94d698ded08e8e.gif" width="200">
                        </div>
                        <h3><p align="center">
                            Su correo es: <br>
                            <font font="verdana"><i><b>{user.username}</b></i></font>
                        </p></h3>

                        <h3><p align="center">
                            La contraseña temporal que ha sido asignada es :  <br>
                            <strong style="color:#5178EC"><i>{password}</i></strong>
                        </p></h3>
                        <h3 align="center">Cuando inicie sesión podrá modificar la contraseña a la que desee.<h3>
                        <p align="center"><a href="https://fynexapp.herokuapp.com"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a> </p>
                        <br>
                    </div>
                </div>
            '''
        res = Tools.sendEmail(user,subject,body)
        return res

    @staticmethod
    def sendEmailUserPasswd(user,new_pass):
        subject = 'Recuperar contraseña'
        body = f'''
             <div style="width:100%;background-color:#D5D5D5;padding-top: 30px;padding-bottom: 30px;">
                <div style="width: 500px;margin: auto auto;background-color:white;border-style: double;">
                    <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" style="width: 100%" align="left">
                    <br>
                    <br><br><br><br>
                    <h1><strong style="color:#1C54F7"><font font="verdana"><i><b><p align="center">Recuperar contraseña</b></i></font></strong></h1></p>
                    <div style="width:100%;text-align:center">
                        <img src="https://i.pinimg.com/originals/7e/69/ec/7e69eca344ca1465da94d698ded08e8e.gif" width="200">
                    </div>
                    <h3><p align="center">
                        Su correo es: <br>
                        <font font="verdana"><i><b>{user.username}</b></i></font>
                    </p></h3>

                    <h3><p align="center">
                        La nueva contraseña de su cuenta es :  <br>
                        <strong style="color:#5178EC"><i>{new_pass}</i></strong>
                    </p></h3>
                    <p align="center"><a href="https://fynexapp.herokuapp.com"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a> </p>
                    <br>
                </div>
            </div>
            '''
        res = Tools.sendEmail(user,subject,body)
        return res

    @staticmethod
    def sendEmailUserMsg(paciente,paciente_sender):
        subject = 'Nuevo mensaje'
        url = 'https://fynexapp.herokuapp.com/Paciente/chat'
        tipo = f'médico <strong>{paciente.medico.user.first_name}</strong>'
        enviar_a = paciente.user
        if paciente_sender:
            tipo = f'paciente <strong>{paciente.user.first_name}</strong>'
            url = f'https://fynexapp.herokuapp.com/Medico/{paciente.id}/chat'
            enviar_a = paciente.medico.user
        body = f'''
                <div style="width:100%;background-color:#D5D5D5;padding-top: 30px;padding-bottom: 30px;">
                    <div style="width: 500px;margin: auto auto;background-color:white;border-style: double;">
                        <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" style="width: 100%" align="left">
                        <br>
                        <br><br><br><br>
                        <h1><strong style="color:#1C54F7"><font font="verdana"><i><b><p align="center">Tienes una nueva notificación</b></i></font></strong></h1></p>
                        <div style="width:100%;text-align:center">
                            <img src="https://i.pinimg.com/originals/7e/69/ec/7e69eca344ca1465da94d698ded08e8e.gif" width="200">
                        </div>
                        <h3><p align="center"> Tienes un nuevo mensaje de tu '''+tipo+'''.</p></h3> <br>
                        <p align="center"><a href="'''+url+'''"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ir al chat</button></a></p>
                        <br>
                    </div>
                </div>
            '''
        res = Tools.sendEmail(enviar_a,subject,body)
        return res

    @staticmethod
    def sendEmailNewRecommendationFood(paciente):
        subject = 'Solicitud de nueva recomendación nutricional'
        body = f'''
                <div style="width:100%;background-color:#D5D5D5;padding-top: 30px;padding-bottom: 30px;">
                    <div style="width: 500px;margin: auto auto;background-color:white;border-style: double;">
                        <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" style="width: 100%" align="left">
                        <br>
                        <br><br><br><br>
                        <h1><strong style="color:#1C54F7"><font font="verdana"><i><b><p align="center">Nueva recomendación</b></i></font></strong></h1></p>
                        <div style="width:100%;text-align:center">
                            <img src="https://i.pinimg.com/originals/7e/69/ec/7e69eca344ca1465da94d698ded08e8e.gif" width="200">
                        </div>
                        <h3><p align="center">
                            El paciente {paciente.user.first_name} desea una nueva recomendación nutricional
                        </p></h3>
                        <p align="center"><a href="https://fynexapp.herokuapp.com/Medico/{paciente.id}/nutrition_recommendations"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a></p>
                        <br>
                    </div>
                </div>
            '''
        res = Tools.sendEmail(paciente.medico.user,subject,body)
        return res
    
    @staticmethod
    def sendEmailNewRecommendationExercise(paciente):
        subject = 'Solicitud de nueva recomendación de ejercicio'
        body = f'''
                <div style="width:100%;background-color:#D5D5D5;padding-top: 30px;padding-bottom: 30px;">
                    <div style="width: 500px;margin: auto auto;background-color:white;border-style: double;">
                        <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" style="width: 100%" align="left">
                        <br>
                        <br><br><br><br>
                        <h1><strong style="color:#1C54F7"><font font="verdana"><i><b><p align="center">Nueva recomendación</b></i></font></strong></h1></p>
                        <div style="width:100%;text-align:center">
                            <img src="https://i.pinimg.com/originals/7e/69/ec/7e69eca344ca1465da94d698ded08e8e.gif" width="200">
                        </div>
                        <h3><p align="center">
                            El paciente {paciente.user.first_name} desea una nueva recomendación de actividad física
                        </p></h3>
                        <p align="center"><a href="https://fynexapp.herokuapp.com/Medico/{paciente.id}/exercise_recommendations"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a></p>
                        <br>
                    </div>
                </div>
            '''
        res = Tools.sendEmail(paciente.medico.user,subject,body)
        return res
    
    @staticmethod
    def sendInformacion(email):
        subject = 'Fynex'
        body = f'''
                <div style="width:100%;background-color:#D5D5D5;padding-top: 30px;padding-bottom: 30px;">
                    <div style="width: 500px;margin: auto auto;background-color:white;border-style: double;">
                        <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" style="width: 100%" align="left">
                        <br>
                        <br><br><br><br>
                        <h1><strong style="color:#1C54F7"><font font="verdana"><i><b><p align="center">Fynex</b></i></font></strong></h1></p>
                        <div style="width:100%;text-align:center">
                            <img src="https://i.pinimg.com/originals/7e/69/ec/7e69eca344ca1465da94d698ded08e8e.gif" width="200">
                        </div>
                        <p align="center">
                            Fynex es una aplicación que ayuda a la prevención y tratamiento de enfermedades basadas en trastornos alimenticios, ofreciendo planes nutricionales y planes de actividad física. Además, ofrece un seguimiento personalizado a los pacientes, al disponer de funcionalidades gráficas y de comunicación como un chat de mensajería.<br><br>
                            Para mayor información, comunicarse con <a href="mailto:fynexhealth@gmail.com">fynexhealth@gmail.com</a>
                        </p>
                        <p align="center"><a href="https://fynexapp.herokuapp.com"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a></p>
                        <br>
                    </div>
                </div>
            '''
        res = Tools.sendEmailRaw(email,subject,body)
        return res
    
    @staticmethod
    def sendEmailNuevoExamen(paciente,examen):
        subject = 'Nuevo resultado de examen'
        body = f'''
                <div style="width:100%;background-color:#D5D5D5;padding-top: 30px;padding-bottom: 30px;">
                    <div style="width: 500px;margin: auto auto;background-color:white;border-style: double;">
                        <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" style="width: 100%" align="left">
                        <br>
                        <br><br><br><br>
                        <h1><strong style="color:#1C54F7"><font font="verdana"><i><b><p align="center">Nuevo resultado</b></i></font></strong></h1></p>
                        <div style="width:100%;text-align:center">
                            <img src="https://i.pinimg.com/originals/7e/69/ec/7e69eca344ca1465da94d698ded08e8e.gif" width="200">
                        </div>
                        <h3><p align="center">
                            El paciente {paciente.user.first_name} ha subido el resultado del examen: <b>{examen.nombre}</b>
                        </p></h3>
                        <p align="center"><a href="https://fynexapp.herokuapp.com/Medico/{paciente.id}/examenes"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ver examenes</button></a></p>
                        <br>
                    </div>
                </div>
            '''
        res = Tools.sendEmail(paciente.medico.user,subject,body)
        return res