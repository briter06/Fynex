from ..models import Medico
from ..models import Paciente
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pandas as pd

class MedicoHelper:

    def __init__(self,user):
        self.medico = Medico.objects.all().get(user=user)
    
    def registrar_paciente(self,username,password,first_name,fecha_nacimiento,documento_identificacion,telefono):
        try:
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = ""
            paciente = Paciente()
            paciente.user = user
            paciente.fecha_nacimiento = fecha_nacimiento
            paciente.documento_identificacion = documento_identificacion
            paciente.telefono = telefono
            paciente.medico = self.medico
            group = Group.objects.get(name='paciente') 
            user.save()
            paciente.save()
            group.user_set.add(user)
            return paciente
        except Exception as e:
            return None
    def modificar_paciente(self,username,newusername,first_name,fecha_nacimiento,documento_identificacion,telefono):
        try:
            user = User.objects.get(username=username)
            paciente = Paciente.objects.get(user=user) 
            user.username = newusername
            user.first_name = first_name
            paciente.fecha_nacimiento = fecha_nacimiento
            paciente.documento_identificacion = documento_identificacion
            paciente.telefono = telefono
            user.save()
            paciente.save()
            return paciente
        except:
            return None
    def eliminar_paciente(self,username):
        try:
            user = User.objects.get(username=username)
            paciente = Paciente.objects.get(user=user)
            paciente.delete()
            user.delete()
            return True
        except:
            return False
    
    def getPacientes(self):
        res = Paciente.objects.all().filter(medico=self.medico)
        return res

    def getPaciente(self,cod_paciente):
        res = Paciente.objects.all().get(pk=cod_paciente)
        return res

    def verifyPaciente(self,cod_paciente):
        res = Paciente.objects.all().filter(medico=self.medico,pk=cod_paciente)
        return res