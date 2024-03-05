import streamlit as st
from bs4 import BeautifulSoup

def main(codigo):
    
    st.write(codigo)
    
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
        
        