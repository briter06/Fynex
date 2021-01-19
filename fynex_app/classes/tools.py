from django.core.mail import EmailMessage
import random
import string
from django.conf import settings
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from django.templatetags.static import static

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

            <img src="{static('images/banner.jpg')}" align="center">
            <br>
            <br>
            Bienvenido a Fynex {user.username}<br>
            <br>
            La contraseña temporal que ha sido asignada es : {password} <br>
            <br>
            Cuando inicie sesión podrá modificar la contraseña a la que desee.
            <br>
            <br>



            '''
        res = Tools.sendEmail(user,subject,body)
        return res

