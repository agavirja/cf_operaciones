import streamlit as st
import re
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.doc2nube import doc2nube
from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad

from modulos.update_tables import updatedocuments


#-----------------------------------------------------------------------------#
# Info Documentos Inversionistas
#-----------------------------------------------------------------------------#
def main(codigo,data,dataprocesos,userchange):    

    dataprocesos = dataprocesos[dataprocesos['tabla']=='cj_clientes']

    # ID
    col1, col2, col3, col4 = st.columns([1,1,3,2])

    urlid = data['urlID'].iloc[0]
    value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/cancelar.png'
    if urlid is not None:
        value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png'
        
    with col1:
        w = dataprocesos[dataprocesos['variable']=='urlID']
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
        if urlid is not None:
            html += f"""
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
               <a href="{urlid}" target="_blank">
               <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/pdffile.png" alt="link" width="30" height="30">
               </a>                    
            </td>
            """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
    
    with col3:
        ID_file = st.file_uploader("Subir ID personal")
        if ID_file is not None:
            with col4:
                st.write('')
                st.write('')
                st.write('')
                if st.button('Guardar ID'):
                    subfolder = f'cliente-{codigo}'
                    value    = doc2nube(subfolder,ID_file,'ID_inversionista_principal')
                    inputvar = {'urlID':value,'updated_at':datetime.now().strftime('%Y-%m-%d')}
                    codigo_name     = 'codigo'
                    codigo_cliente  = codigo
                    codigo_proyecto = None
                    updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_clientes',data,userchange)

                    
    # Pasaporte
    col1, col2, col3, col4 = st.columns([1,1,3,2])
    urlpasaporte = data['urlpasaporte'].iloc[0]
    value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/cancelar.png'
    if urlpasaporte is not None:
        value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png'
        
    with col1:
        w = dataprocesos[dataprocesos['variable']=='urlpasaporte']
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
        if urlpasaporte is not None:
            html += f"""
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
               <a href="{urlpasaporte}" target="_blank">
               <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/pdffile.png" alt="link" width="30" height="30">
               </a>                    
            </td>
            """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
    
    with col3:
        ID_file = st.file_uploader("Subir Pasaporte")
        if ID_file is not None:
            with col4:
                st.write('')
                st.write('')
                st.write('')
                if st.button('Guardar Pasaporte'):
                    subfolder = f'cliente-{codigo}'
                    value    = doc2nube(subfolder,ID_file,'Pasaporte')
                    inputvar = {'urlpasaporte':value,'updated_at':datetime.now().strftime('%Y-%m-%d')}
                    codigo_name     = 'codigo'
                    codigo_cliente  = codigo
                    codigo_proyecto = None
                    updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_clientes',data,userchange)

    # NIE
    col1, col2, col3, col4 = st.columns([1,1,3,2])
    urlnie = data['urlnie'].iloc[0]
    value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/cancelar.png'
    if urlnie is not None:
        value = 'https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png'
        
    with col1:
        w = dataprocesos[dataprocesos['variable']=='urlnie']
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
        if urlnie is not None:
            html += f"""
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
               <a href="{urlnie}" target="_blank">
               <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/pdffile.png" alt="link" width="30" height="30">
               </a>                    
            </td>
            """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
    
    with col3:
        ID_file = st.file_uploader("Subir NIE")
        if ID_file is not None:
            with col4:
                st.write('')
                st.write('')
                st.write('')
                if st.button('Guardar NIE'):
                    subfolder = f'cliente-{codigo}'
                    value    = doc2nube(subfolder,ID_file,'NIE')
                    inputvar = {'urlnie':value,'updated_at':datetime.now().strftime('%Y-%m-%d')}
                    codigo_name     = 'codigo'
                    codigo_cliente  = codigo
                    codigo_proyecto = None
                    updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_clientes',data,userchange)
