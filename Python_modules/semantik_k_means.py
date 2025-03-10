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

def semantic_search(prompt, df, model, top_k=1000):
    # Generate embeddings for the descriptions
    df['embeddings'] = df['Descripcion del Proceso'].apply(lambda x: model.encode(x, convert_to_tensor=True))

    prompt_embedding = model.encode(prompt, convert_to_tensor=True)
    similarities = df['embeddings'].apply(lambda x: util.pytorch_cos_sim(prompt_embedding, x).item())
    df['similarity'] = similarities
    return df



data1=pd.read_csv(r"data/compilado_error.csv",encoding="utf-8",delimiter=";")