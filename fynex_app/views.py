from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'fynex_app/index.html')