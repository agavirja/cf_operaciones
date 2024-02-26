import streamlit as st
import re
import json
import hashlib
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine 

from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from scripts.dataconfiguracion import dataconfiguracion

from modulos.update_tables import update_historico

user     = st.secrets["user_cf_pdfcf"]
password = st.secrets["password_cf_pdfcf"]
host     = st.secrets["host_cf_pdfcf"]
schema   = st.secrets["schema_cf_pdfcf"]

def main(codigo_cliente,datacliente,userchange):
    
    formato = {
               'crear_proyecto':False,
               }
    
    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
            
    nombre_cliente = datacliente['nombre'].iloc[0].replace(' ','_')
    fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    codigo_proyecto = generar_codigo(f'{nombre_cliente}{fecha_creacion}')
                    
    col1,col2,col3 = st.columns([2,2,1])
    with col1:
        options = ['España']
        pais =  st.selectbox('País de inversión',key='paisinversionnuevoproyecto',options=options)
    with col2:
        options = ['Madrid']
        ciudad  =  st.selectbox('Ciudad de la inversión',key='ciudadinversionnuevoproyecto',options=options)
    with col3:
        options = ["EUR", "USD", "COP", "MXN", "ARS", "CLP"]
        moneda = st.selectbox('moneda',key='monedainversionnuevoproyecto',options=options)
        
    col1,col2,col3 = st.columns([2,2,1])
    with col1:
        capital =  st.number_input('Capital disponible',key='capitalinversionnuevoproyecto',min_value=0,value=0)
    with col2:
        valorproyecto = st.number_input('Valor del proyecto',key='valorinversionnuevoproyecto',min_value=0,value=0)
    with col3:
        options = ['','Si','No']
        financiacion = st.selectbox('Financiación',key='financiacioninversionnuevoproyecto',options=options)

        
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar',key='creando_nuevo_proyecto'):
            with st.spinner('Guardando'):
                
                    # Nuevo proyecto
                engine       = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}') 
                inputvar     = {'codigo_proyecto':codigo_proyecto,'pais':pais,'ciudad':ciudad,'capital':capital,'valorproyecto':valorproyecto,'financiacion':financiacion,'moneda':moneda,'created_at':datetime.now().strftime('%Y-%m-%d')}
                dataproyecto = pd.DataFrame([inputvar])
                dataproyecto.to_sql('cj_proyecto', engine, if_exists='append', index=False, chunksize=1)
    
                    # Contrato
                datacontrato = pd.DataFrame([{'codigo_proyecto':codigo_proyecto,'pagorealizado':'No','created_at':datetime.now().strftime('%Y-%m-%d')}])
                datacontrato.to_sql('cj_contrato', engine, if_exists='append', index=False, chunksize=1)

                    # PBC
                datapbc = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,'codigo_proyecto':codigo_proyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                datapbc.to_sql('cj_pbc', engine, if_exists='append', index=False, chunksize=1)

                    # Clientes por proyecto 
                dataproyectocliente = pd.DataFrame([{'codigo_proyecto':codigo_proyecto,'cj_clientes_codigo':codigo_cliente,'created_at':datetime.now().strftime('%Y-%m-%d')}]) 
                dataproyectocliente.to_sql('cj_proyecto_cliente', engine, if_exists='append', index=False, chunksize=1)
                
                    # Tipo de inversionista
                datacoinversion = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,'codigo_proyecto':codigo_proyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                datacoinversion.to_sql('cj_tipoinversionista', engine, if_exists='append', index=False, chunksize=1)

                    # NIE
                datanie = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,'codigo_proyecto':codigo_proyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                datanie.to_sql('cj_nie', engine, if_exists='append', index=False, chunksize=1)

                    # SL
                datasl = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,'codigo_proyecto':codigo_proyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                datasl.to_sql('cj_sl', engine, if_exists='append', index=False, chunksize=1)
 
                    # Cuenta Bancaria
                datacuentabancaria = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,'codigo_proyecto':codigo_proyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                datacuentabancaria.to_sql('cj_cuenta_bancaria', engine, if_exists='append', index=False, chunksize=1)
  
                    # Financiacion
                datafinanciacion = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,'codigo_proyecto':codigo_proyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                datafinanciacion.to_sql('cj_financiacion', engine, if_exists='append', index=False, chunksize=1)
                 
                    # Configuracion
                dataconfig = pd.DataFrame([{'cj_clientes_codigo':codigo_cliente,'codigo_proyecto':codigo_proyecto,'json':json.dumps(dataconfiguracion()),'created_at':datetime.now().strftime('%Y-%m-%d')}])
                dataconfig.to_sql('cj_configuracion', engine, if_exists='append', index=False, chunksize=1)

                    # Historico
                resultado = []
                formato   = [{'tabla':'cj_proyecto','data':json.dumps(dataproyecto, orient='records')},
                             {'tabla':'cj_pbc','data':json.dumps(datapbc, orient='records')},
                             {'tabla':'cj_proyecto_cliente','data':json.dumps(dataproyectocliente, orient='records')},
                             {'tabla':'cj_tipoinversionista','data':json.dumps(datacoinversion, orient='records')}]
                for items in formato:
                    
                    resultado.append({'cj_clientes_codigo':codigo_cliente,
                                        'codigo_proyecto':codigo_proyecto,
                                        'tabla':items['tabla'],
                                        'updated_at':datetime.now().strftime('%Y-%m-%d'),
                                        'userchange':userchange,
                                        'json':items['data']})
                    
                dataexport = pd.DataFrame(resultado)
                engine     = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
                dataexport.to_sql('cj_historic_update',engine,if_exists='append', index=False)
                engine.dispose()
                
                st.success('Nuevo proyecto guardado exitosamente')
                engine.dispose()
                st.cache_data.clear()
                st.session_state.crear_proyecto = False
                st.rerun()
                    
def generar_codigo(x):
    hash_sha256 = hashlib.sha256(x.encode()).hexdigest()
    codigo      = hash_sha256[:6]
    return codigo
