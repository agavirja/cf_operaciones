import streamlit as st
import re
import json
import time
import pandas as pd
import pymysql
import hashlib
import boto3
import streamlit.components.v1 as components
from sqlalchemy import create_engine 
from datetime import datetime

from scripts.ciudades import ciudades
from scripts.doc2nube import doc2nube
from scripts.tipo_identidad import tipo_identidad
from scripts.tiposIdentidadEmpresarial import tiposIdentidadEmpresarial
from scripts.dataconfiguracion import dataconfiguracion

def main(codigoproyecto=None):
    
    user     = st.secrets["user_cf_pdfcf"]
    password = st.secrets["password_cf_pdfcf"]
    host     = st.secrets["host_cf_pdfcf"]
    schema   = st.secrets["schema_cf_pdfcf"]
    userchange = '0'
    
    st.write('---')
    codigo_inversionista,datacliente = formulario()
    datacliente['created_at'] = datetime.now().strftime('%Y-%m-%d')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar Cliente'):
            with st.spinner('Guardando cliente'):
            
                if not datacliente.empty:
                    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}') 
                    datacliente.to_sql('cj_clientes', engine, if_exists='append', index=False, chunksize=1)

                    # Crear cliente en tablas
                    
                        # codigo proyecto
                    if codigoproyecto is None:
                        nombre_cliente = datacliente['nombre'].iloc[0].replace(' ','_')
                        fecha_creacion = datetime.now().strftime('%Y-%m-%d')
                        codigoproyecto = generar_codigo(f'{nombre_cliente}{fecha_creacion}')
                    dataproyecto   = pd.DataFrame([{'codigo_proyecto':codigoproyecto,'created_at':fecha_creacion}])
                    dataproyecto.to_sql('cj_proyecto', engine, if_exists='append', index=False, chunksize=1)
                    
                        # Contrato
                    datacontrato = pd.DataFrame([{'codigo_proyecto':codigoproyecto,'pagorealizado':'No','created_at':datetime.now().strftime('%Y-%m-%d')}])
                    datacontrato.to_sql('cj_contrato', engine, if_exists='append', index=False, chunksize=1)

                        # PBC
                    datapbc = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    datapbc.to_sql('cj_pbc', engine, if_exists='append', index=False, chunksize=1)

                        # Clientes por proyecto 
                    dataproyectocliente = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    dataproyectocliente.to_sql('cj_proyecto_cliente', engine, if_exists='append', index=False, chunksize=1)
                                        
                        # Tipo de inversionista
                    datacoinversion = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    datacoinversion.to_sql('cj_tipoinversionista', engine, if_exists='append', index=False, chunksize=1)
                                   
                        # NIE
                    datanie = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    datanie.to_sql('cj_nie', engine, if_exists='append', index=False, chunksize=1)

                        # SL
                    datasl = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    datasl.to_sql('cj_sl', engine, if_exists='append', index=False, chunksize=1)
 
                        # Cuenta Bancaria
                    datacuentabancaria = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    datacuentabancaria.to_sql('cj_cuenta_bancaria', engine, if_exists='append', index=False, chunksize=1)
  
                        # Financiacion
                    datafinanciacion = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    datafinanciacion.to_sql('cj_financiacion', engine, if_exists='append', index=False, chunksize=1)
  
                        # Configuracion
                    dataconfig = pd.DataFrame([{'cj_clientes_codigo':codigo_inversionista,'codigo_proyecto':codigoproyecto,'json':json.dumps(dataconfiguracion()),'created_at':datetime.now().strftime('%Y-%m-%d')}])
                    dataconfig.to_sql('cj_configuracion', engine, if_exists='append', index=False, chunksize=1)

                        # Historico
                    resultado = []
                    formato   = [{'tabla':'cj_clientes','data':json.dumps(datacliente.to_json(orient='records'))},
                                 {'tabla':'cj_proyecto','data':json.dumps(dataproyecto.to_json(orient='records'))},
                                 {'tabla':'cj_contrato','data':json.dumps(datacontrato.to_json(orient='records'))},
                                 {'tabla':'cj_pbc','data':json.dumps(datapbc.to_json(orient='records'))},
                                 {'tabla':'cj_proyecto_cliente','data':json.dumps(dataproyectocliente.to_json(orient='records'))},
                                 {'tabla':'cj_tipoinversionista','data':json.dumps(datacoinversion.to_json(orient='records'))},
                                 {'tabla':'cj_nie','data':json.dumps(datanie.to_json(orient='records'))},
                                 {'tabla':'cj_sl','data':json.dumps(datasl.to_json(orient='records'))},
                                 {'tabla':'cj_cuenta_bancaria','data':json.dumps(datacuentabancaria.to_json(orient='records'))},
                                 {'tabla':'cj_financiacion','data':json.dumps(datafinanciacion.to_json(orient='records'))},]
                    for items in formato:
                        
                        resultado.append({'cj_clientes_codigo':codigo_inversionista,
                                                    'codigo_proyecto':codigoproyecto,
                                                    'tabla':items['tabla'],
                                                    'updated_at':datetime.now().strftime('%Y-%m-%d'),
                                                    'userchange':userchange,
                                                    'json':items['data']})
                        
                    dataexport = pd.DataFrame(resultado)
                    engine     = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
                    dataexport.to_sql('cj_historic_update',engine,if_exists='append', index=False)
                    engine.dispose()
                    
                    
                    st.success('Cliente guardado exitosamente')
                    engine.dispose()
                    st.cache_data.clear()
                    st.session_state.tipo_clientes = True
                    st.session_state.tipo_crear    = False
                    st.rerun()
                    
