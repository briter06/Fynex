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
    def sendEmailUserAdded(user,password):
        subject = 'Bienvenido - Fynex'
        body = f'''
                <div style="align-content: center;margin: auto auto;width: 100%;text-align: center">
                    <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" align="center" width="500">
                    <br>
                    <br>
                    <h1><strong>Bienvenido</strong><br></h1>
                    <h1><strong style="color:#1C54F7"><font font="verdana"><i><b>{user.first_name}</b></i></font></strong><br><br></h1>
                    <br>
                    Su correo es: <br>
                    <font font="verdana"><i><b>{user.username}</b></i></font>
                    <br>
                    La contraseña temporal que ha sido asignada es :  <br>
                    <strong style="color:#5178EC"><i>{password}</i></strong><br></h2>
                    <br>
                   <h2>Cuando inicie sesión podrá modificar la contraseña a la que desee.<h2>
                    <br>
                    <br>
                    <a href="https://fynexapp.herokuapp.com"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a>
                    <br>
                </div>

            '''
        res = Tools.sendEmail(user,subject,body)
        return res

    @staticmethod
    def sendEmailUserPasswd(user):
        subject = 'Recuperar contraseña'
        body = f'''
             <div style="align-content: center;margin: auto auto;width: 100%;text-align: center">
                    <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" align="center" width="500">
                    <br>
                    <br>
                    <h1><strong>Recuperar contraseña</strong><br></h1>
                    <h1><strong style="color:#1C54F7"><font font="verdana"><i><b>{user.first_name}</b></i></font></strong><br><br></h1>
                    <br>
                    Su correo es: <br>
                    <font font="verdana"><i><b>{user.username}</b></i></font>
                    <br>
                    La contraseña de se cuenta es :  <br>
                    <strong style="color:#5178EC"><i>{user.password}</i></strong><br></h2>
                    <br>
                    <br>
                    <a href="https://fynexapp.herokuapp.com"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a>
                    <br>
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
                <div style="align-content: center;margin: auto auto;width: 100%;text-align: center">
                    <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" align="center" width="500">
                    <br>
                    <br>
                    <h1><strong style="color:#1C54F7"><font font="verdana"><i><b>Nuevos Mensajes</b></i></font></strong><br><br></h1>
                    <br>
                    <h3>Tienes nuevos mensajes de tu '''+tipo+'''.</h3> <br>
                    <a href="'''+url+'''"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ir al chat</button></a>
                    <br>
                </div>

            '''
        res = Tools.sendEmail(enviar_a,subject,body)
        return res

    @staticmethod
    def sendEmailNewRecommendationFood(paciente):
        subject = 'Solicitud de nueva recomendación'
        body = f'''
                <div style="align-content: center;margin: auto auto;width: 100%;text-align: center">
                    <img src="https://fynexapp.herokuapp.com/static/images/banner.jpg" align="center" width="500">
                    <br>
                    <br>
                    <h1><strong style="color:#1C54F7"><font font="verdana"><i><b>Nueva recomendación</b></i></font></strong><br><br></h1>
                    <br>
                    <h3>El paciente {paciente.user.first_name} desea una nueva recomendación nutricional</h3> <br>
                    <a href="https://fynexapp.herokuapp.com/Medico/{paciente.id}/nutrition_recommendations"><button style="border-radius: 12px;font-size: 25px;background-color: #125570;color:white">Ingresar</button></a>
                    <br>
                </div>

            '''
        res = Tools.sendEmail(paciente.medico.user,subject,body)
        return res
