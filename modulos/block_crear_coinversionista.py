import streamlit as st
import re
import json
import hashlib
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine 

from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from scripts.dataclientes import dataclientes as listaClientes, datainfocliente as dataClienteParticular
from scripts.dataconfiguracion import dataconfiguracion

user     = st.secrets["user_cf_pdfcf"]
password = st.secrets["password_cf_pdfcf"]
host     = st.secrets["host_cf_pdfcf"]
schema   = st.secrets["schema_cf_pdfcf"]

def main(codigo_proyecto,userchange):
    
    formato = {
               'crear_co_inversionista':False,
               }
    
    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
    
    data      = listaClientes()
    col1,col2 = st.columns(2)
    userclient = 'Nuevo'
    if not data.empty:
        with col1:
            listaclientes = list(data['nombre'].unique())
            listaclientes = ['Nuevo'] + listaclientes
            userclient    = st.selectbox('Cliente',key='nombrecliente',options=listaclientes)
        
    #-------------------------------------------------------------------------#
    # Cliente ya existente
    #-------------------------------------------------------------------------#
    if 'nuevo' not in userclient.lower():
        codigo_userclient = None
        if not data.empty:
            codigo_userclient = data[data['nombre']==userclient]['codigo'].iloc[0]
            
        if codigo_userclient is not None:
            datainversionista_p = dataClienteParticular(codigo_userclient)

            col1,col2,col3 = st.columns([2,1,1])
            with col1:
                st.text_input(' Nombre del cliente ',value=datainversionista_p['nombre'].iloc[0],disabled=True)
            with col2:
                st.text_input(' Sexo ',value=datainversionista_p['sexo'].iloc[0],disabled=True)
            with col3:
                st.text_input(' Nacionalidad ',value=datainversionista_p['nacionalidad'].iloc[0],disabled=True)
            col1,col2,col3 = st.columns([2,1,1])
            with col1:
                st.text_input(' País de residencia ',value=datainversionista_p['pais_residencia'].iloc[0],disabled=True)
            with col2:
                st.text_input(' Ciudad de residencia ',value=datainversionista_p['ciudad'].iloc[0],disabled=True)
            with col3:
                st.text_input(' Dirección de residencia ',value=datainversionista_p['direccion'].iloc[0],disabled=True)
            col1,col2,col3 = st.columns([1,1,2])
            with col1:
                st.text_input(' Código teléfono ',value=datainversionista_p['codigotel'].iloc[0],disabled=True)
            with col2:
                st.text_input(' Número de telefono ',value=datainversionista_p['telefono'].iloc[0],disabled=True)
            with col3:
                st.text_input(' Email ',value=datainversionista_p['email'].iloc[0],disabled=True)
            col1,col2 = st.columns(2)
            with col1:
                st.text_input(' Tipo de identificación ',value=datainversionista_p['tipoid'].iloc[0],disabled=True)
            with col2:
                st.text_input(' Número de identificación ',value=datainversionista_p['numeroid'].iloc[0],disabled=True)      
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(' Pasaporte ',value=datainversionista_p['pasaporte'].iloc[0],disabled=True)      
            with col2:
                st.text_input(' NIE ',value=datainversionista_p['nie'].iloc[0],disabled=True)      

            col1, col2 = st.columns(2)
            with col1:
                if st.button('Guardar',key='guardar_coinversionista'):
                    with st.spinner('Guardando'):
                        
                        engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}') 
                        codigo_cliente = datainversionista_p['codigo'].iloc[0]
                        
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
                              
                            # Historico
                        resultado = []
                        formato   = [{'tabla':'cj_pbc','data':json.dumps(datapbc, orient='records')},
                                     {'tabla':'cj_proyecto_cliente','data':json.dumps(dataproyectocliente, orient='records')},
                                     {'tabla':'cj_tipoinversionista','data':json.dumps(datacoinversion, orient='records')},
                                     {'tabla':'cj_nie','data':json.dumps(datanie, orient='records')},
                                     {'tabla':'cj_sl','data':json.dumps(datasl, orient='records')},
                                     {'tabla':'cj_cuenta_bancaria','data':json.dumps(datacuentabancaria, orient='records')},
                                     {'tabla':'cj_financiacion','data':json.dumps(datafinanciacion, orient='records')},]
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
                        
                        st.success('Cliente guardado exitosamente')
                        engine.dispose()
                        st.cache_data.clear()
                        st.session_state.crear_co_inversionista = False
                        st.rerun()
                    
    #-------------------------------------------------------------------------#
    # Cliente Nuevo
    #-------------------------------------------------------------------------#
    elif 'nuevo' in userclient.lower():
        col1,col2,col3 = st.columns([2,1,1])
        with col1:
            nombre = st.text_input('Nombre del cliente ',key='nombrecoinversionista',value='')
            nombre = nombre.upper()
            nombre = re.sub('\s+',' ',nombre)
        with col2:
            sexo = st.selectbox('Sexo',key='sexocoinversionista',options=['Hombre','Mujer'])
        with col3:
            options = ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador','Estados Unidos','España', 'Guatemala', 'Haití', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'República Dominicana', 'Uruguay', 'Venezuela']
            nacionalidad =  st.selectbox('Nacionalidad ',key='nacionalidadcoinversionista',options=options)
            
        col1,col2,col3 = st.columns([2,1,1])
        with col1:
            options = ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador','Estados Unidos','España', 'Guatemala', 'Haití', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'República Dominicana', 'Uruguay', 'Venezuela']
            pais_residencia =  st.selectbox('País de residencia ',key='paisresidenciacoinversionista',options=options)
        with col2:
            options = ciudades(pais_residencia)
            ciudad = st.selectbox('Ciudad de residencia ',key='ciudadresidenciacoinversionista',options=options)
        with col3:
            direccion = st.text_input('Dirección de residencia ',key='direccionresidenciacoinversionista',value='')
                        
        col1,col2,col3 = st.columns([1,1,2])
        with col1:
            options = ['Argentina +54', 'Bolivia +591', 'Brasil +55', 'Chile +56', 'Colombia +57', 'Costa Rica +506', 'Cuba +53', 'Ecuador +593', 'El Salvador +503','Estados Unidos +1','España +34', 'Guatemala +502', 'Haití +509', 'Honduras +504', 'México +52', 'Nicaragua +505', 'Panamá +507', 'Paraguay +595', 'Perú +51', 'República Dominicana +1-809, +1-829, +1-849', 'Uruguay +598', 'Venezuela +58']
            codigotel = st.selectbox('Código teléfono ',key='codigotelcoinversionista',options=options)
            codigotel = '+'+codigotel.split('+')[-1].strip()
    
        with col2:
            telefono = st.text_input('Número de telefono ',key='numerotelcoinversionista',value='')
        with col3:
            email = st.text_input('Email',key='emailcoinversionista',value='')
            
        col1,col2 = st.columns(2)
        with col1:
            tiposID = tipo_identidad()
            options = tiposID[nacionalidad]
            tipoid  = st.selectbox('Tipo de identificación ',key='tipoidcoinversionista', options=options)
        with col2:
            numeroid = st.text_input('Número de identificación ',key='numeroidcoinversionista',value='')
                
        col1, col2 = st.columns(2)
        with col1:
            pasaporte = st.text_input('Pasaporte ',key='pasaportecoinversionista',value='')
        with col2:
            nie = st.text_input('NIE ',key='niecoinversionista',value='')
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Guardar',key='guardar_coinversionista'):
                with st.spinner('Guardando'):
                    
                        # Cliente
                    nombrecod      = re.sub('\s+','',re.sub(r'[^a-z]','',nombre.lower()))
                    texto          = f'{nombrecod}{tiposID}{numeroid}'
                    codigo_cliente = generar_codigo(re.sub('\s+', '', re.sub(r'[^a-zA-Z0-9]', '', texto.lower())))
                    
                    inputvar       = {'codigo':codigo_cliente,'nombre':nombre,'sexo':sexo,'nacionalidad':nacionalidad,'pais_residencia':pais_residencia,'ciudad':ciudad,'direccion':direccion,'tipoid':tipoid,'numeroid':numeroid,'pasaporte':pasaporte,'nie':nie,'codigotel':codigotel,'telefono':telefono,'email':email,'created_at':datetime.now().strftime('%Y-%m-%d')}
                    datacliente    = pd.DataFrame([inputvar])
                   
                    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}') 
                    datacliente.to_sql('cj_clientes', engine, if_exists='append', index=False, chunksize=1)
    
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
                    formato   = [{'tabla':'cj_clientes','data':json.dumps(datacliente, orient='records')},
                                 {'tabla':'cj_pbc','data':json.dumps(datapbc, orient='records')},
                                 {'tabla':'cj_proyecto_cliente','data':json.dumps(dataproyectocliente, orient='records')},
                                 {'tabla':'cj_tipoinversionista','data':json.dumps(datacoinversion, orient='records')},
                                 {'tabla':'cj_nie','data':json.dumps(datanie, orient='records')},
                                 {'tabla':'cj_sl','data':json.dumps(datasl, orient='records')},
                                 {'tabla':'cj_cuenta_bancaria','data':json.dumps(datacuentabancaria, orient='records')},
                                 {'tabla':'cj_financiacion','data':json.dumps(datafinanciacion, orient='records')},]
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
                    
                    st.success('Cliente guardado exitosamente')
                    engine.dispose()
                    st.cache_data.clear()
                    st.session_state.crear_co_inversionista = False
                    st.rerun()
                    

        
def generar_codigo(x):
    hash_sha256 = hashlib.sha256(x.encode()).hexdigest()
    codigo      = hash_sha256[:6]
    return codigo
