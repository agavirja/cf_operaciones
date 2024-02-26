import streamlit as st
import pandas as pd
from sqlalchemy import create_engine 

@st.cache_data
def dataproyectos():
    
    user     = st.secrets["user_cf_pdfcf"]
    password = st.secrets["password_cf_pdfcf"]
    host     = st.secrets["host_cf_pdfcf"]
    schema   = st.secrets["schema_cf_pdfcf"]

    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
    data   = pd.read_sql_query(f"SELECT * FROM {schema}.cj_proyecto" , engine)
    engine.dispose()
    return data
