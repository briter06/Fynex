from ..models import Mensaje
from ..models import Paciente
from ..models import Medico
import pandas as pd
from .tools import Tools


class MensajeHelper:


    def verify_email(self,fech,paciente,paciente_sender):
        last_m = Mensaje.objects.all().filter(notificado_email=True,paciente=paciente,paciente_emisor=paciente_sender).order_by('-fecha').first()
        if last_m is None:
            Tools.sendEmailUserMsg(paciente,paciente_sender)
            return True
        else:
            diff = fech - last_m.fecha
            hours = (diff.total_seconds()/60)/60
            if hours > 12:
                Tools.sendEmailUserMsg(paciente,paciente_sender)
                return True
        return False
    def agregarMensaje(self,message,paciente,paciente_sender,fecha):
        try:
            fech = Tools.getTodayStr(fecha)
            notificado_email = self.verify_email(fech,paciente,paciente_sender)
            mensaje = Mensaje()
            mensaje.mensaje = message
            mensaje.fecha = fech
            mensaje.paciente = paciente
            mensaje.paciente_emisor = paciente_sender
            mensaje.notificado_email = notificado_email
            mensaje.save()
            return mensaje
        except:
            return None
    def getPaciente(self,cod_paciente):
        paciente = Paciente.objects.all().get(pk=cod_paciente)
        return paciente
    
    def getMensajesMedico(self,user,paciente):
        mensajes = Mensaje.objects.all().filter(paciente=paciente).order_by('-fecha')
        return mensajes
    def getMensajesPaciente(self,user):
        paciente = Paciente.objects.all().get(user=user)
        mensajes = Mensaje.objects.all().filter(paciente=paciente).order_by('-fecha')
        return mensajes
