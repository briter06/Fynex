from ..models import Medico
from ..models import Paciente
from ..models import VariableSeguimiento
from ..models import HistorialVariableSeguimiento
from ..models import PlanNutricional
from ..models import PartePlanNutricional
from ..models import PlanEjercicio
from ..models import RecomendadorMemoria
from ..models import Examen
from django.db.models import Max
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from .tools import Tools

class MedicoHelper:

    def __init__(self,user):
        self.medico = Medico.objects.all().get(user=user)
    
    def getEdad(self,cod_paciente):
        try:
            paciente = Paciente.objects.all().get(pk=cod_paciente)
            res = relativedelta(datetime.date.today(), paciente.fecha_nacimiento).years
            return res
        except:
            return 0

    def getRitmoCardiaco(self,cod_paciente):
        try:
            var = VariableSeguimiento.objects.all().get(paciente__id=cod_paciente,nombre = 'Ritmo Cardiaco')
            historial = HistorialVariableSeguimiento.objects.all().filter(variable_seguimiento=var).order_by('fecha').last()
            return historial
        except:
            return None
    
    def getGlucosa(self,cod_paciente):
        try:
            var = VariableSeguimiento.objects.all().get(paciente__id=cod_paciente,nombre = 'Nivel de glucosa')
            historial = HistorialVariableSeguimiento.objects.all().filter(variable_seguimiento=var).order_by('fecha').last()
            return historial
        except:
            return None

    def getAltura(self,cod_paciente):
        try:
            var = VariableSeguimiento.objects.all().get(paciente__id=cod_paciente,nombre = 'Altura')
            historial = HistorialVariableSeguimiento.objects.all().filter(variable_seguimiento=var).order_by('fecha').last()
            return historial
        except:
            return None
    
    def getPeso(self,cod_paciente):
        try:
            var = VariableSeguimiento.objects.all().get(paciente__id=cod_paciente,nombre = 'Peso')
            historial = HistorialVariableSeguimiento.objects.all().filter(variable_seguimiento=var).order_by('fecha').last()
            return historial
        except:
            return None
    
    def eliminarPlanNutricional(self,cod_plan):
        try:
            plan = PlanNutricional.objects.all().get(pk=cod_plan)
            plan.delete()
            return True
        except:
            return False
    def getPlanesNutricionales(self,cod_paciente):
        paciente = Paciente.objects.all().get(pk=cod_paciente)
        planes = PlanNutricional.objects.all().filter(paciente=paciente).order_by('id')
        return planes
    
    def getPlanesEjercicio(self,cod_paciente):
        paciente = Paciente.objects.all().get(pk=cod_paciente)
        planes = PlanEjercicio.objects.all().filter(paciente=paciente).order_by('id')
        return planes

    def getPartesDePlanNutricional(self,plan):
        return PartePlanNutricional.objects.all().filter(plan_nutricional=plan)
    
    def getPlanNutricional(self,cod_plan):
        try:
            return PlanNutricional.objects.all().get(pk=cod_plan)
        except:
            return None
    
    def modificarPlanNutricional(self,id,rating,estado):
        try:
            plan = PlanNutricional.objects.all().get(pk=id)
            plan.rating = rating
            plan.estado = estado
            plan.save()
            return plan
        except:
            return None
    def guardarRecomendacionNutricion(self,df,cod_paciente):
        try:
            plan = PlanNutricional()
            plan.paciente = Paciente.objects.all().get(pk=cod_paciente)
            plan.rating = 0
            plan.estado = "I"
            plan.save()
            for i,row in df.iterrows():
                parte = PartePlanNutricional()
                parte.plan_nutricional = plan
                parte.parte = row['Parte']
                parte.alimento = row['Alimento']
                parte.nombre = row['Nombre']
                parte.calorias = row['Energia(Kcal)']
                parte.proteinas = row['Proteina(g)']
                parte.carbohidratos = row['Carbohidratos(g)']
                parte.grasas = row['GrasaTotal(g)']
                parte.save()
            return plan
        except Exception as e:
            print (e)
            return None
    def guardarHistorialVariable(self,variable,fecha,valor):
        try:
            historico = HistorialVariableSeguimiento()
            historico.variable_seguimiento = variable
            historico.fecha = fecha
            historico.valor = valor
            historico.save()
            return historico
        except:
            return None
    def modificarHistorialVariable(self,cod_historico,fecha,valor):
        try:
            historico = HistorialVariableSeguimiento.objects.all().get(pk=cod_historico)
            historico.fecha = fecha
            historico.valor = valor
            historico.save()
            return historico
        except:
            return None
    
    def eliminarHistorialVariable(self,cod_historico):
        try:
            historico = HistorialVariableSeguimiento.objects.all().get(pk=cod_historico)
            historico.delete()
            return True
        except:
            return False

    def getHistoricoVariable(self,variable):
        return HistorialVariableSeguimiento.objects.all().filter(variable_seguimiento=variable)

    def getVariable(self,cod_variable):
        try:
            return VariableSeguimiento.objects.all().get(pk=cod_variable)
        except:
            return None


    def modificarVariable(self,cod_variable,nombre,intervalo_referencia,unidad):
        try:
            variable = VariableSeguimiento.objects.all().get(pk=cod_variable)
            variable.nombre = nombre
            variable.intervalo_referencia = intervalo_referencia
            variable.unidad = unidad
            variable.save()
            return variable
        except:
            return None
    def eliminarVariable(self,cod_variable):
        try:
            variable = VariableSeguimiento.objects.all().get(pk=cod_variable)
            variable.delete()
            return True
        except:
            return False
    def addVariableSeguimiento(self,nombre,intervalo_referencia,unidad,paciente,obligatorio):
        try:
            res = VariableSeguimiento.objects.all().filter(nombre = nombre.strip(),paciente=paciente).count()
            if res !=0:
                return None
            variable = VariableSeguimiento()
            variable.nombre = nombre.strip()
            variable.intervalo_referencia = intervalo_referencia
            variable.unidad = unidad
            variable.paciente = paciente
            variable.obligatorio = obligatorio
            variable.save()
            return variable
        except Exception as e:
            print(e)
            return None
    
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
            res = Tools.sendEmailUserAdded(user,password)
            self.addVariableSeguimiento('Ritmo Cardiaco','Normal: [60-100]','latidos/minuto',paciente,1)
            self.addVariableSeguimiento('Nivel de glucosa','Normal: [70-100] en ayunas, [70-140] despues de comer','mg/dl',paciente,1)
            self.addVariableSeguimiento('Altura','','Metros',paciente,1)
            self.addVariableSeguimiento('Peso','','Kilogramos',paciente,1)
            return paciente
        except Exception as e:
            print(e)
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
    def verifyExamen(self,cod_examen):
        pacientes = Paciente.objects.all().filter(medico=self.medico)
        res = Examen.objects.all().filter(paciente__in=pacientes,pk=cod_examen)
        return res
    def verifyPlanNutricional(self,cod_paciente,cod_plan):
        res = PlanNutricional.objects.all().filter(pk=cod_plan,paciente__id=cod_paciente,paciente__medico=self.medico)
        return res
    
    def getVariablesSeguimiento(self,cod_paciente):
        paciente = Paciente.objects.all().get(pk=cod_paciente)
        res = VariableSeguimiento.objects.all().filter(paciente=paciente)
        return res
    
    def getExamenes(self,cod_paciente):
        paciente = Paciente.objects.all().get(pk=cod_paciente)
        res = Examen.objects.all().filter(paciente=paciente)
        return res
    def addExamen(self,nombre,descripcion,fecha_peticion,paciente):
        try:
            examen = Examen()
            examen.nombre = nombre.strip()
            examen.descripcion = descripcion.strip()
            examen.fecha_peticion = fecha_peticion
            examen.paciente = paciente
            examen.save()
            return examen
        except Exception as e:
            print(e)
            return None
    def modificarExamen(self,cod_examen,nombre,descripcion,fecha_peticion):
        try:
            examen = Examen.objects.all().get(pk=cod_examen)
            examen.nombre = nombre
            examen.descripcion = descripcion
            examen.fecha_peticion = fecha_peticion
            examen.save()
            return examen
        except:
            return None

    def eliminarExamen(self,cod_examen):
        try:
            examen = Examen.objects.all().get(pk=cod_examen)
            examen.delete()
            return True
        except:
            return False

    def getMemoryRecommendation(self,cod_paciente):
        try:
            similar = RecomendadorMemoria.objects.filter(user1=cod_paciente,usado=False).order_by('-similitud').first()
            if similar==None:
                return None
            plan_prev = PlanNutricional.objects.filter(paciente__id=similar.user2).order_by('-rating').first()
            partes = self.getPartesDePlanNutricional(plan_prev)
            
            plan = PlanNutricional()
            plan.paciente = Paciente.objects.all().get(pk=cod_paciente)
            plan.rating = 0
            plan.estado = "I"
            plan.save()

            for p in partes:
                parte = PartePlanNutricional()
                parte.plan_nutricional = plan
                parte.parte = p.parte
                parte.alimento = p.alimento
                parte.nombre = p.nombre
                parte.calorias = p.calorias
                parte.proteinas = p.proteinas
                parte.carbohidratos = p.carbohidratos
                parte.grasas = p.grasas
                parte.save()
            similar.usado = True
            similar.save()
            return plan
        except:
            return None
        