import pickle
import pandas as pd
from scipy.spatial import distance
import random
import os
from django.conf import settings
from os import listdir
from os.path import isfile, join

class ContentRecommenderNutrition:

    def __init__(self):
        self.data = pickle.load(open(os.path.join(settings.RECOMMENDER_ROOT, 'Assets/data.fynex'),'rb'))
        self.partes_menu = ['desayuno','almuerzo','comida']
        self.df_menu = {}
        self.df_diet = {}
        path_menu = os.path.join(settings.RECOMMENDER_ROOT, 'Menu')

        for f in listdir(path_menu):
            file = join(path_menu, f)
            if isfile(file):
                name = f.split('.')[0]
                self.df_menu[name] = pd.read_csv(file,delimiter=';',encoding="UTF-8")

        path_diets = os.path.join(settings.RECOMMENDER_ROOT, 'Diets')

        for f in listdir(path_diets):
            file = join(path_diets, f)
            if isfile(file):
                name = f.split('.')[0]
                self.df_diet[name] = pd.read_csv(file,delimiter=';',encoding="UTF-8",index_col=0)


    
    def harris_benedict(self,gender,weight,height,age):
        if gender == 1:
            return (13.397*weight)+(479.9*height)-(5.677*age)+88.362
        else:
            return (9.24*weight)+(309.8*height)-(4.33*age)+447.593
    def calorieIntake(self,gender,weight,height,age,exercise):
        return exercise*self.harris_benedict(gender,weight,height,age)
    def closest_node(self,node, nodes,degree_freedom):
        closest_index = distance.cdist(node, nodes)
        aux_df = pd.DataFrame(closest_index[0]).sort_values(by=0)
        num = 0
        try:
            num = random.randrange(int(len(closest_index[0])*degree_freedom))
        except:
            pass
        return aux_df.iloc[[num]].index.values[0]
    def getFood(self,menu):
        partes = menu.split('/')
        return random.choice(partes)
    def get_diet(self,diseases):
        dfs = list(map(lambda x: self.df_diet[x], diseases))
        tot_diet = pd.concat(dfs)
        tot_diet = tot_diet.groupby(tot_diet.index).mean()
        return tot_diet
    def predict(self,diseases,degree_freedom=0.1):
        menu = self.df_menu[diseases[0]]
        diet = self.get_diet(diseases)
        result = []
        res_diff1 = {'proteinas':{'desayuno':0,'almuerzo':0,'comida':0},'carbohidratos':{'desayuno':0,'almuerzo':0,'comida':0},'grasas':{'desayuno':0,'almuerzo':0,'comida':0}}
        res_diff2 = {'proteinas':{'desayuno':0,'almuerzo':0,'comida':0},'carbohidratos':{'desayuno':0,'almuerzo':0,'comida':0},'grasas':{'desayuno':0,'almuerzo':0,'comida':0}}
        for parte in self.partes_menu:
            df_parte = menu[menu['Parte']==parte]
            for alimentos in df_parte['Alimentos'].values:
                alimento = self.getFood(alimentos)
                point_current = diet.loc[[alimento]]
                res_diff1['proteinas'][parte]+=point_current['Protein'][0]
                res_diff1['carbohidratos'][parte]+=point_current['Carbohidrates'][0]
                res_diff1['grasas'][parte]+=point_current['Fat'][0]
                food = self.data[alimento]
                data_food = food[['Proteina(g)','Carbohidratos(g)','GrasaTotal(g)']]
                num = self.closest_node(point_current.values,data_food.values,degree_freedom)
                res = food.iloc[num]
                result.append([parte,alimento,res['Nombre'],res['Energia(Kcal)'],res['Proteina(g)'],res['Carbohidratos(g)'],res['GrasaTotal(g)']])
                res_diff2['proteinas'][parte]+=res['Proteina(g)']
                res_diff2['carbohidratos'][parte]+=res['Carbohidratos(g)']
                res_diff2['grasas'][parte]+=res['GrasaTotal(g)']
        res_diff = {'proteinas':{'desayuno':0,'almuerzo':0,'comida':0},'carbohidratos':{'desayuno':0,'almuerzo':0,'comida':0},'grasas':{'desayuno':0,'almuerzo':0,'comida':0}}
        for parte in self.partes_menu:
            res_diff['proteinas'][parte] = res_diff2['proteinas'][parte]-res_diff1['proteinas'][parte]
            res_diff['carbohidratos'][parte] = res_diff2['carbohidratos'][parte]-res_diff1['carbohidratos'][parte]
            res_diff['grasas'][parte] = res_diff2['grasas'][parte]-res_diff1['grasas'][parte]
        df_res = pd.DataFrame(result,columns=['Parte','Alimento','Nombre','Energia(Kcal)','Proteina(g)','Carbohidratos(g)','GrasaTotal(g)'])
        return [df_res,res_diff]
    
    def howFar(self,data,food_data):
        closest_index = distance.cdist(data, food_data.values)
        aux_df = pd.DataFrame(closest_index[0]).sort_values(by=0)
        print(aux_df)


