import streamlit as st
import re
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.doc2nube import doc2nube
from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista,updatedocuments

#-----------------------------------------------------------------------------#
# Info contrato
#-----------------------------------------------------------------------------#
def main(codigo,data,datainversionista,dataprocesos,userchange):

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        value = ''
        if not datainversionista.empty and 'tipoid' in datainversionista:
            value = datainversionista['tipoid'].iloc[0]
        st.text_input('Tipo de identificación ', value=value,disabled=True)
    with col2:
        value = ''
        if not datainversionista.empty and 'numeroid' in datainversionista:
            value = datainversionista['numeroid'].iloc[0]
        st.text_input('Número de identificación ',value=value,disabled=True)
    with col3:
        value = ''
        if not datainversionista.empty and 'pasaporte' in datainversionista:
            value = datainversionista['pasaporte'].iloc[0]
        st.text_input('Pasaporte ',value=value,disabled=True)
    with col4:
        value = ''
        if not datainversionista.empty and 'nie' in datainversionista:
            value = datainversionista['nie'].iloc[0]
        st.text_input('NIE ',value=value,disabled=True)
        
    col1,col2 = st.columns(2)
    with col1:
        options = ['','Pasaporte extranjero','Pasaporte español','Documento de identidad extranjero','NIE','DNI','NIF']
        index   = 0
        if not data.empty:
            value   = data['tipo'].iloc[0]
            if value is not None and value!='':
                index = options.index(value)
        tipo = st.selectbox('Datos con los que figura en el contrato ',options=options,index=index)
    with col2:
        options = ['','Persona física','Sociedad limitada']
        index   = 0
        if not data.empty:
            value   = data['vehiculo'].iloc[0]
            if value is not None and value!='':
                index = options.index(value)
        vehiculo = st.selectbox('Vehículo de inversioón',options=options,index=index)
        
    col1,col2,col3 = st.columns([1,2,1])
    with col1:
        options = ['No','Si']
        index   = 0
        if not data.empty:
            value   = data['firmado'].iloc[0]
            if value is not None and value!='':
                index = options.index(value)
        firmado =  st.selectbox('Contrato firmado',options=options,index=index)
        
    with col2:
        value = 0
        if not data.empty:
            try:   value = int(data['valorcontrato'].iloc[0])
            except: pass
        valorcontrato =  st.number_input('Valor del contrato',value=value)
        if valorcontrato==0:
            valorcontrato = None
    
    with col3:
        options = ['No','Si']
        index   = 0
        if not data.empty:
            value   = data['pagorealizado'].iloc[0]
            if value is not None and value!='':
                index = options.index(value)
        pagorealizado =  st.selectbox('Pago realizado',options=options,index=index)
        

    inputvar        = {'tipo': tipo,'vehiculo': vehiculo,'firmado': firmado,'valorcontrato':valorcontrato,'pagorealizado':pagorealizado,'updated_at':datetime.now().strftime('%Y-%m-%d')}
    codigo_cliente  = None
    codigo_name     = None
    codigo_proyecto = codigo
    updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_contrato',data,userchange,'button_info_contrato')


    # Subir contrato
    dataprocesos = dataprocesos[dataprocesos['tabla']=='cj_contrato']

    col1, col2, col3, col4 = st.columns([1,1,3,2])
    contrato = data['contrato'].iloc[0]
    value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/cancelar.png'
    if contrato is not None:
        value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png'
        
    with col1:
        w = dataprocesos[dataprocesos['variable']=='contrato']
        if not w.empty and (w['open'].iloc[0]==True or w['open'].iloc[0]==1):
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/asterisco.png" alt="link" width="30" height="30">                   
            </td>
            """ 
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
            
    with col2:
        st.write('')
        st.write('')
        st.write('')
        html = f"""
        <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
        <img src="{value}" alt="link" width="30" height="30">                   
        </td>
        """
        if contrato is not None:
            html += f"""
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
               <a href="{contrato}" target="_blank">
               <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/pdffile.png" alt="link" width="30" height="30">
               </a>                    
            </td>
            """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
    
    with col3:
        file_contrato = st.file_uploader("Subir el contrato")
        if file_contrato is not None:
            with col4:
                st.write('')
                st.write('')
                st.write('')
                if st.button('Guardar contrato'):
                    subfolder = f'cliente-{codigo}'
                    value    = doc2nube(subfolder,file_contrato,'ID_inversionista_principal')
                    inputvar = {'contrato':value,'updated_at':datetime.now().strftime('%Y-%m-%d')}
                    codigo_cliente  = None
                    codigo_name     = None
                    codigo_proyecto = codigo
                    updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_contrato',data,userchange)
                    st.cache_data.clear()
                    st.rerun()