import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from datetime import datetime

user     = st.secrets["user_cf_pdfcf"]
password = st.secrets["password_cf_pdfcf"]
host     = st.secrets["host_cf_pdfcf"]
schema   = st.secrets["schema_cf_pdfcf"]
    
def updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,tabla,data,userchange,key):
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar',key=key):
            with st.spinner('Guardando'):
                variables  = list(inputvar)
                var2change = '`'+'`=%s, `'.join(variables) +'`=%s'
                
                condicion  = ''
                if codigo_cliente is not None and codigo_cliente!='':
                    inputvar.update({codigo_name:codigo_cliente})
                    condicion += f'AND `{codigo_name}` = %s'
                if  codigo_proyecto is not None and codigo_proyecto!='':
                    inputvar.update({'codigo_proyecto':codigo_proyecto})
                    condicion += 'AND `codigo_proyecto` = %s'
                if condicion!='':
                    condicion = condicion.strip('AND').strip()
                
                datachange = pd.DataFrame([inputvar])
                conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=schema)
                with conn.cursor() as cursor:
                    sql = f"UPDATE {tabla} SET {var2change} WHERE {condicion}"
                    list_of_tuples = datachange.to_records(index=False).tolist()
                    cursor.executemany(sql, list_of_tuples)
                conn.commit()
                conn.close() 
                
                update_historico(inputvar,codigo_cliente,codigo_proyecto,tabla,data,userchange)
                
                st.cache_data.clear()
                st.rerun()
               
def updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,tabla,data,userchange):
    with st.spinner('Guardando'):
        variables  = list(inputvar)
        var2change = '`'+'`=%s, `'.join(variables) +'`=%s'
        
        condicion  = ''
        if codigo_cliente is not None and codigo_cliente!='':
            inputvar.update({codigo_name:codigo_cliente})
            condicion += f'AND `{codigo_name}` = %s'
        if  codigo_proyecto is not None and codigo_proyecto!='':
            inputvar.update({'codigo_proyecto':codigo_proyecto})
            condicion += 'AND `codigo_proyecto` = %s'
        if condicion!='':
            condicion = condicion.strip('AND').strip()
            
        datachange = pd.DataFrame([inputvar])
        conn = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            sql = f"UPDATE {tabla} SET {var2change} WHERE {condicion}"
            list_of_tuples = datachange.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        conn.commit()
        conn.close() 
        
        update_historico(inputvar,codigo_cliente,codigo_proyecto,tabla,data,userchange)
        
        st.cache_data.clear()
        st.rerun()
        
        
def update_historico(inputvar,codigo_cliente,codigo_proyecto,tabla,data,userchange):
    dataupdate = data.copy()
    for key,value in inputvar.items():
        if key in dataupdate:
            dataupdate[key] = value
    dataexport = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,
                                'codigo_proyecto':codigo_proyecto,
                                'tabla':tabla,
                                'updated_at':datetime.now().strftime('%Y-%m-%d'),
                                'userchange':userchange,
                                'json':pd.io.json.dumps(dataupdate, orient='records')}])
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
    dataexport.to_sql('cj_historic_update',engine,if_exists='append', index=False)
    engine.dispose()