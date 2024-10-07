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

extrange="Tamaño valor extraño"
filtrado1=filtrado1.rename(columns={"predict": "Valor Proyectado", "value_thousand_dolar": "Valor real","likelihood":"Similitud de valor"})


filtrado1["exchange_rate"]=filtrado1["exchange_rate"]/1000
filtrado1["Valor Proyectado"]=filtrado1["Valor Proyectado"]*filtrado1["exchange_rate"]
filtrado1["Valor real"]=filtrado1["Valor real"]*filtrado1["exchange_rate"]
filtrado1[extrange]=(filtrado1["perc_error"]-filtrado1["predicterr"])*filtrado1["Valor real"]
filtrado1["range-"]=filtrado1["exchange_rate"]*filtrado1["Valor Proyectado"]/2
filtrado1["veces la predicción"]=filtrado1["Valor real"]/filtrado1["Valor Proyectado"]
filtrado1["Departamento Entidad"]=filtrado1["Departamento Entidad"].apply(str.upper)
filtrado1["Ciudad Entidad"]=filtrado1["Ciudad Entidad"].apply(str.upper)
unique_dept=pd.unique(filtrado1["Departamento Entidad"])
unique_cities=pd.unique(filtrado1["Ciudad Entidad"])
unique_sector=pd.unique(filtrado1["Tipo de Contrato"])
filtrado1=filtrado1.sort_values(extrange,ascending=False)

filtrado1[0:50000][["Entidad","Descripción del Procedimiento","Tipo de Contrato",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor","veces la predicción"]].to_csv(r"data/cleaned1.csv")
filtrado1[50000:][["Entidad","Descripción del Procedimiento","Tipo de Contrato",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor","veces la predicción"]].to_csv(r"data/cleaned2.csv")
filtrado1[["Entidad","Tipo de Contrato",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor",
                     "veces la predicción"]].groupby(["Entidad"]).sum().to_csv(r"data/groupedent.csv")
filtrado1[["Entidad","Tipo de Contrato",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor",
                     "veces la predicción","Ciudad Entidad","Departamento Entidad"]].groupby(["Ciudad Entidad","Departamento Entidad"]).sum().to_csv(r"data/groupedcit.csv")