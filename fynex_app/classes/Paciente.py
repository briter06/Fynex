from ..models import VariableSeguimiento
from ..models import PlanNutricional
from ..models import PartePlanNutricional
from ..models import Paciente
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pandas as pd

class PacienteHelper:

    def __init__(self,user):
        self.paciente = Paciente.objects.all().get(user=user)
    
    def getPlanesNutricionales(self):
        planes = PlanNutricional.objects.all().filter(paciente=self.paciente,estado='A').order_by('id')
        return planes
    
    def getPartesDePlanNutricional(self,plan):
        return PartePlanNutricional.objects.all().filter(plan_nutricional=plan)
    
    def getPlanNutricional(self,cod_plan):
        try:
            return PlanNutricional.objects.all().get(pk=cod_plan,paciente=self.paciente)
        except:
            return None
    
    