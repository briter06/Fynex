import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from .DiseasePredictor import DiseasePredictor
from .ContentRecommender import ContentRecommender
import math

class HybridRecommender:

    def __init__(self):
        self.disease_predictor = DiseasePredictor()
        self.content_recommender = ContentRecommender()
    
    def predict(self,heartRate, glucose, height, weight, age):
        bmi = weight/math.pow(height,2)
        res_disease = self.disease_predictor.predictDisease(heartRate,glucose,bmi,age)
        res_disease = res_disease[res_disease['Proba']>0.5]
        diseases = res_disease['Disease'].values
        degrees_freedom = 0.3 if len(diseases) == 0 else 0.1
        diseases = ['normal'] if len(diseases) == 0 else diseases
        res = self.content_recommender.predict(diseases,degrees_freedom)
        return {'diseases':diseases,'recommendations':res}


