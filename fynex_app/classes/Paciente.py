from ..models import VariableSeguimiento
from ..models import Paciente
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pandas as pd

class PacienteHelper:

    def __init__(self,user):
        self.paciente = Paciente.objects.all().get(user=user)
    
    