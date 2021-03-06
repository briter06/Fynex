import pandas as pd
import os
from django.conf import settings
import random

class ContentRecommenderExercise:

    def __init__(self):
        self.df_plans = pd.read_csv(os.path.join(settings.RECOMMENDER_ROOT, 'Exercise/plans.csv'),delimiter=';',encoding='UTF8',index_col=0)
        self.df_sports = pd.read_csv(os.path.join(settings.RECOMMENDER_ROOT, 'Exercise/sports.csv'),delimiter=';',encoding='UTF8')
    
    def predict(self,disease):
        df_disease_plan = self.df_plans.loc[disease]
        ex_type = df_disease_plan['exercise']
        df_disease_sports = self.df_sports[self.df_sports['type']==ex_type]
        res = pd.DataFrame([random.choice(df_disease_sports.values)],columns=df_disease_sports.columns)
        res = res.set_index(self.df_plans.loc[[disease]].index.values)
        return pd.concat([res,self.df_plans.loc[[disease]]], axis=1)