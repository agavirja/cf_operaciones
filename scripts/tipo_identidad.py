import streamlit as st

@st.cache_data
def tipo_identidad(x=None):
    result =  {
    "Argentina": ["DNI (Documento Nacional de Identidad)", "CUIL (Código Único de Identificación Laboral)"],
    "Bolivia": ["CI (Cédula de Identidad)"],
    "Brasil": ["RG (Registro Geral)", "CPF (Cadastro de Pessoas Físicas)"],
    "Chile": ["RUT (Rol Único Tributario)"],
    "Colombia": ["CC (Cédula de Ciudadanía)", "TI (Tarjeta de Identidad)", "CE (Cédula de Extranjería)", "NIT (Número de Identificación Tributaria)"],
    "Costa Rica": ["Cédula de Identidad"],
    "Cuba": ["Carné de Identidad"],
    "Ecuador": ["Cédula de Identidad"],
    "El Salvador": ["DUI (Documento Único de Identidad)"],
    "Estados Unidos": ["SSN (Social Security Number)", "Driver's License", "Passport"],
    "Guatemala": ["DPI (Documento Personal de Identificación)"],
    "Haití": ["Carte d'identité nationale"],
    "Honduras": ["RTN (Registro Tributario Nacional)"],
    "México": ["INE (Instituto Nacional Electoral)", "CURP (Clave Única de Registro de Población)"],
    "Nicaragua": ["Cédula de Identidad"],
    "Panamá": ["Cédula de Identidad Personal"],
    "Paraguay": ["Cédula de Identidad Civil"],
    "Perú": ["DNI (Documento Nacional de Identidad)"],
    "República Dominicana": ["Cédula de Identidad y Electoral"],
    "Uruguay": ["CI (Cédula de Identidad)"],
    "Venezuela": ["Cédula de Identidad"],
    "España": ["DNI (Documento Nacional de Identidad)", "NIE (Número de Identificación de Extranjero)"]
    }
    if x is not None:
        if x in result:
            result = result[x]
        else: result = ''
    return result
