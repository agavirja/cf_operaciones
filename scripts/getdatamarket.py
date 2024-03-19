import streamlit as st
import pandas as pd
from sqlalchemy import create_engine 

@st.cache_data
def datamarket(inputvar,polygon=None):
    
    user     = st.secrets["user_cf_pdfcf"]
    password = st.secrets["password_cf_pdfcf"]
    host     = st.secrets["host_cf_pdfcf"]
    schema   = "pdfcf"
    
    preciocompramax = inputvar['preciocompra'] if 'preciocompra' in inputvar and (isinstance(inputvar['preciocompra'], float) or isinstance(inputvar['preciocompra'], int)) and inputvar['preciocompra']>0 else None
    superficiereal  = inputvar['superficiereal'] if 'superficiereal' in inputvar and (isinstance(inputvar['superficiereal'], float) or isinstance(inputvar['superficiereal'], int)) and inputvar['superficiereal']>0 else None

    query = ""
    if preciocompramax is not None:
        query += f" AND precio<={preciocompramax*1.05}"
    if superficiereal is not None:
        query += f" AND area>={superficiereal*0.95}"
    
    if isinstance(polygon, str):
        query += f" AND ST_CONTAINS(ST_GEOMFROMTEXT('{polygon}'), POINT(`longitud`,`latitud`))"
        
    if query!="":
        query = query.strip().strip('AND')
        query = f' WHERE tipo_operacion="venta" AND {query} '
            
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
    data   = pd.read_sql_query(f"SELECT * FROM {schema}.data_idealista {query}" , engine)
    engine.dispose()
    return data