import streamlit as st
from datetime import datetime

from modulos.update_tables import updateinfoinversionista

#-----------------------------------------------------------------------------#
# Info Capital
#-----------------------------------------------------------------------------#
def main(codigo,data,userchange):
    
    col1,col2,col3 = st.columns([2,2,1])
    with col1:
        options = ['España']
        value   = data['pais'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        pais =  st.selectbox('País de inversión',key='paisinversion',options=options,index=index)

    with col2:
        options = ['Madrid']
        value   = data['ciudad'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        ciudad =  st.selectbox('Ciudad de la inversión',key='ciudadinversion',options=options,index=index)
    with col3:
        options = ["EUR", "USD", "COP", "MXN", "ARS", "CLP"]
        value   = data['moneda'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        moneda = st.selectbox('moneda',options=options,index=index)
        
    col1,col2 = st.columns([4,1])
    with col1:
        value = data['nombre_proyecto'].iloc[0]
        if value is None:
            value = ''
        nombre_proyecto =  st.text_input('Nombre del proyecto',key='nombreproyectoinversion',value=value)

    col1,col2,col3 = st.columns([2,2,1])
    with col1:
        value = data['capital'].iloc[0]
        if value is None:
            value = 0
        else: 
            value = int(value)
        capital =  st.number_input('Capital disponible',min_value=0,value=value)
    with col2:
        value = data['valorproyecto'].iloc[0]
        if value is None:
            value = 0
        else: 
            value = int(value)
        valorproyecto = st.number_input('Valor del proyecto',min_value=0,value=value)
    with col3:
        options = ['','Si','No']
        value   = data['financiacion'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        financiacion = st.selectbox('Financiación',options=options,index=index)

        
    inputvar = {'pais':pais,'ciudad':ciudad,'nombre_proyecto':nombre_proyecto,'capital':capital,'valorproyecto':valorproyecto,'financiacion':financiacion,'moneda':moneda,'updated_at':datetime.now().strftime('%Y-%m-%d')}
    codigo_cliente  = None
    codigo_name     = None
    updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo,'cj_proyecto',data,userchange,'button_info_capital')
