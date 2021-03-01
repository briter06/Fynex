from django.urls import path
from . import views
from .classes.tools import Tools

urlpatterns = [
    path('', views.index, name="Fynex-index"),
    path('privacy-policy', views.privacy_policy,name="Fynex-privacy-policy"),
    path('logout', views.logout_user, name="Logout-index"),
    path('administrator', views.administrator_index, name="Administrator-index"),

    path('CentroMedico', views.centroMedico_index, name="CentroMedico-index"),

    path('Medico', views.medico_index, name="Medico-index"),
    path('Medico/<int:cod_paciente>/paciente', views.medico_paciente, name="Medico-paciente-index"),
    path('Medico/<int:cod_paciente>/nutrition_recommendations', views.medico_nutricion, name="Medico-nutricion-index"),
    path('Medico/<int:cod_paciente>/exercise_recommendations', views.medico_ejercicio, name="Medico-ejercicio-index"),
    
    path('Medico/<int:cod_paciente>/variables', views.medico_variables, name="Medico-variables-index"),
    path('Medico/<int:cod_paciente>/variables/<int:cod_variable>', views.medico_variable_historico, name="Medico-variables-historial-index"),
    path('Medico/<int:cod_paciente>/plan_nutricion/generar', views.medico_generar_nutricion, name="Medico-nutrition-generate-index"),
    path('Medico/<int:cod_paciente>/plan_nutricion/<int:cod_plan>', views.medico_detail_nutricion, name="Medico-nutrition-plan-index"),
    path('Medico/<int:cod_paciente>/examenes', views.medico_examenes, name="Medico-examenes-index"),

    path('Paciente/info', views.paciente_index, name="Paciente-index"),
    path('Paciente/nutrition_recommendations', views.paciente_nutricion, name="Paciente-nutrition-index"),
    path('Paciente/plan_nutricion/<int:cod_plan>', views.paciente_detail_nutricion, name="Paciente-nutrition-plan-index"),
    
    path('Medico/<int:cod_paciente>/chat', views.medico_chat, name="Medico-chat"),
    path('Paciente/chat', views.paciente_chat, name="Paciente-chat"),
    path('Paciente/variables', views.paciente_variables, name="Paciente-variables-index"),
    path('Paciente/examenes', views.paciente_examenes, name="Paciente-examenes-index"),




    path('download/<str:file_name>', views.download_test, name="Download"),

    path('fg_passwd/', Tools.sendEmailUserPasswd , name="passwd"),
    
]
