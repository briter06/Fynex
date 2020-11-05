from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .recommender.HybridRecommender import HybridRecommender

# Create your views here.

def login_user(request, template_name):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        messages.error(
            request, 'El usuario o la contraseña son incorrectos')
    else:
        login(request, user)
    return HttpResponseRedirect(reverse(template_name))

def verify_auth(request,group_name):
    if not request.user.groups.filter(name='administrator').exists():
        return False
    return True

def index(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            return login_user(request, 'Fynex-index')
    else:
        if request.user.is_authenticated:
            if request.user.groups.filter(name='administrator').exists():
                return HttpResponseRedirect(reverse('Administrator-index'))
            else:
                return logout_user(request)
        else:
            return render(request, 'fynex_app/index.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('Fynex-index'))

def administrator_index(request):
    if not verify_auth(request,'administrator'):
        return HttpResponseRedirect(reverse('Fynex-index'))
    if request.method=='POST':
        return logout_user(request)
    else:
        heartRate = 90
        glucose = 180
        height = 1.65
        weight = 65
        age = 55

        hr = HybridRecommender()

        result = hr.predict(heartRate,glucose,height,weight,age)
        return render(request,'fynex_app/administrator/res_temp.html',{"result":result['recommendations'].to_html()})