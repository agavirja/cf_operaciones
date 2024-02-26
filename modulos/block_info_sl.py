import streamlit as st
import re
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.doc2nube import doc2nube
from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista,updatedocuments


#-----------------------------------------------------------------------------#
# Info SL
#-----------------------------------------------------------------------------#
def main(codigo_cliente,codigo_proyecto,data,dataprocesos,userchange):

    col1, col2 = st.columns(2)
    with col1:
        value = data['vencimiento'].iloc[0]
        if value is None:
            value = ''
        vencimiento = st.date_input('Vencimiento',value="today",key='seccion_sl_vencimiento',format="YYYY-MM-DD")
    
    with col2:
        value = data['nif'].iloc[0]
        if value is None:
            value = ''
        nif = st.text_input('NIF',value=value,key='seccion_sl_nif')

    inputvar    = {'vencimiento':vencimiento,'nif':nif}
    codigo_name = 'cj_clientes_codigo'
    updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_sl',data,userchange,'button_info_sl')
    

    formato = [{'variable':'poder_adminsitrador','button_name':'Poder Adminsitrador','file_name':'sl_poder_adminsitrador'},
               {'variable':'apostilla_poder','button_name':'Apostilla Poder ','file_name':'sl_apostilla_poder'},
               {'variable':'cinco_nombres','button_name':'5 Nombres','file_name':'sl_cinco_nombres'},
               {'variable':'cert_denominacion_social','button_name':'Certificado Denominación Social','file_name':'sl_cert_denominacion_social'},
               {'variable':'cuenta_bancaria','button_name':'Cuenta Bancaria','file_name':'sl_cuenta_bancaria'},
               {'variable':'trans_k_social','button_name':'Transferencia K social','file_name':'sl_trans_k_social'},
               {'variable':'recibo','button_name':'Recibo','file_name':'sl_recibo'},
               {'variable':'estatutos','button_name':'Estatutos','file_name':'sl_estatutos'},
               {'variable':'constitucion_notaria','button_name':'Constitución Notaria','file_name':'sl_constitucion_notaria'},
               {'variable':'registro','button_name':'Registro','file_name':'sl_registro'},
               {'variable':'documento_nif','button_name':'Documento NIF','file_name':'sl_documento_nif'},
               {'variable':'alta_aeat','button_name':'Alta AEAT','file_name':'sl_alta_aeat'},
               {'variable':'alta_hacienda','button_name':'Alta Hacienda','file_name':'sl_alta_hacienda'},
               {'variable':'cert_firma_digital','button_name':'Certificado Firma Digital','file_name':'sl_cert_firma_digital'},
               ]
    
    dataprocesos = dataprocesos[dataprocesos['tabla']=='cj_sl']

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
                        updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_sl',data,userchange)
                        st.cache_data.clear()
                        st.rerun()