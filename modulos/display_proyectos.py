import streamlit as st
import numpy as np
import streamlit.components.v1 as components
from bs4 import BeautifulSoup

def main(dataproyectos,titulo=''):
    if not dataproyectos.empty:
        dataexport = dataproyectos.copy()
        dataproyectos.replace({None: '', np.nan: ''}, inplace=True)
        html_tabla = ""
        for _,i in dataproyectos.iterrows():
            html_tabla += f""" 
            <tr>
              <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                 <a href="https://operaciones.streamlit.app/Proyectos?codigo_proyecto={i['codigo_proyecto']}" target="_blank">
                 <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/usuario.png" alt="link" width="20" height="20">
                 </a>                    
              </td>
              <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <h6 class="mb-0 text-sm">{i['codigo_proyecto']}</h6>
              </td>
              <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <h6 class="mb-0 text-sm">{i['nombre_proyecto']}</h6>
              </td>
              <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <h6 class="mb-0 text-sm">{i['pais']}</h6>
              </td>
              <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <h6 class="mb-0 text-sm">{i['ciudad']}</h6>
              </td>         
              <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <h6 class="mb-0 text-sm">{i['direccion']}</h6>
              </td>     
              <td class="align-middle text-center text-sm" style="border: none;padding: 8px;">
                <h6 class="mb-0 text-sm">{i['created_at']}</h6>
              </td>  
            """
        tabla_vigencia = f"""
        <div class="cliente-table">
            <table class="table align-items-center mb-0" style="background-color: #ffffff;" >
                <thead>
                    <tr style="margin-bottom: 0px;background-color: #ffffff;">
                      <th class="align-middle text-center" style="border-top:none; border-left:none;border-right:none;border-bottom: 1px solid #ccc;">Link</th>
                      <th class="align-middle text-center" style="border-top:none; border-left:none;border-right:none;border-bottom: 1px solid #ccc;">Código</th>
                      <th class="align-middle text-center" style="border-top:none; border-left:none;border-right:none;border-bottom: 1px solid #ccc;">Nombre Proyecto</th>
                      <th class="align-middle text-center" style="border-top:none; border-left:none;border-right:none;border-bottom: 1px solid #ccc;">País</th>
                      <th class="align-middle text-center" style="border-top:none; border-left:none;border-right:none;border-bottom: 1px solid #ccc;">Ciudad</th>
                      <th class="align-middle text-center" style="border-top:none; border-left:none;border-right:none;border-bottom: 1px solid #ccc;">Dirección</th>
                      <th class="align-middle text-center" style="border-top:none; border-left:none;border-right:none;border-bottom: 1px solid #ccc;">Fecha de creación</th>
                    </tr>
                </thead>
                <tbody>
                    {html_tabla}
                </tbody>
                </div>
            </table>
        </div>
        """
        style = """
        <style>
            .tabla_principal {
                max-width: 100%;
                max-height: 100%;
            }
        
            .cliente-table {
                overflow-x: auto;
                overflow-y: auto;
                max-width: 100%;
                max-height: 400px;
                scroll-behavior: smooth;
                scroll-margin-top: 0px;
            }
        
            .chart-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
                width: 100%;
                margin-top: 100px;
            }
        
            body {
                font-family: Arial, sans-serif;
            }
        
            .table th, .table td {
                padding: 12px;
                text-align: center;
                min-width: 100px;
            }
        
            .table th {
                background-color: #ffffff;
                position: sticky;
                top: 0; 
            }
        </style>
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
          <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-icons.css" rel="stylesheet">
          <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-svg.css" rel="stylesheet">
          <link id="pagestyle" href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/soft-ui-dashboard.css?v=1.0.7" rel="stylesheet">
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          {style}
        </head>
        <body>
          <div class="container-fluid py-4" style="margin-bottom: 0px;margin-top: -20px;">
            <div class="row">

              <div class="col-xl-12 col-sm-6 mb-xl-0 mb-2">
                <div class="card h-100">
                  <div class="card-body p-3">  
                    <div class="container-fluid py-4">
                      <div class="row" style="margin-bottom: 0px;margin-top: -20px;">
                        <div class="card-body p-3">
                          <div class="row">
                            <div class="numbers">
                              <h3 class="font-weight-bolder mb-0" style="text-align: center; font-size: 1.5rem; padding-bottom: 8px;">{titulo}</h3>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>                       
                    <div class="container-fluid py-4">
                      <div class="row" style="margin-bottom: -30px;margin-top: -50px;">
                        {tabla_vigencia}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
 
            </div>
          </div>
        </body>
        </html>
        """
        texto = BeautifulSoup(html, 'html.parser')
        st.markdown(texto, unsafe_allow_html=True)

        variables = ['chip', 'vigencia', 'nroIdentificacion', 'valorAutoavaluo', 'valorImpuesto', 'copropiedad', 'indPago', 'tipoPropietario', 'tipoDocumento', 'primerNombre', 'segundoNombre', 'primerApellido', 'segundoApellido', 'telefono1', 'telefono2', 'telefono3', 'telefono4', 'telefono5', 'email1', 'email2', 'email3']
        variables = [x for x in variables if x in dataexport]
        if variables:
            dataexport = dataexport[variables]
            dataexport.rename(columns={"chip":"Chip","vigencia":"Vigencia","nroIdentificacion":"Identificacion","valorAutoavaluo":"Avaluo catastral","valorImpuesto":"Predial","copropiedad":"Porcentaje copropiedad","indPago":"Indicador de pago","tipoPropietario":"Tipo propietario","tipoDocumento":"Tipo documento","primerNombre":"Primer nombre","segundoNombre":"Segundo nombre","primerApellido":"Primer apellido","segundoApellido":"Segundo apellido","telefono1":"Telefono 1","telefono2":"Telefono 2","telefono3":"Telefono 3","telefono4":"Telefono 4","telefono5":"Telefono 5","email1":"Email 1","email2":"Email 2","email3":"Email 3"},inplace=True)
            col1, col2 = st.columns([3,1])
            with col2:
                csv = convert_df(dataexport)     
                st.download_button(
                   "Descargar información",
                   csv,
                   "data_info_prediales.csv",
                   "text/csv"
                )
                
    
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
