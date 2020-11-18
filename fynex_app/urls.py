from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="Fynex-index"),
    path('privacy-policy', views.privacy_policy,name="Fynex-privacy-policy"),
    path('logout', views.logout_user, name="Logout-index"),
    path('administrator', views.administrator_index, name="Administrator-index"),
    path('CentroMedico', views.centroMedico_index, name="CentroMedico-index"),
    path('Medico', views.medico_index, name="Medico-index"),
    path('Medico/<int:cod_paciente>/paciente', views.medico_paciente, name="Medico-paciente-index"),
    path('Medico/<int:cod_paciente>/nutrition_recommendations', views.medico_nutricion, name="Medico-nutricion-index"),
]
