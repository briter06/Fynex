from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="Fynex-index"),
    path('administrator', views.administrator_index, name="Administrator-index"),
]
