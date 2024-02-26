import streamlit as st
import pandas as pd
from sqlalchemy import create_engine 
import mysql.connector

@st.cache_data
def dataconfiguracion():
    
    user     = st.secrets["user_cf_pdfcf"]
    password = st.secrets["password_cf_pdfcf"]
    host     = st.secrets["host_cf_pdfcf"]
    schema   = st.secrets["schema_cf_pdfcf"]

    conexion = mysql.connector.connect(host=host,user=user,password=password,database=schema)
    cursor   = conexion.cursor()
    cursor.execute(f"SHOW TABLES LIKE 'cj_%'")
    tablas = [tabla[0] for tabla in cursor.fetchall()] # ['cj_clientes','cj_contrato','cj_cuenta_bancaria','cj_financiacion','cj_historic_update','cj_nie','cj_pbc','cj_proyecto','cj_proyecto_cliente','cj_sl','cj_tipoinversionista']
    cursor.close()
    conexion.close()
        
    lista  = []
    result = []
    for i in tablas:
        v = tablas_variables(host, user, password, schema, i)
        for j in v:
            if 'longtext' in j[1].lower():
                result.append({'tabla':i,'variable':j[0],'seccion':f'_{i}_','nombre':j[0],'open':False})

    df            = pd.DataFrame(result)
    
    idd           = df['seccion'].isin(['_cj_historic_update_','_cj_configuracion_'])
    df            = df[~idd]
    df['seccion'] = df['seccion'].replace(['_cj_clientes_', '_cj_contrato_', '_cj_cuenta_bancaria_','_cj_financiacion_', '_cj_nie_','_cj_pbc_', '_cj_sl_', '_cj_tipoinversionista_'],['Inversonista', 'Contrato', 'Cuenta bancaria','Financiacion', 'Nie','PBC', 'SL', 'Tipo de inversionista'])
    
    a             = ['urlID', 'urlpasaporte', 'urlnie', 'contrato', 'cuenta_bancaria', 'escritura_publica_const', 'atr', 'alta_hacienda_036', 'trimestr_iva_303', 'impuesto_sociedades_200', 'cert_vida_laboral', 'carta_contable', 'declaracion_renta', 'otra_fuente_ingresos', 'reporte_credito', 'extractos_bancarios', 'extractos_hipoteca', 'contrato_alquiler', 'nif', 'escritura_constitucion', 'escr_titularidad_real', 'impuesto_sociedades', 'balances', 'PyG', 'modelo_290', 'pago_trimestrales_iva', 'pool_bancario', 'detalle_inmovilizado', 'modelo_347', 'modelo_190', 'poder_nie', 'apostilla_poder', 'pasaporte_autenticado', 'apostilla_pasaporte', 'causas_economicas', 'ex_15', 'tasa_790', 'contrato_laboral', 'nominas', 'justificacion_economica', 'carta_contador', 'pago_impuestos', 'declaracion_participacion', 'informacion_socios', 'extractos_bancarios', 'justificante_domicilio', 'poder_adminsitrador', 'apostilla_poder', 'cinco_nombres', 'cert_denominacion_social', 'cuenta_bancaria', 'trans_k_social', 'recibo', 'estatutos', 'constitucion_notaria', 'registro', 'documento_nif', 'alta_aeat', 'alta_hacienda', 'cert_firma_digital', 'documento_empresa_1', 'documento_empresa_2']
    b             = ['ID', 'Pasaporte', 'NIE', 'Contrato', 'Cuenta Bancaria', 'Escritura Pública', 'ATR', 'Alta Hacienda 036', 'Trimestre IVA 303', 'Impuesto a sociedades 200', 'Certificado vida laboral', 'Carta Contable', 'Declaración de renta', 'Otra fuente de ingresos', 'Reporte de crédito', 'Extractos Bancarios', 'Extractos de hipoteca', 'Contrato Alquiler', 'NIF', 'Escritura Constitución', 'Escritura titularidad real', 'Impuesto sociedades', 'Balances', 'PyG', 'Modelo 290', 'Pago trimestrales IVA', 'Pool bancario', 'Detalle inmovilizado', 'Modelo 347', 'Modelo 190', 'Poder NIE', 'Apostilla poder', 'Pasaporte autenticado', 'Apostilla pasaporte', 'Causas Económicas', 'EX 15', 'Tasa 790', 'Contrato laboral', 'Nominas', 'Justificación económica', 'Carta contador', 'Pago impuestos', 'Declaración participación', 'Información de socios', 'Extractos Bancarios', 'Justificante Domicilio', 'Poder administrativo', 'Apostilla poder', 'Cinco nombres', 'Certificado denominación social', 'Cuenta Bancaria', 'Trans K social', 'Recibo', 'Estatutos', 'Constitución Notaria', 'Registro', 'Documento NIF', 'Alta AEAT', 'Alta hacienda ', 'Certificado firma digital', 'Documento Empresa (1)', 'Documento Empresa (2)']
    df['nombre']  = df['nombre'].replace(a,b)
    
    idd = df['nombre'].isin([ 'comentarios',])
    df  = df[~idd]
    
    idd = df['nombre'].isin(['ID','Pasaporte','NIE','Contrato','Cuenta Bancaria'])
    if sum(idd)>0:
        df.loc[idd,'open'] = True
        
    return df.to_dict(orient='records')

def tablas_variables(host, usuario, contraseña, base_datos, tabla):
    conexion = mysql.connector.connect(host=host,user=usuario,password=contraseña,database=base_datos)
    cursor = conexion.cursor()
    cursor.execute(f"DESCRIBE {tabla}")
    nombre_y_tipo_variables = []
    for columna in cursor.fetchall():
        nombre_variable = columna[0]
        tipo_variable = columna[1]
        nombre_y_tipo_variables.append((nombre_variable, tipo_variable))
    cursor.close()
    conexion.close()
    return nombre_y_tipo_variables
