#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:53:27 2024

@author: dduque
"""

import pandas as pd
import os
import geopandas as gp
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers import util

def semantic_search(prompt, df, model, top_k=1000):
    # Generate embeddings for the descriptions
    df['embeddings'] = df['Descripcion del Proceso'].apply(lambda x: model.encode(x, convert_to_tensor=True))

    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    similarities = df['embeddings'].apply(lambda x: util.pytorch_cos_sim(prompt_embedding, x).item())
    df['similarity'] = similarities
    return df

def extrange_calc(vhat,ehat,v):
    if v>max(vhat,(vhat*(1+ehat))):
        return(v/max(vhat,(vhat*(1+ehat))))
    elif v<min(vhat,(vhat*(1+ehat))):
        return v/min(vhat,(vhat*(1+ehat)))
    else:
        return 0
model = SentenceTransformer("tomaarsen/static-similarity-mrl-multilingual-v1")
filtrado1=pd.read_csv(r"data/compilado_error.csv",encoding="utf-8",sep=";")

extrange="Tamaño valor extraño"
filtrado1=filtrado1.rename(columns={"predict": "Valor Proyectado",
                                    "value_thousand_dolar": "Valor real",
                                    "likelihood":"Similitud de valor",
                                    "similarity":"Contrato relacionado con publicidad"}
                           ).drop_duplicates(["URLProceso"])


filtrado1["exchange_rate"]=filtrado1["exchange_rate"]/1000
filtrado1["Valor Proyectado"]=filtrado1["Valor Proyectado"]*filtrado1["exchange_rate"]
filtrado1["Valor real"]=filtrado1["Valor real"]*filtrado1["exchange_rate"]
filtrado1[extrange]=filtrado1.apply(lambda row: extrange_calc(
    row["Valor Proyectado"],row['predicterr'],row["Valor real"]),axis=1)
filtrado1[extrange]=abs(2-filtrado1["Similitud de valor"])
filtrado1["range-"]=filtrado1["exchange_rate"]*filtrado1["Valor Proyectado"]/2
filtrado1["veces la predicción"]=(filtrado1["Valor real"]/filtrado1["Valor Proyectado"])
filtrado1["Departamento Entidad"]=filtrado1["Departamento"].apply(str.upper)
filtrado1["Ciudad Entidad"]=filtrado1["Ciudad"].apply(str.upper)
unique_dept=pd.unique(filtrado1["Departamento Entidad"])
unique_cities=pd.unique(filtrado1["Ciudad Entidad"])
unique_sector=pd.unique(filtrado1["Tipo de Contrato"])
filtrado1=filtrado1.sort_values(extrange,ascending=True)
nombres= ["Nombre Entidad",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor",
                     "veces la predicción"]
##agrupado por entidad
filtrado1[nombres].groupby(["Nombre Entidad"]).sum().to_csv(r"data/groupedent.csv")
#agrupado por ciudad
filtrado1[nombres+["veces la predicción","Ciudad Entidad","Departamento Entidad"]].groupby(["Ciudad Entidad","Departamento Entidad"]).sum().to_csv(r"data/groupedcit.csv")

#similar al comunicación
comu=pd.DataFrame()
for i in range(0,40):
    prompt = "Pauta | Publicidad | Prensa | Periodismo | Periodista | Divulgación | Multimedia publicitaria | Redes Sociales | propaganda en Televisión | publicidad en Radio | cuña Radial | Periódico |propaganda Audiovisual | Video | Revista | Comunicaciones divulgativas"

    filtrado2=filtrado1[50000*i:50000*(i+1)][["Nombre Entidad","Descripcion del Proceso","Tipo de Contrato","Género Representante Legal",
                         "Valor real","Valor Proyectado","Duración del contrato",extrange,"Similitud de valor","veces la predicción","URLProceso",]]
    
    
    
    filtrado2=semantic_search(prompt,filtrado2,model)
    filtrado2=filtrado2[filtrado2['similarity']>0.3]
    filtrado2=filtrado2.drop(['embeddings'],axis=1)
    filtrado2.to_csv(r"data/cleaned"+str(i)+".csv")
    if i==0:
        comu=filtrado2
        
    else:
        comu=pd.concat([comu,filtrado2])
    comu.to_csv(r"data/cleanedcomu.csv")
    print(i)

linksave=r"data/particular"
def carga_multiple(filtrado1,linksave):
    print(i)
    df=filtrado1
    gb = df.groupby(["Departamento Entidad","Ciudad Entidad"])    
    for x in gb.groups:
        print(x)
        subdata=gb.get_group(x)
        partitions=len(subdata)//5000
        for part in range(0,partitions+1):
            saving_place=linksave+"//"+x[0].upper()+"-"+x[1].upper()+str(part)+".csv"
            subdata[part*5000:(part+1)*5000].to_csv(saving_place)
            """
            try:
                
                updating_data=pd.read_csv(saving_place)
                pd.concat([updating_data,updating_data]).to_csv(saving_place)
            except FileNotFoundError:
                subdata.to_csv(saving_place)    
            """
carga_multiple(filtrado1,linksave)