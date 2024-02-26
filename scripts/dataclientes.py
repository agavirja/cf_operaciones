import streamlit as st
import pandas as pd
from sqlalchemy import create_engine 

@st.cache_data
def dataclientes():
    
    user     = st.secrets["user_cf_pdfcf"]
    password = st.secrets["password_cf_pdfcf"]
    host     = st.secrets["host_cf_pdfcf"]
    schema   = st.secrets["schema_cf_pdfcf"]
    
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
    data   = pd.read_sql_query(f"SELECT codigo,nombre,nacionalidad,tipoid,numeroid,pasaporte,nie,created_at FROM {schema}.cj_clientes" , engine)
    engine.dispose()
    return data
    

@st.cache_data
def datacliente(cj_clientes_codigo,codigo_proyecto=None):
    
    user     = st.secrets["user_cf_pdfcf"]
    password = st.secrets["password_cf_pdfcf"]
    host     = st.secrets["host_cf_pdfcf"]
    schema   = st.secrets["schema_cf_pdfcf"]

    #-------------------------------------------------------------------------#
    # Datos del cliente
    engine        = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
    datacliente   = pd.read_sql_query(f"SELECT * FROM {schema}.cj_clientes WHERE codigo='{cj_clientes_codigo}'" , engine)
    
    consulta = ""
    if codigo_proyecto is not None and codigo_proyecto!='':
        consulta = f" AND codigo_proyecto='{codigo_proyecto}'"
    dataproyectos = pd.read_sql_query(f"SELECT codigo_proyecto,cj_clientes_codigo FROM {schema}.cj_proyecto_cliente WHERE cj_clientes_codigo='{cj_clientes_codigo}' {consulta}" , engine)

    #-------------------------------------------------------------------------#
    # Co-inversionistas
    lista = list(dataproyectos['codigo_proyecto'].unique())
    query = "','".join(lista)
    query = f" codigo_proyecto IN ('{query}')"
    dataproyectoscoinv   = pd.read_sql_query(f"SELECT cj_clientes_codigo as codigo FROM {schema}.cj_proyecto_cliente WHERE {query}" , engine)
    dataproyectoscoinv   = dataproyectoscoinv[dataproyectoscoinv['codigo']!=cj_clientes_codigo]
    datacoinversionistas = pd.DataFrame()
    if not dataproyectoscoinv.empty:
        query = "','".join(dataproyectoscoinv['codigo'].unique())
        query = f" codigo IN ('{query}')"
        datacoinversionistas = pd.read_sql_query(f"SELECT * FROM {schema}.cj_clientes WHERE {query}" , engine)
        
    lista = list(dataproyectos['codigo_proyecto'].unique())
    query = "','".join(lista)
    query = f" codigo_proyecto IN ('{query}')"

    #-------------------------------------------------------------------------#
    # Contrato
    datacontrato = pd.read_sql_query(f"SELECT * FROM {schema}.cj_contrato WHERE {query}" , engine)
    #-------------------------------------------------------------------------#
    # PBC
    datapbc = pd.read_sql_query(f"SELECT * FROM {schema}.cj_pbc WHERE {query} AND cj_clientes_codigo='{cj_clientes_codigo}'" , engine)
    #-------------------------------------------------------------------------#
    # Tipo de inversionista
    datatipoinversionista = pd.read_sql_query(f"SELECT * FROM {schema}.cj_tipoinversionista WHERE {query} AND cj_clientes_codigo='{cj_clientes_codigo}'" , engine)
    #-------------------------------------------------------------------------#
    # Proyectos
    dataproyectos = pd.read_sql_query(f"SELECT * FROM {schema}.cj_proyecto WHERE {query}" , engine)
    #-------------------------------------------------------------------------#
    # NIE
    datanie = pd.read_sql_query(f"SELECT * FROM {schema}.cj_nie WHERE {query} AND cj_clientes_codigo='{cj_clientes_codigo}'" , engine)
    #-------------------------------------------------------------------------#
    # SL
    datasl = pd.read_sql_query(f"SELECT * FROM {schema}.cj_sl WHERE {query} AND cj_clientes_codigo='{cj_clientes_codigo}'" , engine)
    #-------------------------------------------------------------------------#
    # Cuenta Bancaria
    datacuentabancaria = pd.read_sql_query(f"SELECT * FROM {schema}.cj_cuenta_bancaria WHERE {query} AND cj_clientes_codigo='{cj_clientes_codigo}'" , engine)
    #-------------------------------------------------------------------------#
    # Financiacion
    datafinanciacion = pd.read_sql_query(f"SELECT * FROM {schema}.cj_financiacion WHERE {query} AND cj_clientes_codigo='{cj_clientes_codigo}'" , engine)
    #-------------------------------------------------------------------------#
    # Configuracion
    dataconfiguracion = pd.read_sql_query(f"SELECT * FROM {schema}.cj_configuracion WHERE {query} AND cj_clientes_codigo='{cj_clientes_codigo}'" , engine)

    engine.dispose()

    return datacliente,dataproyectos,datacoinversionistas,datatipoinversionista,datacontrato,datapbc,dataproyectos,datanie,datasl,datacuentabancaria,datafinanciacion,dataconfiguracion


@st.cache_data
def datainfocliente(cj_clientes_codigo):
    
    user     = st.secrets["user_cf_pdfcf"]
    password = st.secrets["password_cf_pdfcf"]
    host     = st.secrets["host_cf_pdfcf"]
    schema   = st.secrets["schema_cf_pdfcf"]
    
    #-------------------------------------------------------------------------#
    # Datos del cliente
    engine        = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
    datacliente   = pd.read_sql_query(f"SELECT * FROM {schema}.cj_clientes WHERE codigo='{cj_clientes_codigo}'" , engine)
    engine.dispose()

    return datacliente
