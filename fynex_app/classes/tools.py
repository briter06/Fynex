from django.core.mail import EmailMessage
import random
import string
from django.conf import settings

class Tools:

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
        body = '''
            <h1>Fynex Health</h1></br>
            <strong>Usuario:</strong> <p> '''+user.username+'''</p></br>
            <strong>Contraseña temporal:</strong> <p> '''+password+'''</p></br>
            '''
        res = Tools.sendEmail(user,password,subject,body)
        return res

