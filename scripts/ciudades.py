import streamlit as st

@st.cache_data
def ciudades(x=None):
    
    result =  {
        "Argentina": ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "San Miguel de Tucumán"],
        "Bolivia": ["La Paz", "Santa Cruz de la Sierra", "Cochabamba", "Sucre", "Tarija"],
        "Brasil": ["São Paulo", "Río de Janeiro", "Brasilia", "Salvador", "Fortaleza"],
        "Chile": ["Santiago", "Valparaíso", "Concepción", "La Serena", "Antofagasta"],
        "Colombia": ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"],
        "Costa Rica": ["San José", "Alajuela", "Liberia", "Heredia", "Puntarenas"],
        "Cuba": ["La Habana", "Santiago de Cuba", "Camagüey", "Holguín", "Santa Clara"],
        "Ecuador": ["Quito", "Guayaquil", "Cuenca", "Santo Domingo de los Colorados", "Machala"],
        "El Salvador": ["San Salvador", "Santa Ana", "San Miguel", "Mejicanos", "Soyapango"],
        "Estados Unidos": ["Nueva York", "Los Ángeles", "Chicago", "Houston", "Phoenix"],
        "Guatemala": ["Ciudad de Guatemala", "Mixco", "Villa Nueva", "Quetzaltenango", "San Miguel Petapa"],
        "Haití": ["Puerto Príncipe", "Carrefour", "Delmas", "Pétion-Ville", "Port-de-Paix"],
        "Honduras": ["Tegucigalpa", "San Pedro Sula", "Choloma", "La Ceiba", "El Progreso"],
        "México": ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Toluca"],
        "Nicaragua": ["Managua", "León", "Masaya", "Matagalpa", "Chinandega"],
        "Panamá": ["Ciudad de Panamá", "San Miguelito", "Tocumen", "David", "Arraiján"],
        "Paraguay": ["Asunción", "Ciudad del Este", "San Lorenzo", "Luque", "Capiatá"],
        "Perú": ["Lima", "Arequipa", "Trujillo", "Chiclayo", "Huancayo"],
        "República Dominicana": ["Santo Domingo", "Santiago de los Caballeros", "Santiago de los Caballeros", "La Romana", "San Pedro de Macorís"],
        "España": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza"],
        "Uruguay": ["Montevideo", "Salto", "Paysandú", "Las Piedras", "Rivera"],
        "Venezuela": ["Caracas", "Maracaibo", "Valencia", "Barquisimeto", "Maracay"]
    }
    if x is not None:
        if x in result:
            result = result[x]
        else: result = ''
    return result
        
