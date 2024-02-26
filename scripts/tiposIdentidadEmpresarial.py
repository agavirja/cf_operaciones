import streamlit as st

@st.cache_data
def tiposIdentidadEmpresarial(x=None):
    result =   {
    "Argentina": ["CUIL (Código Único de Identificación Laboral)"],
    "Bolivia": ["NIT (Número de Identificación Tributaria)"],
    "Brasil": ["CPF (Cadastro de Pessoas Físicas)"],
    "Chile": ["RUT (Rol Único Tributario)"],
    "Colombia": ["NIT (Número de Identificación Tributaria)"],
    "Costa Rica": ["Cédula Jurídica"],
    "Cuba": ["RFC (Registro Federal de Contribuyentes)"],
    "Ecuador": ["RUC (Registro Único de Contribuyentes)"],
    "El Salvador": ["NIT (Número de Identificación Tributaria)"],
    "España": ["NIF (Número de Identificación Fiscal)"],
    "Estados Unidos": ["EIN (Employer Identification Number)"],
    "Guatemala": ["NIT (Número de Identificación Tributaria)"],
    "Haití": ["Identifiant Fiscal Unique (IFU)"],
    "Honduras": ["RTN (Registro Tributario Nacional)"],
    "México": ["RFC (Registro Federal de Contribuyentes)"],
    "Nicaragua": ["RUC (Registro Único de Contribuyentes)"],
    "Panamá": ["RUC (Registro Único de Contribuyentes)"],
    "Paraguay": ["RUC (Registro Único de Contribuyentes)"],
    "Perú": ["RUC (Registro Único de Contribuyentes)"],
    "República Dominicana": ["RNC (Registro Nacional del Contribuyente)"],
    "Uruguay": ["RUT (Registro Único Tributario)"],
    "Venezuela": ["RIF (Registro de Información Fiscal)"]
    }
    if x is not None:
        if x in result:
            result = result[x]
        else: result = ''
    return result
