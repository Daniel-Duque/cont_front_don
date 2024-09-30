#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:53:27 2024

@author: dduque
"""

import pandas as pd
import os
import geopandas as gp

filtrado1=pd.read_csv(
    r"data/compilado_error.csv",encoding="latin-1",sep=";")


filtrado1=filtrado1.rename(columns={"predict": "Valor Proyectado", "value_thousand_dolar": "Valor real","likelihood":"Similitud de valor"})
extrange="Tamaño valor extraño"
filtrado1["exchange_rate"]=filtrado1["exchange_rate"]/1000000
filtrado1[extrange]=(filtrado1["perc_error"]-filtrado1["predicterr"])
filtrado1["range-"]=filtrado1["exchange_rate"]*filtrado1["Valor Proyectado"]/2
filtrado1["veces la predicción"]=filtrado1["Valor real"]/filtrado1["Valor Proyectado"]
filtrado1["Departamento Entidad"]=filtrado1["Departamento Entidad"].apply(str.upper)
filtrado1["Ciudad Entidad"]=filtrado1["Ciudad Entidad"].apply(str.upper)
unique_dept=pd.unique(filtrado1["Departamento Entidad"])
unique_cities=pd.unique(filtrado1["Ciudad Entidad"])
unique_sector=pd.unique(filtrado1["Tipo de Contrato"])
filtrado1.to_csv(r"data/cleaned.csv")
filtrado1[0:50000].to_csv(r"data/cleaned1.csv")
filtrado1[50000:].to_csv(r"data/cleaned2.csv")