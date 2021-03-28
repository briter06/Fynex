from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetimeutc.fields import DateTimeUTCField
from django_cryptography.fields import encrypt

#Falta -> PlaneActividadFisica

class CentroMedico(models.Model):
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Medico(models.Model):
    centro_medico = models.ForeignKey(CentroMedico, on_delete=models.CASCADE)
    documento_identificacion = encrypt(models.CharField(max_length=30))
    especialidad = encrypt(models.CharField(max_length=250))
    telefono = encrypt(models.CharField(max_length=30))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
class Paciente(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    documento_identificacion = encrypt(models.CharField(max_length=30))
    telefono = encrypt(models.CharField(max_length=30))
    fecha_nacimiento = models.DateField(default=now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Auditoria(models.Model):
    fecha = DateTimeUTCField()
    descripcion = models.CharField(max_length=250)
    direccion_ip = models.CharField(max_length=50)
    correo_usuario = models.CharField(max_length=50)
    tipo_usuario = models.CharField(max_length=50)
class VariableSeguimiento(models.Model):
    nombre = models.CharField(max_length=50)
    intervalo_referencia = models.CharField(max_length=150)
    unidad = models.CharField(max_length=150)
    obligatorio = models.IntegerField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
class HistorialVariableSeguimiento(models.Model):
    variable_seguimiento = models.ForeignKey(VariableSeguimiento,on_delete=models.CASCADE)
    valor = models.FloatField()
    fecha = models.DateField()
class Examen(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    fecha_peticion = models.DateField()
    fecha_entrega = models.DateField(default=None, blank=True, null=True)
    documento_ruta = encrypt(models.CharField(max_length=200))
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
class PlanNutricional(models.Model):
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha = models.DateField()
    rating = models.FloatField()
    estado = models.CharField(max_length=1)
    dif_proteinas = models.TextField()
    dif_carbohidratos = models.TextField()
    dif_grasas = models.TextField()
    generador = models.TextField()
class PartePlanNutricional(models.Model):
    plan_nutricional = models.ForeignKey(PlanNutricional,on_delete=models.CASCADE)
    parte = models.CharField(max_length=30)
    alimento = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    calorias = models.FloatField()
    proteinas = models.FloatField()
    carbohidratos = models.FloatField()
    grasas = models.FloatField()
class PlanEjercicio(models.Model):
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    fecha = models.DateField()
    rating = models.FloatField()
    estado = models.CharField(max_length=1)
    tipo_ejercicio = models.CharField(max_length=50)
    ejercicio = models.CharField(max_length=50)
    info = models.CharField(max_length=200)
    dias = models.CharField(max_length=50)
    tiempo = models.CharField(max_length=50)
    generador = models.TextField()

class Mensaje(models.Model):
    fecha = DateTimeUTCField()
    mensaje = encrypt(models.TextField())
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    paciente_emisor = models.IntegerField()
    notificado_email = models.BooleanField()


class SistemaMemoria(models.Model):
    user1 = models.IntegerField()
    user2 = models.IntegerField()
    similitud = models.FloatField()
    usado_nutricion = models.BooleanField()
    usado_ejercicio = models.BooleanField()