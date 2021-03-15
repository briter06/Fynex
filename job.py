import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Fynex.settings")
django.setup()


from fynex_app.models import *
import pandas as pd

res = VariableSeguimiento.objects.raw('''
SELECT DISTINCT ON (id) id,nombre,paciente_id,valor FROM (
SELECT fynex_app_variableseguimiento.id,nombre,paciente_id,valor,fecha FROM fynex_app_variableseguimiento, fynex_app_historialvariableseguimiento
WHERE fynex_app_variableseguimiento.id = fynex_app_historialvariableseguimiento.variable_seguimiento_id
ORDER BY fecha desc) AS c2


''')

results = []

for x in res:
    aux_di = x.__dict__
    results.append(aux_di)


df = pd.DataFrame(results)[['paciente_id','nombre','valor']]
df['nombre'] = df['nombre'].apply(lambda x: x.lower().strip())

indexes = list(zip(*df[['paciente_id','nombre']].transpose().values))

df_s = pd.DataFrame(df['valor'].values,index=pd.MultiIndex.from_tuples(indexes, names=["paciente_id", "nombre"]),columns=['valor'])

df_s = df_s.unstack()
df_s.columns = df_s.columns.get_level_values(1)
df_s = df_s.transpose()

df_corr = df_s.corr()

RecomendadorMemoria.objects.all().delete()

for i,r in df_corr.iterrows():
    for n,x in r.iteritems():
        if int(n) != int(i):
            rec_reg = RecomendadorMemoria()
            rec_reg.user1 = int(i)
            rec_reg.user2 = int(n)
            rec_reg.similitud = x
            rec_reg.usado_nutricion = False
            rec_reg.usado_ejercicio = False
            rec_reg.save()