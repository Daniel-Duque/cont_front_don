#Original From Daniel Duque Lozano
# -*- coding: utf-8 -*-
"""analisis_territorial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AQnWOCqJUWkHUKJg-HgLbDXsLa72uWoS
"""


import pandas as pd
import os



import streamlit as st

import datetime
st.set_page_config(layout='wide')


filtrado1=pd.read_csv(r"data/dicc/Ciudades.csv").sort_values(["Departamento Entidad","Ciudad Entidad"],ascending=False)

extrange="Tamaño valor extraño"

resulting=pd.read_csv(r"data/cleaned0.csv")

st.title("Banderas rojas contratación pública preliminar (valores en millones de pesos)")
pd.set_option("styler.render.max_elements", 8600000)
tab0,tab1= st.tabs(["Corrupción cero","comunicación"])

    
agroupados=pd.read_csv(r"data/groupedcit.csv")


today = datetime.datetime.now()
year = today.year 
jan_1 = datetime.date(year-1, 1, 1)
dec_31 = datetime.date(year, 12, 31)




with tab0:
  
    if "app_runs" not in st.session_state:
        st.session_state.app_runs = 0
        st.session_state.fragment_runs = 0
    @st.fragment
    def select_df():
        st.session_state.fragment_runs += 1
        depto=st.selectbox("Departamento Entidad",
                           pd.unique(filtrado1["Departamento Entidad"]),key=2)
        muni=st.selectbox("Ciudad Entidad",
                           pd.unique(filtrado1[filtrado1["Departamento Entidad"]==depto]["Ciudad Entidad"]),key=3)
        #text search taken from https://blog.streamlit.io/create-a-search-engine-with-streamlit-and-google-sheets/
    
    
    
        on = st.toggle("Opciones extra")
        text_search=""
        ini=jan_1
        fini=dec_31
        
        if on:
            text_search = st.text_input("Busca contratos en tu ciudad.", value="")
    
            
            d = st.date_input(
                "",
                (jan_1, datetime.date(year, 1, 7)),
                jan_1,
                dec_31,
                format="MM.DD.YYYY",
            )
            ini=d[0]
            try:
                fini=d[1]
            except:
                ...
        linksave=r"data/particular"
        try:
            terri=pd.read_csv(linksave+"//"+depto.upper()+"-"+muni.upper()+"0"+".csv")[["Nombre Entidad",
                    "Descripcion del Proceso","Valor real","Valor Proyectado",extrange,"Tipo de Contrato","Fecha de Firma",
                    "URLProceso"]]
        except Exception as e:
            st.error('No encontramos contratos para este municipio en los periodos que se tienen en cuenta', icon="🚨")
            return False
        terri["Fecha de Firma"]=pd.to_datetime(terri["Fecha de Firma"], format='%m/%d/%Y').dt.date
        terri=terri[terri["Fecha de Firma"]>ini]
        terri=terri[terri["Fecha de Firma"]<=fini]            
        m1 = terri["Descripcion del Proceso"].str.lower().str.contains(text_search,case=False)
        terri[extrange]=terri[extrange].abs()
        terri=terri.sort_values(extrange,ascending=True)
        df_search = terri[m1]
        if df_search.empty:
            st.error('No encontramos contratos para este municipio en los periodos que se tienen en cuenta', icon="🚨")
        elif text_search:
            st.dataframe(df_search.style.background_gradient(axis=None, cmap="Reds"), 
                         column_config={
                extrange: st.column_config.BarChartColumn(
                    extrange,
                    help="Que tan extraño nos parece el contrato según nuestras métricas",
                    y_min=0,
                    y_max=1,
                ),
            },
            hide_index=True,)
        else:
            st.dataframe(terri.style.background_gradient(axis=None, cmap="Reds"), 
                         column_config={
                extrange: st.column_config.BarChartColumn(
                    extrange,
                    help="Que tan extraño nos parece el contrato según nuestras métricas",
                    y_min=0,
                    y_max=2,
                ),
            },
            hide_index=True,) 
    
    select_df()
 

with tab1:
  
    
    
    
    resultingcom=pd.read_csv(r"data/cleanedcomu"+".csv")   
    resulting[extrange]=resulting[extrange].abs()
    resulting=resulting.sort_values(extrange,ascending=True)
    st.dataframe(resultingcom.style.background_gradient(axis=None, cmap="Reds"), 
                 column_config={
        extrange: st.column_config.BarChartColumn(
            extrange,
            help="Que tan extraño nos parece el contrato según nuestras métricas",
            y_min=0,
            y_max=1,
        ),
    },
    hide_index=True,)  