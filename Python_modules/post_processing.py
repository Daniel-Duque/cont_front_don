# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 09:00:50 2024

@author: usuario
"""

"""
Created on Thu Sep 19 09:00:50 2024

@author: usuario
"""

import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
n=0
project="warehouse-observatorio"
table="warehouse-observatorio.Secop.SapoError"
path=r"C:\Users\usuario\Documents\contract-transparency-copia\data\resultados"
model = SentenceTransformer('all-distilroberta-v1',device="cuda:0")
# 
# Function to perform semantic search
def semantic_search(prompt, df, model, top_k=1000):
    # Generate embeddings for the descriptions
    df['embeddings'] = df['Descripción del Procedimiento'].apply(lambda x: model.encode(x, convert_to_tensor=True))

    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    similarities = df['embeddings'].apply(lambda x: util.pytorch_cos_sim(prompt_embedding, x).item())
    df['similarity'] = similarities
    return df

# Example search prompt
prompt = "contratar con medios de comunicación"




for i in os.listdir(path):
    print(i)
    if i[0:12]=="col_tria_err":
        if n==0:
            data=pd.read_excel(path+r"/"+i)
            #data=semantic_search(prompt, data, model)
            n+=1
        else:
            data1=pd.read_excel(path+r"/"+i)
            #data1=semantic_search(prompt, data1, model)
            data=pd.concat([data,data1])
            

data["Descripción del Procedimiento"] = data["Descripción del Procedimiento"].str.replace('\\r\\n', ' ', regex=True)
data["Nombre del Procedimiento"] = data["Nombre del Procedimiento"].str.replace('\\r\\n', ' ', regex=True)
data=data.drop(["Unnamed: 0.1","Unnamed: 0"],axis=1)
data=data.drop(['embeddings'],axis=1)

# Initialize the model


data.to_csv(path+r"/"+"compilado_error.csv",index=False,encoding="latin-1",sep=';')