from selenium import webdriver
from django.urls import reverse
from fynex_app.classes.Administrator import Administrator
from fynex_app.classes.CentroMedico import CentroMedicoHelper
from fynex_app.classes.Medico import MedicoHelper
from django.contrib.auth.models import User
from fynex_app.models import *
from django.contrib.auth.models import Group
from django.test import SimpleTestCase 
import unittest
import time
import os
from .Pruebas import Pruebas
from datetime import date

# g1 = Group.objects.create(name='administrator')
# g2 = Group.objects.create(name='centro_medico')
# g3 = Group.objects.create(name='medico')
# g4 = Group.objects.create(name='paciente')
# self.admin = User.objects.create_superuser('fynexhealth@gmail.com', 'fynexhealth@gmail.com', '1234')
# adminHelper = Administrator(self.admin)
# self.centro = adminHelper.registrar_centro('cobos@gmail.com','1234','Cobos','Cr 1','123456')
# centroHelper = CentroMedicoHelper(self.centro.user)
# self.medico = centroHelper.registrar_medico('btg.developers@gmail.com','1234','Camilo Rodriguez','543654','Nutricionista','35454')
# medicoHelper = MedicoHelper(self.medico.user)
# self.paciente = medicoHelper.registrar_paciente('bgonzalezd@gmail.com','1234','Briter Gonzalez','2000-06-06','543654','35454')

# medicoHelper = MedicoHelper(self.medico.user)
# variables = VariableSeguimiento.objects.all().filter(paciente=self.paciente)
# for x in variables:
#     medicoHelper.guardarHistorialVariable(x,date.today(),200)


class TestLogin(SimpleTestCase):

    databases = '__all__'

    def setUp(self):
        self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        self.admin = User.objects.get(username='fynexhealth@gmail.com')
        self.centro = CentroMedico.objects.get(user__username='cobos@gmail.com')
        self.medico = Medico.objects.get(user__username='btg.developers@gmail.com')
        self.paciente = Paciente.objects.get(user__username='bgonzalezd@gmail.com')
        self.host = 'http://localhost:8000'
            

    
    def tearDown(self):
        self.browser.close()
    
    def testMedicoLogin(self):
        self.browser.get(self.host)
        btn_login = self.browser.find_elements_by_id('boton_iniciar_sesion')[0]
        btn_login.click()
        time.sleep(1)
        user_name = self.browser.find_elements_by_id('user_name')[0]
        password = self.browser.find_elements_by_id('password')[0]
        self.browser.execute_script("arguments[0].setAttribute('value',arguments[1])",user_name, self.medico.user.username)
        self.browser.execute_script("arguments[0].setAttribute('value',arguments[1])",password, '1234')
        submit_login = self.browser.find_elements_by_id('submit_login')[0]
        submit_login.click()
        time.sleep(3)
        pacientes_titulo = self.browser.find_elements_by_class_name('main_section')[0]
        pacientes_titulo = pacientes_titulo.find_elements_by_tag_name('h1')[0].text
        self.assertEqual(pacientes_titulo,'PACIENTES')
        pruebas = Pruebas(self)
        pruebas.pruebasMedico()
        self.browser.get(self.host+'/logout')
    
    def testPacienteLogin(self):
        self.browser.get(self.host)
        btn_login = self.browser.find_elements_by_id('boton_iniciar_sesion')[0]
        btn_login.click()
        time.sleep(1)
        user_name = self.browser.find_elements_by_id('user_name')[0]
        password = self.browser.find_elements_by_id('password')[0]
        self.browser.execute_script("arguments[0].setAttribute('value',arguments[1])",user_name, self.paciente.user.username)
        self.browser.execute_script("arguments[0].setAttribute('value',arguments[1])",password, '1234')
        submit_login = self.browser.find_elements_by_id('submit_login')[0]
        submit_login.click()
        time.sleep(3)
        pacientes_titulo = self.browser.find_elements_by_id('personal_info')[0]
        pacientes_titulo = pacientes_titulo.find_elements_by_tag_name('h2')[0]
        pacientes_titulo = pacientes_titulo.find_elements_by_tag_name('strong')[0].text
        self.assertEqual(pacientes_titulo,'Briter Gonzalez')
        pruebas = Pruebas(self)
        pruebas.pruebasPaciente()
        self.browser.get(self.host+'/logout')