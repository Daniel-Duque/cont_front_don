#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:37:14 2024

@author: dduque
"""

import pandas as pd
import os
import geopandas as gp


import streamlit as st
link=r"C:\Users\usuario\Documents\contract-transparency-copia\data\resultados"

def carga_multiple(link):
    for i in os.listdir(link):
        if "col_tri" in i:
            df=pd.read_excel(link+"/"+i)
            gb = df.groupby("Ciudad Entidad")    
            a=[gb.get_group(x) for x in gb.groups]

st.set_page_config(layout='wide')


filtrado1=pd.read_csv(
    r"data/col_tria.csv",delimiter=";")


filtrado1=filtrado1.rename(columns={"predict": "Valor Proyectado", "value_thousand_dolar": "Valor real","likelihood":"Similitud de valor"})
extrange="Tamaño valor extraño"
filtrado1["exchange_rate"]=filtrado1["exchange_rate"]/1000000
filtrado1[extrange]=(filtrado1["Valor real"]-filtrado1["Valor Proyectado"]*2)*filtrado1["exchange_rate"]
filtrado1["range-"]=filtrado1["exchange_rate"]*filtrado1["Valor Proyectado"]/2
filtrado1["veces la predicción"]=filtrado1["Valor real"]/filtrado1["Valor Proyectado"]
filtrado1["Departamento Entidad"]=filtrado1["Departamento Entidad"].apply(str.upper)
filtrado1["Ciudad Entidad"]=filtrado1["Ciudad Entidad"].apply(str.upper)
unique_dept=pd.unique(filtrado1["Departamento Entidad"])
unique_cities=pd.unique(filtrado1["Ciudad Entidad"])
unique_sector=pd.unique(filtrado1["Tipo de Contrato"])
def save_particular_files():
    for dept in unique_dept:
        filtrado2=filtrado1[filtrado1["Departamento Entidad"]==dept]
        for citie in unique_cities:
            filtrado3=filtrado2[filtrado2["Ciudad Entidad"]==citie]
            if not filtrado3.empty:
                filtrado3.to_csv(r"data/particular/"+dept+"-"+citie+".csv")


def agroupationing():
    subset=filtrado1[["Ciudad Entidad","Departamento Entidad","Fecha",
                      "Valor real","Valor Proyectado",extrange,
                      "Similitud de valor","veces la predicción"]]
    subset.groupby(["Ciudad Entidad","Departamento Entidad","Fecha"]).sum().to_csv(r"data/grouped.csv")

def main():
    save_particular_files()
    agroupationing()

if __name__ == "__main__":
    main()
df = geopandas.read_file(r"data/maps/MGN_MPIO_POLITICO.shp")  
