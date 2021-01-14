from ..models import CentroMedico
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pandas as pd
from .tools import Tools

class Administrator:

    def __init__(self,user):
        self.user = user
    
    def registrar_centro(self,username,password,first_name,direccion,telefono):
        try:
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.last_name = ""
            centro = CentroMedico()
            centro.user = user
            centro.direccion = direccion
            centro.telefono = telefono
            group = Group.objects.get(name='centro_medico') 
            user.save()
            centro.save()
            group.user_set.add(user)
            
            res = Tools.sendEmailUserAdded(user,password)

            return centro
        except:
            return None
    def modificar_centro(self,username,newusername,first_name,direccion,telefono):
        try:
            user = User.objects.get(username=username)
            centro = CentroMedico.objects.get(user=user) 
            user.username = newusername
            user.first_name = first_name
            centro.direccion = direccion
            centro.telefono = telefono
            user.save()
            centro.save()
            return centro
        except:
            return None
    def eliminar_centro(self,username):
        try:
            user = User.objects.get(username=username)
            centro = CentroMedico.objects.get(user=user)
            centro.delete()
            user.delete()
            return True
        except:
            return False
    
    def getCentrosMedicos(self):
        res = CentroMedico.objects.all()
        return res