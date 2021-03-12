from ..models import VariableSeguimiento
from ..models import PlanNutricional
from ..models import PlanEjercicio
from ..models import PartePlanNutricional
from ..models import HistorialVariableSeguimiento
from ..models import Paciente
from ..models import Examen
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pandas as pd
from .tools import Tools

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

    def getPlanEjercicio(self,cod_plan):
        try:
            return PlanEjercicio.objects.all().get(pk=cod_plan,paciente=self.paciente)
        except:
            return None

    def getVariablesSeguimiento(self):
        res = VariableSeguimiento.objects.all().filter(paciente=self.paciente)
        return res
    
    def getHistoricoVariable(self,variable):
        return HistorialVariableSeguimiento.objects.all().filter(variable_seguimiento=variable).order_by('fecha')

    def verifyExamen(self,cod_examen):
        res = Examen.objects.all().filter(paciente=self.paciente,pk=cod_examen)
        return res
    
    def getExamenes(self):
        res = Examen.objects.all().filter(paciente=self.paciente)
        return res
    def subirArchivo(self,cod_examen,ruta):
        try:
            res = Examen.objects.all().get(pk=cod_examen)
            res.fecha_entrega = Tools.getToday()
            res.documento_ruta = ruta
            res.save()
            return res
        except:
            return None
    
    def getPlanesEjercicio(self):
        planes = PlanEjercicio.objects.all().filter(paciente=self.paciente).order_by('id')
        return planes
