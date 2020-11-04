from tensorflow.keras import models
import pickle
import pandas as pd
import os
from django.conf import settings

class DiseasePredictor:

    def __init__(self):
        self.model_diabetes = models.load_model(os.path.join(settings.RECOMMENDER_ROOT, 'Models\diabetes_model-tensor.h5'))
        self.model_hypertension = pickle.load(open(os.path.join(settings.RECOMMENDER_ROOT, 'Models\hyper_logistic.fynex'),'rb'))
    
    def predict_diabetes(self,glucose,bmi,age):
        pred_data = [[glucose,bmi,age]]
        prediction = self.model_diabetes.predict(pred_data)
        return prediction[0][0]
    def predict_hypertension(self,heartRate,bmi,age):
        pred_data = [[age,bmi,heartRate]]
        prediction = self.model_hypertension.predict_proba(pred_data)
        return prediction[0][1]
    
    def predictDisease(self,heartRate,glucose,bmi,age):
        pred_diabetes = self.predict_diabetes(glucose,bmi,age)
        pred_hypertension = self.predict_hypertension(heartRate,bmi,age)
        res = pd.DataFrame([['diabetes',pred_diabetes],['hypertension',pred_hypertension]],columns=['Disease','Proba']).sort_values(by='Proba',ascending=False)
        return res



