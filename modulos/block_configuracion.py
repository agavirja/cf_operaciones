import streamlit as st
import re
import json
import pandas as pd
from datetime import datetime

from scripts.ciudades import ciudades
from scripts.tipo_identidad import tipo_identidad
from modulos.update_tables import updateinfoinversionista

def main(codigo,codigo_proyecto,data,userchange):
    
    if not data.empty:
        data = data[(data['cj_clientes_codigo']==codigo) & (data['codigo_proyecto']==codigo_proyecto)]
    if not data.empty and 'json' in data:
        data = pd.DataFrame(json.loads(data['json'].iloc[0]))
        
    if not data.empty:
        dataexport = []
        for secc in data['seccion'].unique():
            st.write('---')
            st.write(f'Seccion: {secc}')
            formato = data[data['seccion']==secc].to_dict(orient='records')
            col     = st.columns(4)
            pos     = 0
            for items in formato:
                tabla    = items['tabla']
                variable = items['variable']
                seccion  = items['seccion']
                nombre   = items['nombre'] 
                isopen   = items['open']
                with col[pos]:
                    if isopen or isopen==1:
                        isopen = st.toggle(nombre.replace('_',' ').title(),key=f'{seccion}: {nombre}', value=True)
                    else:
                        isopen = st.toggle(nombre.replace('_',' ').title(),key=f'{seccion}: {nombre}', value=False)
                dataexport.append({'tabla': tabla, 'variable': variable, 'seccion': seccion, 'nombre':nombre, 'open': isopen})
                pos += 1
                if pos>3:
                    pos = 0
                    col = st.columns(4)
                    
    #inputvar        = {'json':pd.io.json.dumps(dataexport),'updated_at':datetime.now().strftime('%Y-%m-%d')}
    inputvar        = {'json':json.dumps(dataexport),'updated_at':datetime.now().strftime('%Y-%m-%d')}
    codigo_name     = 'cj_clientes_codigo'
    updateinfoinversionista(inputvar,codigo_name,codigo,codigo_proyecto,'cj_configuracion',data,userchange,'button_info_configuracion')
    
    
