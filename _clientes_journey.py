import streamlit as st
import re
import json
import pandas as pd
import streamlit.components.v1 as components
import pymysql
import mysql.connector as sql
import webbrowser
from sqlalchemy import create_engine
from datetime import datetime
from bs4 import BeautifulSoup

from scripts.dataclientes import datacliente
from scripts.ciudades import ciudades
from scripts.doc2nube import doc2nube
from scripts.tipo_identidad import tipo_identidad
from scripts.tiposIdentidadEmpresarial import tiposIdentidadEmpresarial
from scripts.doc2nube import doc2nube

from modulos.block_info_inversionista import main as info_inversionista
from modulos.block_documentos_personales import main as info_documentos_personales
from modulos.block_info_capital import main as info_capital
from modulos.block_info_contrato import main as info_contrato
from modulos.block_info_pbc import main as info_pbc
from modulos.block_info_tipo_inversionista import main as info_tipo_inversionista
from modulos.block_crear_coinversionista import main as crear_coinversionista
from modulos.block_crear_nuevo_proyecto import main as crear_nuevo_proyecto
from modulos.block_info_nie import main as info_nie
from modulos.block_info_sl import main as info_sl
from modulos.block_info_cuenta_bancaria import main as info_cuenta_bancaria
from modulos.block_info_financiacion import main as info_financiacion
from modulos.block_configuracion import main as configuracion

#user     = st.secrets["user_cf_journey"]
#password = st.secrets["password_cf_journey"]
#host     = st.secrets["host_cf_journey"]
#schema   = st.secrets["schema_cf_journey"]

user       = 'external_cfdata'
password   = '5g32W1i&o'
host       = '87.106.125.178'
schema     = 'pdfcf'

