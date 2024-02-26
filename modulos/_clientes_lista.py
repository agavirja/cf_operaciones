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

from scripts.dataclientes import dataclientes
from modulos.display_clientes import display_clientes

def main():
    
    data = dataclientes()
    data.index = range(len(data))
    idd = data.index>=0
    
    st.write('---')
    st.write('Filtros')
    col1,col2,col3,col4 = st.columns(4)
    with col1: 
        options = sorted(data[data['nombre'].notnull()]['nombre'].unique())
        options = ['Todos'] + options
        nombre = st.selectbox('Por Nombre', options=options)
        if 'todos' not in nombre.lower():
            idd = (idd) & (data['nombre']==nombre)
                
    with col2:
        options = sorted(data[data['numeroid'].notnull()]['numeroid'].unique())
        options = ['Todos'] + options
        numeroid = st.selectbox('Por Identificacion', options=options)
        if 'todos' not in numeroid.lower():
            idd = (idd) & (data['numeroid']==numeroid)
            
    with col3: 
        options = sorted(data[data['pasaporte'].notnull()]['pasaporte'].unique())
        options = ['Todos'] + options
        pasaporte = st.selectbox('Por Pasaporte', options=options)
        
        if 'todos' not in pasaporte.lower():
            idd = (idd) & (data['pasaporte']==pasaporte)
            
    with col4: 
        options = sorted(data[data['nie'].notnull()]['nie'].unique())
        options = ['Todos'] + options
        nie = st.selectbox('Por NIE', options=options)

        if 'todos' not in nie.lower():
            idd = (idd) & (data['nie']==nie)
        
    display_clientes(data[idd],titulo='Clientes')
