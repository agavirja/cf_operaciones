import streamlit as st
import pandas as pd
import numpy_financial as npf
import json
from bs4 import BeautifulSoup

from scripts.dataproyectos import dataproyectos as listaproyectos,datacalculadora
from modulos.update_tables import updateinfoinversionista

def main(codigo_proyecto=None,userchange=None):
    IVA = 0.21
    
    data = {
        "preciocompra": [0],
        "moneda": ["EUR"],
        "tipoinversor": ["General"],
        "porcentajecomisioncompra": [0],
        "hipoteca": ["Si"],
        "gastosescriturahipoteca": [0],
        "comisionhipoteca": [0],
        "seguro": [0],
        "superficieregistro": [0],
        "superficiereal": [0],
        "valorobramt2": [0],
        "markupobra": [19],
        "feecf": [3.5],
        "tipoalquiler":["Friend Stay"],
        "valortotalrenta":[0],
        "tasaocupacion":[95],
        "habitaciones":[[{'tipohabitacion':'Doble','numerohabitaciones':3,'valorhabitacion':690},{'tipohabitacion':'Sencilla','numerohabitaciones':2,'valorhabitacion':565}]],
        "margenxhabitacion":[130],
        "iva_renta_mensual":[IVA*100],
        "suministros":[60],
        "servicios":[[{"variable": "Electricidad", "value": 70, "IVA": IVA*100},{"variable": "Gas", "value": 80, "IVA": IVA*100},{"variable": "Agua", "value": 30, "IVA": 10},{"variable": "Limpieza", "value": 50, "IVA": IVA*100},{"variable": "CRM", "value": 15, "IVA": IVA*100},{"variable": "Gestor", "value": 50, "IVA": IVA*100},{"variable": "Portero/Responsable", "value": 0, "IVA": IVA*100},{"variable": "Seguro", "value": 15, "IVA": 0},{"variable": "Internet", "value": 30, "IVA": IVA*100}]],
        "firmacontrato":[[{"variable": "Mes en Curso","cantidad":1, "value": 0, "IVA": IVA*100},{"variable": "Depósito","cantidad":1, "value": 0.0, "IVA": 0},{"variable": "Fianza","cantidad":1, "value": 0.0, "IVA": 0},{"variable": "Agencia","cantidad":1, "value": 0.0, "IVA": IVA*100}]],
        "factordescuento":[10.0],
        "incrementoalquileresano1":[6.25],
        "ipcano1":[3.25],
        "incrementoalquileresano2":[6.25],
        "ipcano2":[3.25],
        "ibi":[0],
        "basegestoriames":[150],
        "carry":[0],
        "aporte":[40],
        "plazo_credito":[20],
        "tasa_credito":[3.25],
        "seguromensual":[30],
        "IBI":[400/12],
        "comunidadvecinos":[80],
        "ahorro_disponible":[200000],
        "per_itp":[7],
        "per_inmobiliaria":[3],
        "ingresonetomes":[0],
    }

    data      = pd.DataFrame(data)
    datastock = datacalculadora(codigo_proyecto)
    if not datastock.empty:
        try:
            data = pd.DataFrame([json.loads(datastock['json'].iloc[0])])
            try: data["habitaciones"] = data["habitaciones"].apply(lambda x: json.loads(x))
            except: pass
            try: data["servicios"] = data["servicios"].apply(lambda x: json.loads(x))
            except: pass    
            try: data["firmacontrato"] = data["firmacontrato"].apply(lambda x: json.loads(x))
            except: pass
        except: pass
                      
    col1,col2 = st.columns([4,1])
    with col2:
        style_button_dir = """
        <style>
        .custom-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #B98C65;
            color: #ffffff; 
            font-weight: bold;
            text-decoration: none;
            border-radius: 10px;
            width: 100%;
            border: none;
            cursor: pointer;
            text-align: center;
            letter-spacing: 1px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .custom-button:visited {
            color: #ffffff;
        }
        </style>
        """
        html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{style_button_dir}</head><body><a href="https://operaciones.streamlit.app/Calculadora_financiera" class="custom-button" target="_self">Resetear Calculadora</a></body></html>"""
        html = BeautifulSoup(html, 'html.parser')
        st.markdown(html, unsafe_allow_html=True)
         
    #-------------------------------------------------------------------------#
    # 1. Cifras generales
    st.write('Cifras Generales')
    col1, col2, col3, col4  = st.columns(4)
    with col1:
        precio_compra = st.number_input("Precio Compra",value=data['preciocompra'].iloc[0])
        data.loc[0,'preciocompra'] = precio_compra
    with col2:
        options = ["EUR", "USD", "COP", "MXN", "ARS", "CLP"]
        value   = data['moneda'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        moneda = st.selectbox('Tipo de Moneda',options=options,index=index)
        data.loc[0,'moneda'] = moneda
    with col3:
        options = ["General","Reducido","Sujeto Pasivo"]
        value   = data['tipoinversor'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        tipo_inversor = st.selectbox("Tipo Inversor",options=options,index=index )
        data.loc[0,'tipoinversor'] = tipo_inversor
    with col4:
        porcentaje_comision_compra = st.number_input("Porcentaje Comision Compra (%)",value=float(data['porcentajecomisioncompra'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'porcentajecomisioncompra'] = porcentaje_comision_compra
    with col1:
        options = ["Si","No"]
        value   = data['hipoteca'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        hipoteca = st.selectbox("Hipoteca",options=options,index=index)
        data.loc[0,'hipoteca'] = hipoteca
    with col2:
        gastos_escritura_hipoteca = st.number_input("Gastos de Escritura de Hipoteca",value=float(data['gastosescriturahipoteca'].iloc[0]))
        data.loc[0,'gastosescriturahipoteca'] = gastos_escritura_hipoteca
    with col3:
        comision_hipoteca = st.number_input("Comision Hipoteca",value=float(data['comisionhipoteca'].iloc[0]))
        data.loc[0,'comisionhipoteca'] = comision_hipoteca
    with col4:
        seguro = st.number_input("Seguro",value=float(data['seguro'].iloc[0]))
        data.loc[0,'seguro'] = seguro
    with col1:
        superficie_registro = st.number_input("superficie registro",value=float(data['superficieregistro'].iloc[0]))
        data.loc[0,'superficieregistro'] = superficie_registro
    with col2:
        superficie_real = st.number_input("superficie real",value=float(data['superficiereal'].iloc[0]))
        data.loc[0,'superficiereal'] = superficie_real
    with col3:
        e_obra_m2 = st.number_input("$ obra / m2",value=float(data['valorobramt2'].iloc[0]))
        data.loc[0,'valorobramt2'] = e_obra_m2
    with col4:
        markup_cf_obra = st.number_input("Markup CF obra (%)",value=float(data['markupobra'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'markupobra'] = markup_cf_obra
    with col1:
        porcentaje_fee_cf = st.number_input("% Fee CF",value=float(data['feecf'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'feecf'] = porcentaje_fee_cf
        
    # Disable
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if "General" in tipo_inversor:
            value_itp = precio_compra * 0.07
        elif "Reducido" in tipo_inversor:
            value_itp = precio_compra * 0.03
        elif "Sujeto Pasivo" in tipo_inversor:
            value_itp = precio_compra * 0.01
        else:
            value_itp = 0
        itp_registro        = st.number_input("ITP / Registro", value=value_itp,disabled=True)
    with col1:
        comision_compra = st.number_input("Comision Compra", value=porcentaje_comision_compra*precio_compra/100,disabled=True)
    with col1:
        comision_iva = st.number_input("Comision + IVA", value=comision_compra*(1+IVA),disabled=True)
    with col2:
        value         = e_obra_m2*(1+IVA)
        e_obra_m2_iva = st.number_input("$ obra / m2 + IVA", value=value,disabled=True)
    with col2:
        obra_mt2_total = st.number_input("$ Obra / m² (TOTAL)", value=e_obra_m2_iva*(1+markup_cf_obra/100),disabled=True)
    with col2:
        costo_obra_base = st.number_input("Costo Obra (Base)", value=e_obra_m2*superficie_real,disabled=True)
    with col2:
        costo_obra_iva = st.number_input("Costo Obra (IVA)", value=costo_obra_base*(1+IVA),disabled=True)
    with col2:
        valor_obra_total = st.number_input("Budget Obra (Base)", value=costo_obra_base*(1+markup_cf_obra/100),disabled=True)
    with col2:
        valor_obra_total_iva = st.number_input("Budget Obra (IVA)", value=costo_obra_iva*(1+markup_cf_obra/100),disabled=True)
    with col3:
        value  = 7000 if (porcentaje_fee_cf/100)*precio_compra<7000 else (porcentaje_fee_cf/100)*precio_compra
        fee_cf = st.number_input("Fee CF", value=value,disabled=True)
    with col3:
        fee_cf_iva = st.number_input("Fee CF (IVA)", value=fee_cf*(1+IVA),disabled=True)
    with col4:
        value           = precio_compra+itp_registro+comision_compra+gastos_escritura_hipoteca+seguro+comision_hipoteca+valor_obra_total+fee_cf
        total_invertido = st.number_input("TOTAL INVERTIDO", value=value,disabled=True)
    with col4:
        value              = precio_compra+itp_registro+comision_iva+gastos_escritura_hipoteca+seguro+comision_hipoteca+valor_obra_total_iva+fee_cf_iva
        total_cashflow_iva = st.number_input("TOTAL CashFlow (IVA)", value=value,disabled=True)


    #-------------------------------------------------------------------------#
    # 2. Friend stay
    st.write('---')
    st.write(' Friend Stay')
    result_doorms = []
    valor_renta_total = 0
    col1,col2     = st.columns(2)    
    with col1:
        options = ['Propiedad completa','Friend Stay']
        value   = data['tipoalquiler'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        tipo_arriendo = st.selectbox('Tipo de arriendo',options=options,index=index)
        data.loc[0,'tipoalquiler'] = tipo_arriendo
    if 'Propiedad completa' in tipo_arriendo:
        tasa_ocupacion    = 1
        value_spread      = 0
        num_prod          = 1
        data.loc[0,'iva_renta_mensual'] = 0
        with col2:
            valor_total_recaudado = st.number_input('Valor total renta',value=float(data['valortotalrenta'].iloc[0]),min_value=0.0)
            data.loc[0,'valortotalrenta'] = valor_total_recaudado
    elif 'Friend Stay' in tipo_arriendo:
        value_spread = 130
        with col1: 
            tasa_ocupacion    = st.number_input('Tasa de ocupacion',value=float(data['tasaocupacion'].iloc[0]),step=0.1)
            data.loc[0,'tasaocupacion'] = tasa_ocupacion
            tasa_ocupacion    = tasa_ocupacion/100
            
        #for j in json.loads(data['habitaciones'].iloc[0]):
        conteo = 0
        for j in data['habitaciones'].iloc[0]:
            conteo += 1
            col1, col2, col3, col4 = st.columns(4)
            with col1: 
                options = ['Doble','Sencilla']
                value   = j['tipohabitacion']
                index   = 0
                if value is not None and value!='':
                    index = options.index(value)
                tipo_hab = st.selectbox(f'Tipo de habitacion ({conteo})', options=options,index=index)
            with col2:
                num_hab  = st.number_input(f'Número de habitaciones ({conteo})',value=j['numerohabitaciones'])
            with col3:
                renta_mes_hab = st.number_input(f'Renta mes ({conteo})', value=float(j['valorhabitacion']),min_value=0.0)
            with col4:
                subtotal = st.number_input(f'Subtotal ({conteo})', value=renta_mes_hab*num_hab,disabled=True)
            result_doorms.append({'tipohabitacion':tipo_hab,'numerohabitaciones':num_hab,'valorhabitacion':renta_mes_hab,'subtotal':subtotal})
                
        valor_total_recaudado = 0
        num_prod              = 0
        for j in result_doorms:
            if 'subtotal' in j:
                valor_total_recaudado += j['subtotal']
            if 'numerohabitaciones'  in j:
                num_prod += j['numerohabitaciones']

        col1,col2 = st.columns(2)  
        with col1:
            valor_renta_total = st.number_input('Renta TOTAL',value=valor_total_recaudado,disabled=True)
        with col2:
            valor_total_recaudado = st.number_input('Renta RECAUDADA',value=valor_total_recaudado*tasa_ocupacion,disabled=True)
    
    data.loc[0,'habitaciones'] = json.dumps(result_doorms)
    
    #-------------------------------------------------------------------------#
    # 3. Margen operativo
    st.write('---')
    st.write(' Margen Operativo')
    col1,col2,col3 = st.columns(3)
    with col1:
        margen_hab = st.number_input('Margen x hab',value=float(data['margenxhabitacion'].iloc[0]))
        data.loc[0,'margenxhabitacion'] = margen_hab
    with col2:
        spread_renttee = st.number_input('Spread Renttee',value=margen_hab*num_prod,disabled=True)
    with col3:
        monto_renta_mensual = st.number_input('Flujo mes inversión',value=valor_total_recaudado-spread_renttee,disabled=True)
     
    with col1:
        suministros = st.number_input('Suministros',value=float(data['suministros'].iloc[0]))
        data.loc[0,'suministros'] = suministros
    with col2:
        valor_total_suministros = st.number_input('Valor total suministros',value=suministros*num_prod,disabled=True)
    with col3:
        monto_renta_mensual = st.number_input('Flujo mes inversión menos suministros',value=valor_total_recaudado-spread_renttee-valor_total_suministros,disabled=True)

    #-------------------------------------------------------------------------#
    # 4. Alquiler
    st.write('---')
    st.write('Alquiler')
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.number_input('Monto mensual',value=monto_renta_mensual,disabled=True)
    with col2:
        iva_renta_mensual = st.number_input('IVA',value=float(data['iva_renta_mensual'].iloc[0]))
        data.loc[0,'iva_renta_mensual'] = iva_renta_mensual
        iva_renta_mensual = iva_renta_mensual/100
    with col3:
        base_renta_mensual = st.number_input('Base',value=monto_renta_mensual/(1+iva_renta_mensual),disabled=True)
    with col4:
        valor_iva_mensual = st.number_input('IVA renta',value=(monto_renta_mensual-base_renta_mensual) ,disabled=True)
    
    with col1:
        roi = st.number_input('ROI',value=(base_renta_mensual*12/total_cashflow_iva)*100,disabled=True)
        
        
    #-------------------------------------------------------------------------#
    # 5. Resumen
    st.write('---')
    st.write('RESUMEN PROYECTO')
    col1,col2 = st.columns(2)
    with col1:
        st.number_input('Precio de compra',value=precio_compra,disabled=True,key='r-preciocompra')
        st.number_input('ITP / Registro',value=itp_registro,disabled=True,key='r-itp')
        st.number_input('Comision Venta',value=comision_iva,disabled=True,key='r-comisionventa')
        st.number_input('Seguro',value=seguro,disabled=True,key='r-seguro')
        st.number_input('Comision Hipoteca',value=comision_hipoteca,disabled=True,key='r-comisionhip')
        st.number_input('Gasto Obra',value=valor_obra_total_iva,disabled=True,key='r-gastoobra')
        st.number_input('Fee CF',value=fee_cf_iva,disabled=True,key='r-feecf')
        st.number_input('TOTAL INV',value=total_cashflow_iva,disabled=True,key='r-totalinv')
        st.number_input('Superficie Obra (m²)',value=superficie_real,disabled=True,key='r-superficieobra')


    #-------------------------------------------------------------------------#
    # 6. Crédito Hipotecário
    
    st.write('---')
    st.write('Simulador cuota del crédito hipotecário')
    col1,col2,col3 = st.columns(3)
    with col1:
        plazo_credito = st.selectbox('Plazo del crédito (años)',options=[5,10,15,20,30],index=3,key='plazo-simulacioncredithip')

    df = pd.DataFrame([40,35,30,25,20,15,10,5],columns=['Aporte'])
    df['Monto a Financiar'] = (1-df['Aporte']/100)*precio_compra
    
    for tasa_credito in [3.25,3.5,3.75,4,4.25,4.5]:
        tasa_interes = (tasa_credito/100)/12   
        df[f'{tasa_credito}%'] = df['Monto a Financiar'].apply(lambda x: round(npf.pmt(tasa_interes, plazo_credito*12,x),2))
    st.dataframe(df,width=1200,hide_index=True)
    
    st.write('---')
    st.write('Crédito Hipotecário')
    col1,col2,col3 = st.columns(3)
 
    with col1:
        options = [5,10,15,20,25,30,35,40]
        value   = data['aporte'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        aporte = st.selectbox('Aporte (%)',options=options,index=index)
        data.loc[0,'aporte'] = aporte
        
    with col2:
        options = [5,10,15,20,30]
        value   = data['plazo_credito'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        plazo_credito = st.selectbox('Plazo del crédito (años)',options=options,index=index)
        data.loc[0,'plazo_credito'] = plazo_credito

    with col3:
        options = [3.25,3.5,3.75,4,4.25,4.5,5,5.5,6]
        value   = data['tasa_credito'].iloc[0]
        index   = 0
        if value is not None and value!='':
            index = options.index(value)
        tasa_credito = st.selectbox('Tasa del crédito (%)',options=options,index=index)
        data.loc[0,'tasa_credito'] = tasa_credito
    
    tasa_interes = (tasa_credito/100)/12  
    numero_pagos = plazo_credito*12  
    pago         = npf.pmt(tasa_interes, numero_pagos,precio_compra*(1-(aporte/100)))
    
    col1,col2 = st.columns(2)
    with col1:
        st.number_input('HIPOTECA AL',value=100-aporte,disabled=True,key='h-hipotecaal')
        st.number_input('Precio Compra',value=precio_compra,disabled=True,key='h-preciocompra')
        st.number_input('Banco',value=precio_compra*(1-(aporte/100)),disabled=True,key='h-banco')
        st.number_input('Aporte',value=precio_compra*(aporte/100),disabled=True,key='h-aporte')
        presupuestototal = st.number_input('Presupuesto Total',value=total_cashflow_iva-precio_compra*(1-(aporte/100)),disabled=True,key='h-presupuesto')
        pesoinversor     = st.number_input('Peso TOTAL Inversor',value=(total_cashflow_iva-precio_compra*(1-(aporte/100)))/total_cashflow_iva*100,disabled=True,key='h-pesopresupuesto')
        st.number_input('Peso Banco',value=(100-pesoinversor),disabled=True,key='h-pesobanco')

    with col2:
        st.number_input('Alquiler Mensual Base',value=base_renta_mensual,disabled=True,key='h-alquilermensual')
        st.number_input('Alquiler Anual Base',value=base_renta_mensual*12,disabled=True,key='h-alquileranual')
        st.number_input('Tasa de Interes',value=tasa_credito,disabled=True,key='h-tasainteres')
        st.number_input('Hipoteca Mensual',value=pago,disabled=True,key='h-hipotecamensual')
        st.number_input('Hipoteca Anual',value=pago*12,disabled=True,key='h-hipotecaanual')
        flujocajamensual = st.number_input('Flujo de Caja Mensual',value=base_renta_mensual+pago,disabled=True,key='h-flujocajamensual')
        st.number_input('Flujo de Caja Anual',value=flujocajamensual*12,disabled=True,key='h-flujocajaanual')

        st.number_input('Cash on Cash',value=base_renta_mensual*12/presupuestototal*100,disabled=True,key='h-cashoncash')
        st.number_input('ROI proyecto',value=roi,disabled=True,key='h-roi')

        seguromensual = st.number_input("Seguro Mensual",value=data['seguromensual'].iloc[0])
        data.loc[0,'seguromensual'] = seguromensual
        
        ibi = st.number_input("IBI",value=data['IBI'].iloc[0])
        data.loc[0,'IBI'] = ibi

        comunidadvecinos = st.number_input("Comudidad Vecinos",value=data['comunidadvecinos'].iloc[0])
        data.loc[0,'comunidadvecinos'] = comunidadvecinos
        
        totalgastosmensual = st.number_input('TOTAL Gastos mes',value=seguromensual+ibi+comunidadvecinos,disabled=True,key='h-totalgastosmes')

        st.number_input('CASH FLOW NETO MES',value=flujocajamensual-totalgastosmensual,disabled=True,key='h-fliujocajamensualneto')
        #st.number_input('SALDO PRESUPUESTO',value=flujocajamensual-totalgastosmensual,disabled=True,key='h-totalgastosmes')
        
        
    #-------------------------------------------------------------------------#
    # 7. Diagnostico
    st.write('---')
    st.write('DIAGNOSTICO')
    col1,col2 = st.columns(2)
    with col1:
        ahorro_disponible = st.number_input("Ahorro disponible",value=data['ahorro_disponible'].iloc[0])
        data.loc[0,'ahorro_disponible'] = ahorro_disponible
        per_itp = st.number_input("ITP (%)",value=data['per_itp'].iloc[0])
        data.loc[0,'per_itp'] = per_itp
        per_inmobiliaria = st.number_input("Comisión inmobiliaria",value=data['per_inmobiliaria'].iloc[0])
        data.loc[0,'per_inmobiliaria'] = per_inmobiliaria
        porcentaje_fee_cf = st.number_input("Capital Friend",value=float(data['feecf'].iloc[0]),min_value=0.0,step=0.1,disabled=True,key='h-feecapitalfriend')
        st.number_input('% Aporte Hipoteca',value=aporte,disabled=True,key='h-aportediag')
        st.number_input("Obra (IVA incluido)", value=valor_obra_total_iva,disabled=True,key='h-obradiag')
        preciomaximo = (ahorro_disponible-valor_obra_total_iva)/( (per_itp/100)+((per_inmobiliaria/100)*1.21)+((porcentaje_fee_cf/100)*1.21)+(aporte/100))
        st.number_input("Precio Maximo", value=preciomaximo,disabled=True,key='h-preciomaxdiag')

        st.write("")
        st.write("")
        st.write("")
        ingresonetomes = st.number_input("Ingreso Neto Mes", value=data['ingresonetomes'].iloc[0],key='h-ingresomax')
        data.loc[0,'ingresonetomes'] = ingresonetomes
        cuotamaxima = st.number_input("Cuota maxima", value=-ingresonetomes*0.35,disabled=True,key='h-cuotamax')

    with col2:
        st.text_input(" ",value="",disabled=True,key='h-nonvalue1')
        st.number_input("ITP",value=preciomaximo*per_itp/100,disabled=True,key='h-itpvalor')
        st.number_input("Comisión inmobiliaria",value=preciomaximo*per_inmobiliaria*1.21/100,disabled=True,key='h-comisioninmob')
        st.number_input("Capital Friend",value=preciomaximo*porcentaje_fee_cf*1.21/100,disabled=True,key='h-capitalfrienddiag')
        st.number_input('% Aporte Hipoteca',value=preciomaximo*aporte/100,disabled=True,key='h-aportediagvalor')
        st.number_input("Obra (IVA incluido)", value=valor_obra_total_iva,disabled=True,key='h-obradiagvalor')


    #-------------------------------------------------------------------------#
    # Guardar data
    st.write('---')
    st.write('Guardar calculadora en proyecto')
    col1,col2 = st.columns(2)
    col1,col2 = st.columns(2)
    with col1:
        nombreproyecto     = None
        datalistaproyectos = listaproyectos()
        datalistaproyectos = datalistaproyectos[datalistaproyectos['nombre_proyecto'].notnull()]
        if codigo_proyecto is not None:
            datalistaproyectos = datalistaproyectos[datalistaproyectos['codigo_proyecto']==codigo_proyecto]
            
        if not datalistaproyectos.empty:
            options = ['']+sorted(datalistaproyectos['nombre_proyecto'].unique())
            nombreproyecto = st.selectbox('Nombre del proyecto',options=options)
        
    with col2:
        if isinstance(nombreproyecto, str) and nombreproyecto!='': 
            st.write('')
            st.write('')
            inputvar       = {'json':json.dumps(data.to_dict(orient='records')[0])}
            codigo_name    = None
            codigo_cliente = None
            codigo_proyecto = datalistaproyectos[datalistaproyectos['nombre_proyecto']==nombreproyecto]['codigo_proyecto'].iloc[0]
            updateinfoinversionista(inputvar,codigo_name,codigo_cliente,codigo_proyecto,'cj_calculadora',data,userchange,'button_info_calculadora')
            