def main(codigo,codigo_proyecto=None):
    usercode = '0'
    
    datainversionista,dataproyectos,datacoinversionistas,datatipoinversionista,datacontrato,datapbc,dataproyectos,datanie,datasl,datacuentabancaria,datafinanciacion,dataconfiguracion = datacliente(codigo,codigo_proyecto)
    
    formato = {
               'crear_proyecto':False,
               'crear_co_inversionista':False,
               }
    
    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
        
    col1,col2 = st.columns([4,1])
    with col2:
        style_button_dir = """
        <style>
        .custom-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #68c8ed;
            color: #ffffff; 
            font-weight: bold;
            text-decoration: none;
            border-radius: 20px;
            width: 100%;
            border: none;
            cursor: pointer;
            text-align: center;
            letter-spacing: 1px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .custom-button:visited {
            color: #ffffff;
        }
        </style>
        """
        nombre = 'Clientes'
        html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{style_button_dir}</head><body><a href="http://localhost:8501/Clientes" class="custom-button" target="_self">{nombre}</a></body></html>"""
        html = BeautifulSoup(html, 'html.parser')
        st.markdown(html, unsafe_allow_html=True)
            
    #-------------------------------------------------------------------------#
    # Informacion inversionista
    col1,col2,col3 = st.columns([1,20,2])
    with col1: 
        html = """
        <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
        <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/usuario.png" alt="link" width="30" height="30">                    
        </td>
        """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
    with col2:
        with st.expander('Información del cliente'):
            info_inversionista(datainversionista,usercode)
    
    
    #-------------------------------------------------------------------------#
    # Documentos inversionista
    
    dataprocesos = pd.DataFrame()
    if not dataconfiguracion.empty:
        dataprocesos = dataconfiguracion[dataconfiguracion['cj_clientes_codigo']==codigo]
    if not dataprocesos.empty and 'json' in dataprocesos:
        dataprocesos = pd.DataFrame(json.loads(dataprocesos['json'].iloc[0]))
        
    col1,col2,col3 = st.columns([1,20,2])
    with col1: 
        html = """
        <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
        <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/documento.png" alt="link" width="30" height="30">                    
        </td>
        """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
    with col2:
        with st.expander('Documentos del inversionista'):
            info_documentos_personales(codigo,datainversionista,dataprocesos,usercode)
    with col3:
        result = getproceso(dataprocesos,datainversionista,'Inversonista',codigo,'codigo',None,'codigo_proyecto')
        if result<100:
            progressbar(result)
        else:
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
            </td>
            """   
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
                        
        
    if len(dataproyectos)>1:
        style = """
        <style>
          .titulo {
            color: #333; /* Color del texto */
            font-size: 24px; /* Tamaño de la fuente */
            font-family: Arial, sans-serif; /* Fuente */
            text-align: center; /* Alineación del texto */
            margin-top: 50px; /* Margen superior */
          }
        </style>
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          {style}
        </head>
        <body>
          <h1 class="titulo">Proyectos de {datainversionista['nombre'].iloc[0].split(' ')[0].title()}</h1>
        </body>
        </html>
        """
        
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
        
        html_paso = ""
        for _,items in dataproyectos.iterrows():
            if isinstance(items['nombre_proyecto'], str) and items['nombre_proyecto']!='':
                nombre_proyecto = items['nombre_proyecto']
            else: nombre_proyecto = 'Sin nombre'
            html_paso += f"""
            <div class="grid-item">
              <a href="https://operaciones.streamlit.app/Clientes?codigo={codigo}&type=profile&codigo_proyecto={items['codigo_proyecto']}">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/project-management.png" width="160" height="120">
              </a>
              <p>{nombre_proyecto}</p>
            </div>
            """
        style = """
        <style>
          .grid-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            justify-content: center;
            justify-items: center;
          }
        
          .grid-item {
            text-align: center;
            margin-right: 20px;
          }
        </style>    
        """
        html = f"""
        {style}
        <div class="grid-container">
        {html_paso}
        </div>    
        """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
    else:
        codigo_proyecto = dataproyectos['codigo_proyecto'].iloc[0]
        
        dataprocesos = pd.DataFrame()
        if not dataconfiguracion.empty:
            dataprocesos = dataconfiguracion[(dataconfiguracion['cj_clientes_codigo']==codigo) & (dataconfiguracion['codigo_proyecto']==codigo_proyecto)]
        if not dataprocesos.empty and 'json' in dataprocesos:
            dataprocesos = pd.DataFrame(json.loads(dataprocesos['json'].iloc[0]))

        #---------------------------------------------------------------------#
        # Configuracion
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/configuraciones.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('Configuracion'):
                configuracion(codigo,codigo_proyecto,dataconfiguracion,usercode)
        
        #---------------------------------------------------------------------#
        # Capital
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/capital.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('Proyecto, Capital e Inversión'):
                info_capital(codigo_proyecto,dataproyectos,usercode)
            
        
        #---------------------------------------------------------------------#
        # Tipo de inversionista
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/comprador.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('Tipo de inversionista'):
                info_tipo_inversionista(codigo,codigo_proyecto,datatipoinversionista,dataprocesos,usercode)
        with col3:
            result = getproceso(dataprocesos,datatipoinversionista,'Tipo de inversionista',codigo,'cj_clientes_codigo',codigo_proyecto,'codigo_proyecto')
            if result<100:
                progressbar(result)
            else:
                html = """
                <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
                </td>
                """   
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)
            
        #---------------------------------------------------------------------#
        # Contrato
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/contrato.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('Contrato'):
                info_contrato(codigo_proyecto,datacontrato,datainversionista,dataprocesos,usercode)
        with col3:
            result = getproceso(dataprocesos,datacontrato,'Contrato',codigo,'cj_clientes_codigo',codigo_proyecto,'codigo_proyecto')
            if result<100:
                progressbar(result)
            else:
                html = """
                <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
                </td>
                """   
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)
        
        #---------------------------------------------------------------------#
        # PBC        
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/contrato.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('PBC'):
                info_pbc(codigo,codigo_proyecto,datapbc,dataprocesos,usercode)
        with col3:
            result = getproceso(dataprocesos,datapbc,'PBC',codigo,'cj_clientes_codigo',codigo_proyecto,'codigo_proyecto')
            if result<100:
                progressbar(result)
            else:
                html = """
                <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
                </td>
                """   
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)
        
        #---------------------------------------------------------------------#
        # NIE
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/comprador.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('NIE'):
                info_nie(codigo,codigo_proyecto,datanie,datainversionista,dataprocesos,usercode)
        with col3:
            result = getproceso(dataprocesos,datanie,'Nie',codigo,'cj_clientes_codigo',codigo_proyecto,'codigo_proyecto')
            if result<100:
                progressbar(result)
            else:
                html = """
                <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
                </td>
                """   
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)
 
        
        #---------------------------------------------------------------------#
        # SL
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/comprador.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('SL'):
                info_sl(codigo,codigo_proyecto,datasl,dataprocesos,usercode)
        with col3:
            result = getproceso(dataprocesos,datasl,'SL',codigo,'cj_clientes_codigo',codigo_proyecto,'codigo_proyecto')
            if result<100:
                progressbar(result)
            else:
                html = """
                <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
                </td>
                """   
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)
            
        #---------------------------------------------------------------------#
        # Cuenta Bancaria
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/comprador.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('Cuenta Bancaria'):
                info_cuenta_bancaria(codigo,codigo_proyecto,datacuentabancaria,dataprocesos,usercode)
        with col3:
            result = getproceso(dataprocesos,datacuentabancaria,'Cuenta bancaria',codigo,'cj_clientes_codigo',codigo_proyecto,'codigo_proyecto')
            if result<100:
                progressbar(result)
            else:
                html = """
                <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
                </td>
                """   
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)
            
        #---------------------------------------------------------------------#
        # Financiacion
        col1,col2,col3 = st.columns([1,20,2])
        with col1: 
            html = """
            <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
            <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/comprador.png" alt="link" width="30" height="30">                    
            </td>
            """
            texto = BeautifulSoup(html, 'html.parser')
            st.markdown(texto, unsafe_allow_html=True)
        with col2:
            with st.expander('Financiación'):
                info_financiacion(codigo,codigo_proyecto,datafinanciacion,datasl,dataprocesos,usercode)
        with col3:
            result = getproceso(dataprocesos,datafinanciacion,'Financiacion',codigo,'cj_clientes_codigo',codigo_proyecto,'codigo_proyecto')
            if result<100:
                progressbar(result)
            else:
                html = """
                <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/si.png" alt="link" width="30" height="30">                   
                </td>
                """   
                texto = BeautifulSoup(html, 'html.parser')
                st.markdown(texto, unsafe_allow_html=True)


    if len(datacoinversionistas)>0 and codigo_proyecto is not None:
        
        style = """
        <style>
          .titulo {
            color: #333; /* Color del texto */
            font-size: 24px; /* Tamaño de la fuente */
            font-family: Arial, sans-serif; /* Fuente */
            text-align: center; /* Alineación del texto */
            margin-top: 50px; /* Margen superior */
          }
        </style>
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          {style}
        </head>
        <body>
          <h1 class="titulo">co-inversionistas</h1>
        </body>
        </html>
        """
        
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
        
        html_paso = ""
        for _,items in datacoinversionistas.iterrows():
            codigo_coinversionista = items['codigo']
            html_paso += f"""
              <div class="image-container">
                <a href="https://operaciones.streamlit.app/Clientes?codigo={codigo_coinversionista}&type=profile">
                  <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/comprador.png" alt="">
                  <p>{items['nombre']}</p>
                </a>
              </div>
            """
        style = """
        <style>
          .container {
            text-align: center; /* Centra los elementos hijos horizontalmente */
          }
          .image-container {
            display: inline-block; 
            margin-right: 20px; 
          }
          .image-container img {
            width: 100px;
            height: auto;
            display: block;
            margin: 0 auto;
          }
          .image-container p {
            text-align: left;
            margin-top: 0px;
          }
          .image-container a {
            text-decoration: none; /* Elimina el subrayado del enlace */
            color: black; /* Cambia el color del texto del enlace a negro */
          }
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Imagen con enlace</title>
        {style}
        </style>
        </head>
        <body>
        <div class="container">
        {html_paso}
        </div>
        </body>
        </html>
        """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)
        
    #-------------------------------------------------------------------------#
    # Crear co inversionista
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Añadir co-inversionista'):
            st.session_state.crear_co_inversionista = True
        
    if st.session_state.crear_co_inversionista:
        crear_coinversionista(codigo_proyecto,usercode)
        
    #-------------------------------------------------------------------------#
    # Crear proyecto
    with col2:
        if st.button('Crear nuevo proyecto'):
            st.session_state.crear_proyecto = True
        
    if st.session_state.crear_proyecto:
        crear_nuevo_proyecto(codigo,datainversionista,usercode)

    components.html(
        """
    <script>
    const elements = window.parent.document.querySelectorAll('.stButton button')
    elements[0].style.backgroundColor = '#B98C65';
    elements[0].style.fontWeight = 'bold';
    elements[0].style.color = 'white';
    elements[0].style.width = '100%';
    
    elements[1].style.backgroundColor = '#B4B9C0';
    elements[1].style.fontWeight = 'bold';
    elements[1].style.color = 'white';
    elements[1].style.width = '100%';
    
    elements[2].style.backgroundColor = '#B4B9C0';
    elements[2].style.fontWeight = 'bold';
    elements[2].style.color = 'white';
    elements[2].style.width = '100%';
    
    elements[3].style.backgroundColor = '#B4B9C0';
    elements[3].style.fontWeight = 'bold';
    elements[3].style.color = 'white';
    elements[3].style.width = '100%';
    
    elements[4].style.backgroundColor = '#B4B9C0';
    elements[4].style.fontWeight = 'bold';
    elements[4].style.color = 'white';
    elements[4].style.width = '100%';
    
    elements[5].style.backgroundColor = '#B4B9C0';
    elements[5].style.fontWeight = 'bold';
    elements[5].style.color = 'white';
    elements[5].style.width = '100%';
    
    elements[6].style.backgroundColor = '#B4B9C0';
    elements[6].style.fontWeight = 'bold';
    elements[6].style.color = 'white';
    elements[6].style.width = '100%';
    
    elements[7].style.backgroundColor = '#B4B9C0';
    elements[7].style.fontWeight = 'bold';
    elements[7].style.color = 'white';
    elements[7].style.width = '100%';
    
    elements[8].style.backgroundColor = '#B4B9C0';
    elements[8].style.fontWeight = 'bold';
    elements[8].style.color = 'white';
    elements[8].style.width = '100%';
      
    elements[9].style.backgroundColor = '#B4B9C0';
    elements[9].style.fontWeight = 'bold';
    elements[9].style.color = 'white';
    elements[9].style.width = '100%';
    
    elements[10].style.backgroundColor = '#B4B9C0';
    elements[10].style.fontWeight = 'bold';
    elements[10].style.color = 'white';
    elements[10].style.width = '100%';
    
    elements[11].style.backgroundColor = '#B4B9C0';
    elements[11].style.fontWeight = 'bold';
    elements[11].style.color = 'white';
    elements[11].style.width = '100%';
    
    elements[12].style.backgroundColor = '#B4B9C0';
    elements[12].style.fontWeight = 'bold';
    elements[12].style.color = 'white';
    elements[12].style.width = '100%';
    
    elements[13].style.backgroundColor = '#B4B9C0';
    elements[13].style.fontWeight = 'bold';
    elements[13].style.color = 'white';
    elements[13].style.width = '100%';
    
    elements[14].style.backgroundColor = '#B4B9C0';
    elements[14].style.fontWeight = 'bold';
    elements[14].style.color = 'white';
    elements[14].style.width = '100%';
    
    elements[15].style.backgroundColor = '#B4B9C0';
    elements[15].style.fontWeight = 'bold';
    elements[15].style.color = 'white';
    elements[15].style.width = '100%';
    
    elements[16].style.backgroundColor = '#B4B9C0';
    elements[16].style.fontWeight = 'bold';
    elements[16].style.color = 'white';
    elements[16].style.width = '100%';
    
    elements[17].style.backgroundColor = '#B4B9C0';
    elements[17].style.fontWeight = 'bold';
    elements[17].style.color = 'white';
    elements[17].style.width = '100%';
    
    elements[18].style.backgroundColor = '#B4B9C0';
    elements[18].style.fontWeight = 'bold';
    elements[18].style.color = 'white';
    elements[18].style.width = '100%';
    
    elements[19].style.backgroundColor = '#B4B9C0';
    elements[19].style.fontWeight = 'bold';
    elements[19].style.color = 'white';
    elements[19].style.width = '100%';
    
    elements[20].style.backgroundColor = '#B4B9C0';
    elements[20].style.fontWeight = 'bold';
    elements[20].style.color = 'white';
    elements[20].style.width = '100%';
    
    elements[21].style.backgroundColor = '#B4B9C0';
    elements[21].style.fontWeight = 'bold';
    elements[21].style.color = 'white';
    elements[21].style.width = '100%';
    
    elements[22].style.backgroundColor = '#B4B9C0';
    elements[22].style.fontWeight = 'bold';
    elements[22].style.color = 'white';
    elements[23].style.width = '100%';
    
    elements[24].style.backgroundColor = '#B4B9C0';
    elements[24].style.fontWeight = 'bold';
    elements[24].style.color = 'white';
    elements[24].style.width = '100%';
    
    elements[25].style.backgroundColor = '#B4B9C0';
    elements[25].style.fontWeight = 'bold';
    elements[25].style.color = 'white';
    elements[25].style.width = '100%';
    </script>
    """
    )


