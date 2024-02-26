import streamlit as st
import streamlit.components.v1 as components

from modulos._clientes_crear import main as crear_cliente
from modulos._clientes_lista import main as clientes

def main():
    
    formato = {'tipo_crear':False,
               'tipo_clientes':True,
    }
    
    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
            
    col1,col2 = st.columns(2) 
    with col1:
        if st.button('Crear cliente'):
            st.session_state.tipo_crear    = True
            st.session_state.tipo_clientes = False
            
    with col2:
        if st.button('Lista de clientes'):
            st.cache_data.clear()
            st.session_state.tipo_clientes = True
            st.session_state.tipo_crear    = False
     
    if st.session_state.tipo_crear:
        crear_cliente()
        
    if st.session_state.tipo_clientes:
        clientes()
                       
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
    
    elements[2].style.backgroundColor = '#B98C65';
    elements[2].style.fontWeight = 'bold';
    elements[2].style.color = 'white';
    elements[2].style.width = '100%';
    
    elements[3].style.backgroundColor = '#B98C65';
    elements[3].style.fontWeight = 'bold';
    elements[3].style.color = 'white';
    elements[3].style.width = '100%';
    
    elements[4].style.backgroundColor = '#B98C65';
    elements[4].style.fontWeight = 'bold';
    elements[4].style.color = 'white';
    elements[4].style.width = '100%';
    
    elements[5].style.backgroundColor = '#B98C65';
    elements[5].style.fontWeight = 'bold';
    elements[5].style.color = 'white';
    elements[5].style.width = '100%';
    
    elements[6].style.backgroundColor = '#B98C65';
    elements[6].style.fontWeight = 'bold';
    elements[6].style.color = 'white';
    elements[6].style.width = '100%';
    
    elements[7].style.backgroundColor = '#B98C65';
    elements[7].style.fontWeight = 'bold';
    elements[7].style.color = 'white';
    elements[7].style.width = '100%';
    
    elements[8].style.backgroundColor = '#B98C65';
    elements[8].style.fontWeight = 'bold';
    elements[8].style.color = 'white';
    elements[8].style.width = '100%';
      
    elements[9].style.backgroundColor = '#B98C65';
    elements[9].style.fontWeight = 'bold';
    elements[9].style.color = 'white';
    elements[9].style.width = '100%';
    
    elements[10].style.backgroundColor = '#B98C65';
    elements[10].style.fontWeight = 'bold';
    elements[10].style.color = 'white';
    elements[10].style.width = '100%';
    
    elements[11].style.backgroundColor = '#B98C65';
    elements[11].style.fontWeight = 'bold';
    elements[11].style.color = 'white';
    elements[11].style.width = '100%';
    
    elements[12].style.backgroundColor = '#B98C65';
    elements[12].style.fontWeight = 'bold';
    elements[12].style.color = 'white';
    elements[12].style.width = '100%';
    </script>
    """
    )

    

