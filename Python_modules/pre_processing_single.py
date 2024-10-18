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
filtrado1=pd.read_csv(
    r"data/compilado_error (1).csv",encoding="latin-1",sep=";")

extrange="Tamaño valor extraño"
filtrado1=filtrado1.rename(columns={"predict": "Valor Proyectado",
                                    "value_thousand_dolar": "Valor real",
                                    "likelihood":"Similitud de valor",
                                    "similarity":"Contrato relacionado con publicidad"})


filtrado1["exchange_rate"]=filtrado1["exchange_rate"]/1000
filtrado1["Valor Proyectado"]=filtrado1["Valor Proyectado"]*filtrado1["exchange_rate"]
filtrado1["Valor real"]=filtrado1["Valor real"]*filtrado1["exchange_rate"]
filtrado1[extrange]=(filtrado1["perc_error"]-filtrado1["predicterr"])*filtrado1["Valor real"]
filtrado1["range-"]=filtrado1["exchange_rate"]*filtrado1["Valor Proyectado"]/2
filtrado1["veces la predicción"]=(filtrado1["Valor real"]/filtrado1["Valor Proyectado"])
filtrado1["Departamento Entidad"]=filtrado1["Departamento Entidad"].apply(str.upper)
filtrado1["Ciudad Entidad"]=filtrado1["Ciudad Entidad"].apply(str.upper)
unique_dept=pd.unique(filtrado1["Departamento Entidad"])
unique_cities=pd.unique(filtrado1["Ciudad Entidad"])
unique_sector=pd.unique(filtrado1["Tipo de Contrato"])
filtrado1=filtrado1.sort_values(extrange,ascending=False)
##agrupado por entidad
filtrado1[["Entidad",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor",
                     "veces la predicción"]].groupby(["Entidad"]).sum().to_csv(r"data/groupedent.csv")
#agrupado por ciudad
filtrado1[["Entidad",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor",
                     "veces la predicción","Ciudad Entidad","Departamento Entidad"]].groupby(["Ciudad Entidad","Departamento Entidad"]).sum().to_csv(r"data/groupedcit.csv")
#similar al comunicación
filtrado1[["Entidad","Descripción del Procedimiento","Tipo de Contrato",
                     "Valor real","Valor Proyectado",extrange,"Similitud de valor",
                     "veces la predicción","Contrato relacionado con publicidad","URLProceso" ]][filtrado1["Contrato relacionado con publicidad"]>0.65].to_csv(r"data/cleanedcomu"+".csv")


for i in range(0,15):
    filtrado1[50000*i:50000*(i+1)][["Entidad","Descripción del Procedimiento","Tipo de Contrato",
                         "Valor real","Valor Proyectado",extrange,"Similitud de valor","veces la predicción","URLProceso",]].to_csv(r"data/cleaned"+str(i)+".csv")

linksave=r"data/particular"
def carga_multiple(filtrado1,linksave):
    print(i)
    df=filtrado1
    gb = df.groupby(["Departamento Entidad","Ciudad Entidad"])    
    for x in gb.groups:
        print(x)
        subdata=gb.get_group(x)
        saving_place=linksave+"//"+x[0].upper()+"-"+x[1].upper()+".csv"
        try:
            
            updating_data=pd.read_csv(saving_place)
            pd.concat([updating_data,updating_data]).to_csv(saving_place)
        except FileNotFoundError:
            subdata.to_csv(saving_place)    
carga_multiple(filtrado1,linksave)