def getproceso(dataprocesos,dataref,seccion,codigo,codigo_name,codigo_proyecto,codigo_proyecto_name):
    result = 1
    dataseguimiento = dataprocesos[(dataprocesos['seccion']==seccion) & ((dataprocesos['open']==True) | (dataprocesos['open']==1))]
    if not dataseguimiento.empty:
        variables       = [x for x in dataseguimiento['variable'].to_list() if x in dataref]
        K               = len(variables)
        if codigo_name in dataref and  codigo is not None and codigo_proyecto_name in dataref and codigo_proyecto is not None:
            dataseguimiento = dataref[(dataref[codigo_name]==codigo) & (dataref[codigo_proyecto_name]==codigo_proyecto)]
        elif codigo_proyecto_name in dataref and codigo_proyecto is not None:
            dataseguimiento = dataref[dataref[codigo_proyecto_name]==codigo_proyecto]
        elif codigo_name in dataref and  codigo is not None:
            dataseguimiento = dataref[dataref[codigo_name]==codigo]
        dataseguimiento = dataseguimiento[variables]
        check           = sum(dataseguimiento.applymap(lambda x: isinstance(x, str)).any())
        result          = check/K
    return result*100

def progressbar(x):
    style = """
    <style>
        .progress-bar {
            width: 100px;
            height: 30px;
            border: 1px solid #ccc;
            border-radius: 5px;
            overflow: hidden;
            position: relative;
            margin-bottom: 20px;
        }
    
        .progress {
            height: 100%;
            background-color: green; /* Color por defecto */
            transition: width 0.5s ease-in-out;
        }
    
        .progress.red {
            background-color: #ff6666; /* Rojo claro */
        }
    
        .progress.yellow {
            background-color: #ffff66; /* Amarillo claro */
        }
    
        .progress.green {
            background-color: #66ff66; /* Verde claro */
        }
    
        .progress.full {
            background-color: #00cc00; /* Verde fuerte */
        }
    
        .marker {
            position: absolute;
            top: 0;
            width: 2px;
            height: 100%;
            background-color: black;
            pointer-events: none;
        }
    </style>
    """
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Barra de Progreso</title>
    {style}
    </head>
    <body>
    
    <div class="progress-bar">
        <div class="progress" id="progress" style="width: {x}%"></div>
        <div class="marker" id="marker"></div>
    </div>
    </body>
    </html>
    """
    texto = BeautifulSoup(html, 'html.parser')
    st.markdown(texto, unsafe_allow_html=True)
    
    
