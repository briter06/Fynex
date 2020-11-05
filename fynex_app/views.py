from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate
from .recommender.HybridRecommender import HybridRecommender

# Create your views here.

def login(request, template_name):
    username = request.POST['user_name']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        return testRecommender(request)
    else:
        messages.error(
            request, 'El usuario o la contraseña son incorrectos')
    return HttpResponseRedirect(reverse(template_name))

def index(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            return login(request, 'Fynex-index')
    else:
        return render(request, 'fynex_app/index.html')

def testRecommender(request):
    heartRate = 90
    glucose = 180
    height = 1.65
    weight = 65
    age = 55

    hr = HybridRecommender()

    result = hr.predict(heartRate,glucose,height,weight,age)
    return render(request,'fynex_app/res_temp.html',{"result":result['recommendations'].to_html()})