from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="Fynex-index"),
    path('logout', views.logout_user, name="Logout-index"),
    path('administrator', views.administrator_index, name="Administrator-index"),
    path('CentroMedico', views.centroMedico_index, name="CentroMedico-index"),
    path('Medico', views.medico_index, name="Medico-index"),
]
