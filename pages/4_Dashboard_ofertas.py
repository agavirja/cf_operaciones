import streamlit as st

from _dashboard_ofertas import main as maindashboard
from modulos._dashboard_ofertas_oportunidades import main as mainalternativas


st.set_page_config(layout="wide",initial_sidebar_state="auto",page_icon="https://operaciones.fra1.digitaloceanspaces.com/_icons/FAVICON-CF.png")

formato = {
           'codigo_proyecto':None,
           }

for key,value in formato.items():
    if key not in st.session_state: 
        st.session_state[key] = value
 
# obtener los argumentos de la url
args = st.experimental_get_query_params()
if 'codigo_proyecto' in args: 
    st.session_state.codigo_proyecto = args['codigo_proyecto'][0]

col1,col2,col3 = st.columns([6,1,1])
with col2:
    st.image('https://capitalfriend.es/studio/img/LOGO-R-CF.png',width=300)

if st.session_state.codigo_proyecto is None:
    maindashboard()
else:   
    mainalternativas(st.session_state.codigo_proyecto)