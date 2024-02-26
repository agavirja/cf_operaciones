import streamlit as st
import re
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.doc2nube import doc2nube
from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista,updatedocuments


#-----------------------------------------------------------------------------#
# Info Financiacion
#-----------------------------------------------------------------------------#
def main(codigo_cliente,codigo_proyecto,data,datasl,dataprocesos,userchange):

    col1,col2 = st.columns(2)
    with col1:
        options = ['Persona Natural','Persona Juridica']
        value   = data['tipo_persona_financiacion'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        tipo_persona_financiacion = st.selectbox('Tipo de persona para la financiación',options=options,index=index)
    
    with col2:
        value = datasl['nif'].iloc[0]
        if value is None:
            value = ''
        st.text_input('NIF',value=value,key='seccion_sl_nif_f',disabled=True)


    inputvar    = {'tipo_persona_financiacion':tipo_persona_financiacion}
    codigo_name = 'cj_clientes_codigo'
    updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_financiacion',data,userchange,'button_info_financiacion')
    
    dataprocesos = dataprocesos[dataprocesos['tabla']=='cj_financiacion']

    if 'Persona Natural' in tipo_persona_financiacion:
        formato = [{'variable':'cert_vida_laboral','button_name':'Certificado de vida laboral','file_name':'f_cert_vida_laboral'},
                   {'variable':'carta_contable','button_name':'Carta contable','file_name':'f_carta_contable'},
                   {'variable':'declaracion_renta','button_name':'Declaración de renta','file_name':'f_declaracion_renta'},
                   {'variable':'otra_fuente_ingresos','button_name':'Otra fuente de ingresos','file_name':'f_otra_fuente_ingresos'},
                   {'variable':'reporte_credito','button_name':'Reporte de crédito','file_name':'f_reporte_credito'},
                   {'variable':'extractos_bancarios','button_name':'Extracto bancario de los últimos 6 meses','file_name':'f_extractos_bancarios'},
                   {'variable':'extractos_hipoteca','button_name':'2 últimos extractos de hipoteca','file_name':'f_extractos_hipoteca'},
                   {'variable':'contrato_alquiler','button_name':'Contrato de alquiler','file_name':'f_contrato_alquiler'},
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
                            updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_financiacion',data,userchange)
                            st.cache_data.clear()
                            st.rerun()
                            
    if 'Persona Juridica' in tipo_persona_financiacion:
        
        formato = [{'variable':'escritura_constitucion','button_name':'Escritura de constitución ','file_name':'f_escritura_constitucion'},
                   {'variable':'escr_titularidad_real','button_name':'Escritura de Titularidad Real','file_name':'f_escr_titularidad_real'},
                   {'variable':'impuesto_sociedades','button_name':'Impuesto sobre sociedades','file_name':'f_impuesto_sociedades'},
                   {'variable':'balances','button_name':'Balances','file_name':'f_balances'},
                   {'variable':'PyG','button_name':'PyG','file_name':'f_PyG'},
                   {'variable':'modelo_290','button_name':'Modelo 390','file_name':'f_modelo_290'},
                   {'variable':'pago_trimestrales_iva','button_name':'Pagos trimestrales de IVA','file_name':'f_pago_trimestrales_iva'},
                   {'variable':'pool_bancario','button_name':'Detalle del pool bancario por entidades','file_name':'f_pool_bancario'},
                   {'variable':'detalle_inmovilizado','button_name':'Detalle inmovilizado','file_name':'f_detalle_inmovilizado'},
                   {'variable':'modelo_347','button_name':'Modelo 347','file_name':'f_modelo_347'},
                   {'variable':'modelo_190','button_name':'Modelo 190','file_name':'f_modelo_190'},
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
                            updatedocuments(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_financiacion',data,userchange)
                            st.cache_data.clear()
                            st.rerun()