"""
    formato = [{'tabla': 'cj_clientes', 'variable': 'urlID', 'seccion': 'inversionista', 'nombre': 'urlID', 'open': True}, 
               {'tabla': 'cj_clientes', 'variable': 'urlpasaporte', 'seccion': 'inversionista', 'nombre': 'urlpasaporte', 'open': True}, 
               {'tabla': 'cj_clientes', 'variable': 'urlnie', 'seccion': 'inversionista', 'nombre': 'urlnie', 'open': True},
               {'tabla': 'cj_contrato', 'variable': 'contrato', 'seccion': 'contrato', 'nombre': 'contrato', 'open': True}, 
               {'tabla': 'cj_cuenta_bancaria', 'variable': 'cuenta_bancaria', 'seccion': 'cuenta_bancaria', 'nombre': 'cuenta_bancaria', 'open': False}, 
               {'tabla': 'cj_cuenta_bancaria', 'variable': 'escritura_publica_const', 'seccion': 'cuenta_bancaria', 'nombre': 'escritura_publica_const', 'open': False}, 
               {'tabla': 'cj_cuenta_bancaria', 'variable': 'atr', 'seccion': 'cuenta_bancaria', 'nombre': 'atr', 'open': False}, 
               {'tabla': 'cj_cuenta_bancaria', 'variable': 'alta_hacienda_036', 'seccion': 'cuenta_bancaria', 'nombre': 'alta_hacienda_036', 'open': False}, 
               {'tabla': 'cj_cuenta_bancaria', 'variable': 'trimestr_iva_303', 'seccion': 'cuenta_bancaria', 'nombre': 'trimestr_iva_303', 'open': False}, 
               {'tabla': 'cj_cuenta_bancaria', 'variable': 'impuesto_sociedades_200', 'seccion': 'cuenta_bancaria', 'nombre': 'impuesto_sociedades_200', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'cert_vida_laboral', 'seccion': 'financiacion', 'nombre': 'cert_vida_laboral', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'carta_contable', 'seccion': 'financiacion', 'nombre': 'carta_contable', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'declaracion_renta', 'seccion': 'financiacion', 'nombre': 'declaracion_renta', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'otra_fuente_ingresos', 'seccion': 'financiacion', 'nombre': 'otra_fuente_ingresos', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'reporte_credito', 'seccion': 'financiacion', 'nombre': 'reporte_credito', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'extractos_bancarios', 'seccion': 'financiacion', 'nombre': 'extractos_bancarios', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'extractos_hipoteca', 'seccion': 'financiacion', 'nombre': 'extractos_hipoteca', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'contrato_alquiler', 'seccion': 'financiacion', 'nombre': 'contrato_alquiler', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'nif', 'seccion': 'financiacion', 'nombre': 'nif', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'escritura_constitucion', 'seccion': 'financiacion', 'nombre': 'escritura_constitucion', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'escr_titularidad_real', 'seccion': 'financiacion', 'nombre': 'escr_titularidad_real', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'impuesto_sociedades', 'seccion': 'financiacion', 'nombre': 'impuesto_sociedades', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'balances', 'seccion': 'financiacion', 'nombre': 'balances', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'PyG', 'seccion': 'financiacion', 'nombre': 'PyG', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'modelo_290', 'seccion': 'financiacion', 'nombre': 'modelo_290', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'pago_trimestrales_iva', 'seccion': 'financiacion', 'nombre': 'pago_trimestrales_iva', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'pool_bancario', 'seccion': 'financiacion', 'nombre': 'pool_bancario', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'detalle_inmovilizado', 'seccion': 'financiacion', 'nombre': 'detalle_inmovilizado', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'modelo_347', 'seccion': 'financiacion', 'nombre': 'modelo_347', 'open': False}, 
               {'tabla': 'cj_financiacion', 'variable': 'modelo_190', 'seccion': 'financiacion', 'nombre': 'modelo_190', 'open': False}, 
               {'tabla': 'cj_nie', 'variable': 'poder_nie', 'seccion': 'nie', 'nombre': 'poder_nie', 'open': False}, 
               {'tabla': 'cj_nie', 'variable': 'apostilla_poder', 'seccion': 'nie', 'nombre': 'apostilla_poder', 'open': False}, 
               {'tabla': 'cj_nie', 'variable': 'pasaporte_autenticado', 'seccion': 'nie', 'nombre': 'pasaporte_autenticado', 'open': False}, 
               {'tabla': 'cj_nie', 'variable': 'apostilla_pasaporte', 'seccion': 'nie', 'nombre': 'apostilla_pasaporte', 'open': False}, 
               {'tabla': 'cj_nie', 'variable': 'causas_economicas', 'seccion': 'nie', 'nombre': 'causas_economicas', 'open': False}, 
               {'tabla': 'cj_nie', 'variable': 'ex_15', 'seccion': 'nie', 'nombre': 'ex_15', 'open': False}, 
               {'tabla': 'cj_nie', 'variable': 'tasa_790', 'seccion': 'nie', 'nombre': 'tasa_790', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'contrato_laboral', 'seccion': 'pbc', 'nombre': 'contrato_laboral', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'nominas', 'seccion': 'pbc', 'nombre': 'nominas', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'justificacion_economica', 'seccion': 'pbc', 'nombre': 'justificacion_economica', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'carta_contador', 'seccion': 'pbc', 'nombre': 'carta_contador', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'pago_impuestos', 'seccion': 'pbc', 'nombre': 'pago_impuestos', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'declaracion_participacion', 'seccion': 'pbc', 'nombre': 'declaracion_participacion', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'informacion_socios', 'seccion': 'pbc', 'nombre': 'informacion_socios', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'extractos_bancarios', 'seccion': 'pbc', 'nombre': 'extractos_bancarios', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'justificante_domicilio', 'seccion': 'pbc', 'nombre': 'justificante_domicilio', 'open': False}, 
               {'tabla': 'cj_pbc', 'variable': 'comentarios', 'seccion': 'pbc', 'nombre': 'comentarios', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'poder_adminsitrador', 'seccion': 'sl', 'nombre': 'poder_adminsitrador', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'apostilla_poder', 'seccion': 'sl', 'nombre': 'apostilla_poder', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'cinco_nombres', 'seccion': 'sl', 'nombre': 'cinco_nombres', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'cert_denominacion_social', 'seccion': 'sl', 'nombre': 'cert_denominacion_social', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'cuenta_bancaria', 'seccion': 'sl', 'nombre': 'cuenta_bancaria', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'trans_k_social', 'seccion': 'sl', 'nombre': 'trans_k_social', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'recibo', 'seccion': 'sl', 'nombre': 'recibo', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'estatutos', 'seccion': 'sl', 'nombre': 'estatutos', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'constitucion_notaria', 'seccion': 'sl', 'nombre': 'constitucion_notaria', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'registro', 'seccion': 'sl', 'nombre': 'registro', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'documento_nif', 'seccion': 'sl', 'nombre': 'documento_nif', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'alta_aeat', 'seccion': 'sl', 'nombre': 'alta_aeat', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'alta_hacienda', 'seccion': 'sl', 'nombre': 'alta_hacienda', 'open': False}, 
               {'tabla': 'cj_sl', 'variable': 'cert_firma_digital', 'seccion': 'sl', 'nombre': 'cert_firma_digital', 'open': False}, 
               {'tabla': 'cj_tipoinversionista', 'variable': 'documento_empresa_1', 'seccion': 'tipo_inversionista', 'nombre': 'documento_empresa_1', 'open': False}, 
               {'tabla': 'cj_tipoinversionista', 'variable': 'documento_empresa_2', 'seccion': 'tipo_inversionista', 'nombre': 'documento_empresa_2', 'open': False}]
    
"""
