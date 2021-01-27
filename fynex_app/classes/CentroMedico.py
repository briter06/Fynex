from ..models import Medico
from ..models import CentroMedico
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pandas as pd
from .tools import Tools

class CentroMedicoHelper:

    def __init__(self,user):
        self.centro = CentroMedico.objects.all().get(user=user)
    
    def registrar_medico(self,username,password,first_name,documento_identificacion,especialidad,telefono):
        try:
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = ""
            medico = Medico()
            medico.user = user
            medico.documento_identificacion = documento_identificacion
            medico.especialidad = especialidad
            medico.telefono = telefono
            medico.centro_medico = self.centro
            group = Group.objects.get(name='medico') 
            user.save()
            medico.save()
            group.user_set.add(user)
            res = Tools.sendEmailUserAdded(user,password)
            return medico
        except Exception as e:
            return None
    def modificar_medico(self,username,newusername,first_name,documento_identificacion,especialidad,telefono):
        try:
            user = User.objects.get(username=username)
            medico = Medico.objects.get(user=user) 
            user.username = newusername
            user.first_name = first_name
            medico.documento_identificacion = documento_identificacion
            medico.especialidad = especialidad
            medico.telefono = telefono
            user.save()
            medico.save()
            return medico
        except:
            return None
    def eliminar_medico(self,username):
        try:
            user = User.objects.get(username=username)
            medico = Medico.objects.get(user=user)
            medico.delete()
            user.delete()
            return True
        except:
            return False
    
    def getMedicos(self):
        res = Medico.objects.all().filter(centro_medico=self.centro)
        return res