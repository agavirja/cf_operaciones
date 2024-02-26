import streamlit as st
import re
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.doc2nube import doc2nube
from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista,updatedocuments


#-----------------------------------------------------------------------------#
# Info Cuenta Bancaria
#-----------------------------------------------------------------------------#
def main(codigo_cliente,codigo_proyecto,data,dataprocesos,userchange):

    dataprocesos = dataprocesos[dataprocesos['tabla']=='cj_cuenta_bancaria']

    formato = [{'variable':'cuenta_bancaria','button_name':'Cuenta Bancaria ','file_name':'cb_cuenta_bancaria'},
               {'variable':'escritura_publica_const','button_name':'Escritura Pública','file_name':'cb_escritura_publica_const'},
               {'variable':'atr','button_name':'ATR','file_name':'cb_atr'},
               {'variable':'alta_hacienda_036','button_name':'Alta en Hacienda 036','file_name':'cb_alta_hacienda_036'},
               {'variable':'trimestr_iva_303','button_name':'Trimestre IVA 303','file_name':'cb_trimestr_iva_303'},
               {'variable':'impuesto_sociedades_200','button_name':'Impuesto de sociedades 200','file_name':'cb_impuesto_sociedades_200'},
               ]
    
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
                        updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_cuenta_bancaria',data,userchange)
                        st.cache_data.clear()
                        st.rerun()