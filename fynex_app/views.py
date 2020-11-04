from django.shortcuts import render
from django.contrib.auth.models import User

from .recommender.HybridRecommender import HybridRecommender
from .recommender.ContentRecommender import ContentRecommender

# Create your views here.


def index(request):
    testRecommender()
    return render(request, 'fynex_app/index.html')

def testRecommender():
    heartRate = 90
    glucose = 180
    height = 1.65
    weight = 65
    age = 55

    hr = HybridRecommender()

    result = hr.predict(heartRate,glucose,height,weight,age)
    print(result['recommendations'])