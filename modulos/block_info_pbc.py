import streamlit as st
import re
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.doc2nube import doc2nube
from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista,updatedocuments


#-----------------------------------------------------------------------------#
# Info PBC
#-----------------------------------------------------------------------------#
def main(codigo_cliente,codigo_proyecto,data,dataprocesos,userchange):
    
    value = data['comentarios'].iloc[0]
    if not isinstance(value, str):
        value = ''

    txt = st.text_area('Comentario',value=value)
    txt = re.sub('\s+',' ',txt).lower()
    inputvar    = {'comentarios':txt}
    codigo_name = 'cj_clientes_codigo'
    updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_pbc',data,userchange,'button_info_pbc')
    
    dataprocesos = dataprocesos[dataprocesos['tabla']=='cj_pbc']
    
    if not data.empty:
        formato = [{'variable':'contrato_laboral','button_name':'contrato laboral','file_name':'principal_contrato_laboral'},
                   {'variable':'nominas','button_name':'últimas 6 nominas','file_name':'principal_ultimas_6_nominas'},
                   {'variable':'justificacion_economica','button_name':'justificación económica','file_name':'principal_justifiacion_economica'},
                   {'variable':'carta_contador','button_name':'carta contador','file_name':'principal_carta_contador'},
                   {'variable':'pago_impuestos','button_name':'pago de impuestos','file_name':'principal_pago_impuestos'},
                   {'variable':'declaracion_participacion','button_name':'declaración de particiación','file_name':'principal_declaracion_participacion'},
                   {'variable':'informacion_socios','button_name':'inforamción de socios','file_name':'principal_informacion_socios'},
                   {'variable':'extractos_bancarios','button_name':'extractos bancarios','file_name':'princi_extractos_bancarios'},
                   {'variable':'justificante_domicilio','button_name':'justificante domicilio','file_name':'principal_justificante_domicilio'},
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
            
            with col3 :
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
                            updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_pbc',data,userchange)
                            st.cache_data.clear()
                            st.rerun()