def formulario():
    
    col1,col2,col3 = st.columns([2,1,1])
    with col1:
        nombre = st.text_input('Nombre del cliente',value='')
        nombre = nombre.upper()
        nombre = re.sub('\s+',' ',nombre)
    with col2:
        sexo = st.selectbox('Sexo',options=['Hombre','Mujer'])
    with col3:
        nacionalidad =  st.selectbox('Nacionalidad',options=['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador','Estados Unidos','España', 'Guatemala', 'Haití', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'República Dominicana', 'Uruguay', 'Venezuela'])
        
    col1,col2,col3 = st.columns([2,1,1])
    with col1:
        pais_residencia =  st.selectbox('País de residencia',options=['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador','Estados Unidos','España', 'Guatemala', 'Haití', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'República Dominicana', 'Uruguay', 'Venezuela'])
    with col2:
        options = ciudades(pais_residencia)
        ciudad = st.selectbox('Ciudad de residencia',options=options)
    with col3:
        direccion = st.text_input('Dirección de residencia',value='')
                
    col1,col2 = st.columns(2)
    with col1:
        tiposID = tipo_identidad()
        try:    opciones = tiposID[nacionalidad]
        except: opciones = []
        tipoid = st.selectbox('Tipo de identificación', options=opciones)
    with col2:
        numeroid = st.text_input('Número de identificación',value='')
        
    nombrecod      = re.sub('\s+','',re.sub(r'[^a-z]','',nombre.lower()))
    texto          = f'{nombrecod}{tiposID}{numeroid}'
    codigo_inversionista = generar_codigo(re.sub('\s+', '', re.sub(r'[^a-zA-Z0-9]', '', texto.lower())))
    
    col1, col2 = st.columns(2)
    with col1:
        pasaporte = st.text_input('Pasaporte',value='')
        
    with col2:
        nie = st.text_input('NIE',value='')
        
    col1,col2,col3 = st.columns([1,1,2])
    with col1:
        codigotel = st.selectbox('Código teléfono',options=['Argentina +54', 'Bolivia +591', 'Brasil +55', 'Chile +56', 'Colombia +57', 'Costa Rica +506', 'Cuba +53', 'Ecuador +593', 'El Salvador +503','Estados Unidos +1','España +34', 'Guatemala +502', 'Haití +509', 'Honduras +504', 'México +52', 'Nicaragua +505', 'Panamá +507', 'Paraguay +595', 'Perú +51', 'República Dominicana +1-809, +1-829, +1-849', 'Uruguay +598', 'Venezuela +58'])
        codigotel = '+'+codigotel.split('+')[-1].strip()

    with col2:
        telefono = st.text_input('Número de telefono',value='')
    with col3:
        email = st.text_input('Email',value='')
                
    inputvar = {
    'codigo':codigo_inversionista,
    'nombre': nombre,
    'sexo': sexo,
    'nacionalidad': nacionalidad,
    'pais_residencia':pais_residencia,
    'ciudad':ciudad,
    'direccion':direccion,
    'tipoid': tipoid,
    'numeroid': numeroid,
    'pasaporte': pasaporte,
    'nie': nie,
    'codigotel': codigotel,
    'telefono': telefono,
    'email': email
    }
    
    data = pd.DataFrame([inputvar])
    data.replace('', None, inplace=True)
    return codigo_inversionista,data

def generar_codigo(x):
    hash_sha256 = hashlib.sha256(x.encode()).hexdigest()
    codigo      = hash_sha256[:6]
    return codigo
