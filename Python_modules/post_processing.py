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
path=r"/data"
model = SentenceTransformer('all-distilroberta-v1')
# 
# Function to perform semantic search
def semantic_search(prompt, df, model, top_k=1000):
    # Generate embeddings for the descriptions
    df['embeddings'] = df['Descripción del Proceso'].apply(lambda x: model.encode(x, convert_to_tensor=True))

    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    similarities = df['embeddings'].apply(lambda x: util.pytorch_cos_sim(prompt_embedding, x).item())
    df['similarity'] = similarities
    return df

# Example search prompt
prompt = "contratar con medios de comunicación"





data1=pd.read_csv(r"/home/dduque/Documents/GitHub/cont_front_don/data/compilado_error.csv",encoding="utf-8",delimiter=";")
data=semantic_search(prompt, data1, model)

            

data["Descripción del Procedimiento"] = data["Descripción del Procedimiento"].str.replace('\\r\\n', ' ', regex=True)
data["Nombre del Procedimiento"] = data["Nombre del Procedimiento"].str.replace('\\r\\n', ' ', regex=True)

data=data.drop(['embeddings'],axis=1)

# Initialize the model


data.to_csv(path+r"/"+"compilado_error2.csv",index=False,encoding="latin-1",sep=';')