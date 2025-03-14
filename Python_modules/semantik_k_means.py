#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 14:18:14 2025

@author: daniel
"""


import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import datetime
today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)
month=last_month.strftime('%Y-%m')
url="https://www.datos.gov.co/resource/jbjy-vk9h.json?$limit=10000000&fecha_de_firma="+month

def semantic_k(prompt, df, model,similitud_min=0.4,k=20 ):
    # Generate embeddings for the descriptions
    df['embeddings'] = df['descripcion_del_proceso'].apply(lambda x: model.encode(x, convert_to_tensor=True))
    print("a")
    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    similarities = df['embeddings'].apply(lambda x: util.pytorch_cos_sim(prompt_embedding, x).item())
    df['similarity'] = similarities
    accept=df[df['similarity'] >similitud_min].sort_values("similarity",ascending=False).iloc[0:k+1]
    accept=accept[1:]
    valor="valor_del_contrato"
    mean=accept[valor].mean()
    desv=accept[valor].std()
    kurt=accept[valor].kurtosis()
    
    return mean,desv,kurt,accept

model = SentenceTransformer('tomaarsen/static-similarity-mrl-multilingual-v1')
prompt = "construcción de hospitales"
#data1=pd.read_csv(r"data/compilado_error.csv",encoding="utf-8",delimiter=";")
data1=pd.read_json(url)
df=data1
mean,desv,kurt,accept=semantic_k(prompt, df, model,k=60)
accept["valor_del_contrato"].hist(bins=100)
rangop=mean+desv-kurt
rangon=max(mean-desv-kurt,0)