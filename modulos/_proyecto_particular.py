import streamlit as st
from bs4 import BeautifulSoup

def main(codigo):
    
    col1,col2 = st.columns([4,1])
    with col2:
        style_button_dir = """
        <style>
        .custom-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #B98C65;
            color: #ffffff; 
            font-weight: bold;
            text-decoration: none;
            border-radius: 10px;
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
        html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{style_button_dir}</head><body><a href="https://operaciones.streamlit.app/Proyectos" class="custom-button" target="_self">Proyectos</a></body></html>"""
        html = BeautifulSoup(html, 'html.parser')
        st.markdown(html, unsafe_allow_html=True)
            
    #---------------------------------------------------------------------#
    # Calculadora
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
      <div class="image-container">
        <a href="https://operaciones.streamlit.app/Calculadora_financiera?codigo_proyecto={codigo}&type=profile">
          <img src="https://operaciones.fra1.digitaloceanspaces.com/_icons/calculadora.png" alt="">
          <p>Calculadora Financiera</p>
        </a>
      </div>
    </div>
    </body>
    </html>
    """
    texto = BeautifulSoup(html, 'html.parser')
    st.markdown(texto, unsafe_allow_html=True)
        
        