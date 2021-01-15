from django.core.mail import EmailMessage
import random
import string
from django.conf import settings
import ibm_boto3
from ibm_botocore.client import Config, ClientError

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
    def sendEmail(user,password,subject, body):
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
            <h1>Fynex Health</h1></br>
            <strong>Usuario:</strong> <p> {user.username} </p></br>
            <strong>Contraseña temporal:</strong> <p> {password} </p></br>
            '''
        res = Tools.sendEmail(user,password,subject,body)
        return res

