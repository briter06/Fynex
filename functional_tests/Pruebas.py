import time

class Pruebas:

    def __init__(self,tester):
        self.tester = tester
    
    def pruebasMedico(self):
        self.entrarAPaciente()
        self.entrarAPlanesNutricionales()
        self.generarPlanNutricional()
        self.entrarAPlanesEjercicio()
        self.generarPlanEjercicio()
        self.entrarSeguimiento()
        self.entrarExamenes()
        self.entrarChat()
        self.entrarPerfil()
    
    def pruebasPaciente(self):
        self.entrarPerfilPaciente()
        self.entrarAPlanesNutricionalesPaciente()
        self.entrarAPlanesEjercicioPaciente()
        self.entrarExamenesPaciente()
        self.entrarChatPaciente()

    def entrarAPaciente(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/paciente')
        titulo_nombre = self.tester.browser.find_elements_by_id('personal_info')[0].find_elements_by_tag_name('h2')[0].find_elements_by_tag_name('strong')[0].text
        self.tester.assertEqual(titulo_nombre,'Briter Gonzalez')
    
    def entrarAPlanesNutricionales(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/nutrition_recommendations')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Planes nutricionales de Briter Gonzalez')
    
    def generarPlanNutricional(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/plan_nutricion/generar')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Plan generado para Briter Gonzalez')
    
    def entrarAPlanesEjercicio(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/exercise_recommendations')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Planes de ejercicio de Briter Gonzalez')
    
    def generarPlanEjercicio(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/plan_ejercicio/generar')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Plan generado para Briter Gonzalez')
    
    def entrarSeguimiento(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/variables')
        inputs = len(self.tester.browser.find_elements_by_css_selector('input[type="date"]'))
        self.tester.assertEqual(inputs,2)
    
    def entrarExamenes(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/examenes')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Exámenes de Briter Gonzalez')
    
    def entrarChat(self):
        self.tester.browser.get(self.tester.host+f'/Medico/{self.tester.paciente.id}/chat')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Chat con Briter Gonzalez')
    
    def entrarPerfil(self):
        self.tester.browser.get(self.tester.host+f'/Medico/perfil')
        titulo_nombre = self.tester.browser.find_elements_by_id('personal_info')[0].find_elements_by_tag_name('h2')[0].find_elements_by_tag_name('strong')[0].text
        self.tester.assertEqual(titulo_nombre,'Camilo Rodriguez')
    
    def entrarPerfilPaciente(self):
        self.tester.browser.get(self.tester.host+f'/Paciente/info')
        titulo_nombre = self.tester.browser.find_elements_by_id('personal_info')[0].find_elements_by_tag_name('h2')[0].find_elements_by_tag_name('strong')[0].text
        self.tester.assertEqual(titulo_nombre,'Briter Gonzalez')
    
    def entrarAPlanesNutricionalesPaciente(self):
        self.tester.browser.get(self.tester.host+f'/Paciente/nutrition_recommendations')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Mis planes nutricionales')
    
    def entrarAPlanesEjercicioPaciente(self):
        self.tester.browser.get(self.tester.host+f'/Paciente/exercise_recommendations')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Mis planes de ejercicio')
    
    def entrarExamenesPaciente(self):
        self.tester.browser.get(self.tester.host+f'/Paciente/examenes')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Mis exámenes')
    
    def entrarChatPaciente(self):
        self.tester.browser.get(self.tester.host+f'/Paciente/chat')
        titulo_nombre = self.tester.browser.find_elements_by_tag_name('h1')[0].text
        self.tester.assertEqual(titulo_nombre,'Chat con Camilo Rodriguez')
