import streamlit as st

from _clientes_crear import main as main_clientes
from _clientes_journey import main as  main_userprofile

st.set_page_config(layout="wide",initial_sidebar_state="auto",page_icon="https://operaciones.fra1.digitaloceanspaces.com/_icons/FAVICON-CF.png")

formato = {
           'codigo':None,
           'codigo_proyecto':None,
           'type':None,
           }

for key,value in formato.items():
    if key not in st.session_state: 
        st.session_state[key] = value
 
# obtener los argumentos de la url
args = st.experimental_get_query_params()
if 'codigo' in args: 
    st.session_state.codigo = args['codigo'][0]
if 'codigo_proyecto' in args: 
    st.session_state.codigo_proyecto = args['codigo_proyecto'][0]
if 'type' in args:
    st.session_state.type = args['type'][0]

col1,col2,col3 = st.columns([6,1,1])
with col2:
    st.image('https://capitalfriend.es/studio/img/LOGO-R-CF.png',width=300)

if st.session_state.codigo is None and st.session_state.type is None:
    main_clientes()
else:
    if 'profile' in st.session_state.type:
        main_userprofile(st.session_state.codigo,codigo_proyecto=st.session_state.codigo_proyecto)

