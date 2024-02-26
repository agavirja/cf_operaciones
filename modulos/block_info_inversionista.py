import streamlit as st
import re
from datetime import datetime

from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista

def main(data,userchange):
    col1,col2,col3 = st.columns([2,1,1])
    with col1:
        nombre = st.text_input('Nombre del cliente',value=data['nombre'].iloc[0])
        nombre = nombre.upper()
        nombre = re.sub('\s+',' ',nombre)
    with col2:
        options = ['Hombre','Mujer']
        value   = data['sexo'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        sexo = st.selectbox('Sexo',options=options,index=index)
    with col3:
        options = ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador','Estados Unidos','España', 'Guatemala', 'Haití', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'República Dominicana', 'Uruguay', 'Venezuela']
        value   = data['nacionalidad'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        nacionalidad = st.selectbox('Nacionalidad',options=options,index=index)
        
    col1,col2,col3 = st.columns([2,1,1])
    with col1:
        options = ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador','Estados Unidos','España', 'Guatemala', 'Haití', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'República Dominicana', 'Uruguay', 'Venezuela']
        value   = data['pais_residencia'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        pais_residencia =  st.selectbox('País de residencia ',options=options,index=index)
    with col2:
        options = ciudades(pais_residencia)
        value   = data['ciudad'].iloc[0]
        index   = 0
        if value is not None and value!='':
            try: index = options.index(value)
            except: pass
        ciudad = st.selectbox('Ciudad de residencia',options=options,index=index)
    with col3:
        value = data['direccion'].iloc[0]
        if value is None:
            value = ''
        direccion = st.text_input('Dirección de residencia',value=value)
                    
    col1,col2,col3 = st.columns([1,1,2])
    with col1:
        options = ['Argentina +54', 'Bolivia +591', 'Brasil +55', 'Chile +56', 'Colombia +57', 'Costa Rica +506', 'Cuba +53', 'Ecuador +593', 'El Salvador +503','Estados Unidos +1','España +34', 'Guatemala +502', 'Haití +509', 'Honduras +504', 'México +52', 'Nicaragua +505', 'Panamá +507', 'Paraguay +595', 'Perú +51', 'República Dominicana +1-809, +1-829, +1-849', 'Uruguay +598', 'Venezuela +58']
        value   = data['codigotel'].iloc[0]
        index   = 0
        if value is not None and value!='':
            w = [x for x in options if value in x]
            if w!=[]:
                index = options.index(w[0])
        codigotel = st.selectbox('Código teléfono',options=options,index=index)
        codigotel = '+'+codigotel.split('+')[-1].strip()

    with col2:
        value = data['telefono'].iloc[0]
        if value is None:
            value = ''
        telefono = st.text_input('Número de telefono',value=value)
    with col3:
        value = data['email'].iloc[0]
        if value is None:
            value = ''
        email = st.text_input('Email',value=value)
        
    col1,col2 = st.columns(2)
    with col1:
        tiposID = tipo_identidad()
        options = tiposID[nacionalidad]
        value   = data['tipoid'].iloc[0]
        index   = 0
        if value is not None and value!='':
            try: index = options.index(value)
            except: pass
        tipoid = st.selectbox('Tipo de identificación', options=options,index=index)
    with col2:
        value = data['numeroid'].iloc[0]
        if value is None:
            value = ''
        numeroid = st.text_input('Número de identificación',value=value)
            
    col1, col2 = st.columns(2)
    with col1:
        value = data['pasaporte'].iloc[0]
        if value is None:
            value = ''
        pasaporte = st.text_input('Pasaporte',value=value)
    with col2:
        value = data['nie'].iloc[0]
        if value is None:
            value = ''
        nie = st.text_input('NIE',value=value)
        
    inputvar        = {'nombre':nombre,'sexo':sexo,'nacionalidad':nacionalidad,'pais_residencia':pais_residencia,'ciudad':ciudad,'direccion':direccion,'tipoid':tipoid,'numeroid':numeroid,'pasaporte':pasaporte,'nie':nie,'codigotel':codigotel,'telefono':telefono,'email':email,'updated_at':datetime.now().strftime('%Y-%m-%d')}
    codigo_cliente  = data['codigo'].iloc[0]
    codigo_name     = 'codigo'
    codigo_proyecto = None
    updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_clientes',data,userchange,'button_info_cliente')
