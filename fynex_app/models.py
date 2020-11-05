from django.db import models
from django.contrib.auth.models import User

#Falta -> PlaneActividadFisica

class CentroMedico(models.Model):
    dirección = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Medico(models.Model):
    centro_medico = models.ForeignKey(CentroMedico, on_delete=models.CASCADE)
    documento_identificacion = models.CharField(max_length=30)
    especialidad = models.CharField(max_length=250)
    telefono = models.CharField(max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
class Paciente(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    documento_identificacion = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Auditoria(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=250)
    direccion_ip = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class PreexistenciaMedica(models.Model):
    descripcion = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class VariableSeguimiento(models.Model):
    nombre = models.CharField(max_length=30)
    intervalo_referencia = models.CharField(max_length=50)
    unidad = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class HistorialVariableSeguimiento(models.Model):
    variable_seguimiento = models.ForeignKey(VariableSeguimiento,on_delete=models.CASCADE)
    valor = models.FloatField()
    fecha = models.DateTimeField()
class Examen(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateTimeField()
    documento_ruta = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class PlanNutricional(models.Model):
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    rating = models.FloatField
class PartePlanNutricional(models.Model):
    plan_nutricional = models.ForeignKey(PlanNutricional,on_delete=models.CASCADE)
    parte = models.CharField(max_length=30)
    alimento = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    calorias = models.FloatField()
    proteinas = models.FloatField()
    carbohidratos = models.FloatField()
    grasas = models.FloatField()