import streamlit as st
import re
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.doc2nube import doc2nube
from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista,updatedocuments

from scripts.tiposIdentidadEmpresarial import tiposIdentidadEmpresarial

#-----------------------------------------------------------------------------#
# Info Tipo de Inversionistas
#-----------------------------------------------------------------------------#
def main(codigo_cliente,codigo_proyecto,data,dataprocesos,userchange):
    col1,col2 = st.columns(2)
    with col1:
        options = ['Persona natural','Persona Juridica']
        value   = data['tipoinversionista'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        tipoinversionista = st.selectbox('Tipo de inversionista',options=options,index=index)

    pais_empresa,nombre_empresa,tipodocumento_empresa,id_empresa, nombre_rl,tipoid_rl,numeroid_rl = [None]*7
    
    if 'Persona Juridica' in tipoinversionista:
        col1,col2 = st.columns(2)
        with col1:
            options=['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador', 'El Salvador', 'España', 'Estados Unidos', 'Guatemala', 'Haití', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'República Dominicana', 'Uruguay', 'Venezuela']
            value   = data['pais_empresa'].iloc[0]
            index   = 0
            if value is not None and value!='':
                index = options.index(value)
            pais_empresa = st.selectbox('País de la sociedad',options=options,index=index)
        with col2: 
            value = data['nombre_empresa'].iloc[0]
            if value is None:
                value = ''
            nombre_empresa = st.text_input('Nombre de la sociedad',value=value)
            
        with col1:
            tiposID = tiposIdentidadEmpresarial()
            options = tiposID[pais_empresa]
            value   = data['tipodocumento_empresa'].iloc[0]
            index   = 0
            if value is not None and value!='':
                try: index = options.index(value)
                except: pass
            tipodocumento_empresa = st.selectbox('Tipo de identificación de la empresa', options=options,index=index)
        with col2:
            value = data['id_empresa'].iloc[0]
            if value is None:
                value = ''
            id_empresa = st.text_input('ID se la empresa',value=value)
            
        col1,col2,col3 = st.columns([2,1,1])
        with col1:
            value = data['nombre_rl'].iloc[0]
            if value is None:
                value = ''
            nombre_rl = st.text_input('Nombre del representante legal',value=value)
            nombre_rl = nombre_rl.upper()
        with col2:
            value = data['tipoid_rl'].iloc[0]
            if value is None:
                value = ''
            tipoid_rl = st.text_input('Tipo de identificación RL', value=value)
        with col3:
            value = data['numeroid_rl'].iloc[0]
            if value is None:
                value = ''
            numeroid_rl = st.text_input('Número de identificación RL',value=value)

    inputvar   = {'tipoinversionista':tipoinversionista,'pais_empresa':pais_empresa,'nombre_empresa':nombre_empresa,'tipodocumento_empresa':tipodocumento_empresa,'id_empresa':id_empresa, 'nombre_rl':nombre_rl,'tipoid_rl':tipoid_rl,'numeroid_rl':numeroid_rl,'updated_at':datetime.now().strftime('%Y-%m-%d')}
    codigo_name = 'cj_clientes_codigo'
    updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_tipoinversionista',data,userchange,'button_info_tipo_inversionista')
    
    
    if 'Persona Juridica' in tipoinversionista:
        formato = [{'variable':'documento_empresa_1','button_name':'Documento empresa (1)','file_name':'documento_empresa_1'},
                   {'variable':'documento_empresa_2','button_name':'Documento empresa (2)','file_name':'documento_empresa_2'},
                   ]
        dataprocesos = dataprocesos[dataprocesos['tabla']=='cj_tipoinversionista']

        for items in formato:
            
            variable    = items['variable']
            button_name = items['button_name']
            file_name   = items['file_name']
            
            col1, col2, col3, col4 = st.columns([1,1,3,2])
            urllink = data[variable].iloc[0]
            value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/cancelar.png'
            if urllink is not None:
                value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png'
                
            with col1:
                w = dataprocesos[dataprocesos['variable']==variable]
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
                if urllink is not None:
                    html += f"""
                    <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                       <a href="{urllink}" target="_blank">
                       <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/pdffile.png" alt="link" width="30" height="30">
                       </a>                    
                    </td>
                    """
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)
            
            with col3:
                file_contrato = st.file_uploader(f'Subir {button_name}')
                if file_contrato is not None:
                    with col4:
                        st.write('')
                        st.write('')
                        st.write('')
                        if st.button(f'Guardar {button_name}'):
                            subfolder   = f'cliente-{codigo_cliente}/proyecto-{codigo_proyecto}'
                            value       = doc2nube(subfolder,file_contrato,file_name)
                            inputvar    = {variable:value,'updated_at':datetime.now().strftime('%Y-%m-%d')}
                            codigo_name = 'cj_clientes_codigo'
                            updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_tipoinversionista',data,userchange)
                            st.cache_data.clear()
                            st.rerun()
