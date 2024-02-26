import streamlit as st
import re
import time
import pandas as pd
import pymysql
import hashlib
import boto3
import streamlit.components.v1 as components
from sqlalchemy import create_engine 
from datetime import datetime

from scripts.dataproyectos import dataproyectos
from modulos.display_proyectos import main as display_proyectos

def main():
    
    data = dataproyectos()
    data.index = range(len(data))
    idd = data.index>=0
    
    st.write('Filtros')
    col1,col2,col3 = st.columns(3)
    with col1: 
        options = sorted(data[data['codigo_proyecto'].notnull()]['codigo_proyecto'].unique())
        options = ['Todos'] + options
        codigo_proyecto = st.selectbox('Por Código', options=options)
        if 'todos' not in codigo_proyecto.lower():
            idd = (idd) & (data['codigo_proyecto']==codigo_proyecto)
                
    with col2:
        options = sorted(data[data['nombre_proyecto'].notnull()]['nombre_proyecto'].unique())
        options = ['Todos'] + options
        nombre_proyecto = st.selectbox('Por Nombre del Proyecto', options=options)
        if 'todos' not in nombre_proyecto.lower():
            idd = (idd) & (data['nombre_proyecto']==nombre_proyecto)
            
    with col3: 
        options = sorted(data[data['pais'].notnull()]['pais'].unique())
        options = ['Todos'] + options
        pais = st.selectbox('Por País', options=options)
        
        if 'todos' not in pais.lower():
            idd = (idd) & (data['pais']==pais)
            
    col1,col2,col3 = st.columns(3)
    with col1: 
        options = sorted(data[data['direccion'].notnull()]['direccion'].unique())
        options = ['Todos'] + options
        direccion = st.selectbox('Por Dirección', options=options)
        if 'todos' not in direccion.lower():
            idd = (idd) & (data['direccion']==direccion)
        
    with col2: 
        options = sorted(data[data['ciudad'].notnull()]['ciudad'].unique())
        options = ['Todos'] + options
        ciudad = st.selectbox('Por Ciudad', options=options)

        if 'todos' not in ciudad.lower():
            idd = (idd) & (data['ciudad']==ciudad)
            
    with col3: 
        options = ['Todos'] + ['Si','No'] 
        activos = st.selectbox('Activos', options=options)

    display_proyectos(data[idd],titulo='Proyectos')