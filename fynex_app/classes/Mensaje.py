from ..models import Mensaje
from ..models import Paciente
from ..models import Medico
import pandas as pd
from .tools import Tools


class MensajeHelper:

    def agregarMensaje(self,message,paciente,paciente_sender):
        try:
            mensaje = Mensaje()
            mensaje.mensaje = message
            mensaje.fecha = Tools.getToday(True)
            mensaje.paciente = paciente
            mensaje.medico = paciente.medico
            mensaje.paciente_emisor = paciente_sender
            mensaje.notificado_email = False
            mensaje.save()
            return mensaje
        except:
            return None
    def getPaciente(self,cod_paciente):
        paciente = Paciente.objects.all().get(pk=cod_paciente)
        return paciente
    
    def getMensajesMedico(self,user,paciente):
        medico = Medico.objects.all().get(user=user)
        mensajes = Mensaje.objects.all().filter(medico=medico,paciente=paciente).order_by('-fecha')
        return mensajes
    def getMensajesPaciente(self,user):
        paciente = Paciente.objects.all().get(user=user)
        mensajes = Mensaje.objects.all().filter(paciente=paciente).order_by('-fecha')
        return mensajes
