import streamlit as st

from _calculadora_financiera import main

st.set_page_config(layout="wide",initial_sidebar_state="auto",page_icon="https://operaciones.fra1.digitaloceanspaces.com/_icons/FAVICON-CF.png")

col1,col2,col3 = st.columns([6,1,1])
with col2:
    st.image('https://capitalfriend.es/studio/img/LOGO-R-CF.png',width=300)

main()

