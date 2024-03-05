import streamlit as st
import pandas as pd
import json

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
    
    #-------------------------------------------------------------------------#
    # 5. Gastos mes
    st.write('---')
    st.write('Gastos Mes')
    result_services = []
    with st.expander('Servicios mensuales'):
        formato = data['servicios'].iloc[0]
        conteo = 0
        for j in formato:
            conteo += 1
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: 
                tipo_servicio = st.text_input('Tipo de servicio',key=f'tipo_servicio_({conteo+1})',value=j["variable"])
            with col2:
                valor_servicio  = st.number_input('Valor del servicio',key=f'valor_servicio_({conteo+1})',value=j['value'])
            with col3:
                iva_servicio  = st.number_input('IVA del servicio',key=f'iva_servicio_({conteo+1})',value=j['IVA'])
            with col4:
                base_servicio  = st.number_input('Base',key=f'base_servicio_({conteo+1})',value=valor_servicio/(1+(iva_servicio/100)),disabled=True)
            with col5:
                pagoiva_servicio  = st.number_input('IVA',key=f'pagoiva_servicio_({conteo+1})',value=valor_servicio-base_servicio,disabled=True)
            result_services.append({'variable':tipo_servicio,'value':valor_servicio,'IVA':iva_servicio,'base_servicio':base_servicio,'pagoiva_servicio':pagoiva_servicio})
    
    data.loc[0,'servicios'] = json.dumps(result_services)
    valor_total_servicio = 0
    valor_base_servicio  = 0
    valor_IVA_servicio   = 0
    for j in result_services:
        if 'value' in j:
            valor_total_servicio += j['value']
        if 'base_servicio' in j:
            valor_base_servicio += j['base_servicio']
        if 'pagoiva_servicio' in j:
            valor_IVA_servicio += j['pagoiva_servicio'] 
            
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input('Total valor de los servicios mensuales',value=valor_total_servicio,disabled=True)
    with col2: 
        st.number_input('Total valor de los servicios Base',value=valor_base_servicio,disabled=True)
    with col3: 
        st.number_input('Total IVA de los servicios mensuales',value=valor_IVA_servicio,disabled=True)
        
    #-------------------------------------------------------------------------#
    # 6. Costo firma de contrato
    st.write('---')
    st.write('Costo Firma de Contrato')
    result_tabla_contrato = []
    formato = data["firmacontrato"].iloc[0]
    for i in formato:
        if "Mes en Curso" in i["variable"]:
            i["value"] = monto_renta_mensual
    conteo = 0
    for j in formato:
        conteo += 1
        isdisabled = False
        col1, col2, col3, col4, col5,col6 = st.columns(6)
        with col1: 
            tabla_contrato_tipo = st.text_input('Descripción',key=f'tabla_contrato_tipo_({conteo+1})',value=j["variable"])
        with col2:
            options = [1,0]
            value   = j['cantidad']
            index   = 0
            if value is not None and value!='':
                index = options.index(value)
            tabla_contrato_cantidad = st.selectbox('Cantidad',key=f'tabla_contrato_cantidad_({conteo+1})',options=options,index=index)
        if tabla_contrato_cantidad==0: isdisabled = True
        with col3:
            tabla_contrato_monto  = st.number_input('Monto',key=f'tabla_contrato_monto_({conteo+1})',value=j['value']*tabla_contrato_cantidad,disabled=isdisabled)
        with col4:
            tabla_contrato_iva  = st.number_input('IVA',key=f'tabla_contrato_iva_({conteo+1})',value=j["IVA"],disabled=isdisabled)
        with col5:
            tabla_contrato_base  = st.number_input('Base',key=f'tabla_contrato_base_({conteo+1})',value=tabla_contrato_monto/(1+(tabla_contrato_iva/100)),disabled=True)
        with col6:
            tabla_contrato_pagoiva  = st.number_input('Pago IVA',key=f'tabla_contrato_pagoiva_({conteo+1})',value=tabla_contrato_monto-tabla_contrato_base,disabled=True)
        result_tabla_contrato.append({'variable':tabla_contrato_tipo,'cantidad':tabla_contrato_cantidad,'value':tabla_contrato_monto,'IVA':tabla_contrato_iva,'tabla_contrato_base':tabla_contrato_base,'tabla_contrato_pagoiva':tabla_contrato_pagoiva})
        
    data.loc[0,'firmacontrato'] = json.dumps(result_tabla_contrato)
    valor_total_tabla_contrato = 0
    valor_base_tabla_contrato  = 0
    valor_IVA_tabla_contrato   = 0
    for j in result_tabla_contrato:
        if 'value' in j:
            valor_total_tabla_contrato += j['value']
        if 'tabla_contrato_base' in j:
            valor_base_tabla_contrato += j['tabla_contrato_base']
        if 'tabla_contrato_pagoiva' in j:
            valor_IVA_tabla_contrato += j['tabla_contrato_pagoiva'] 
            
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input('Total Monto',key='monto_tabla_contrato',value=valor_total_tabla_contrato,disabled=True)
    with col2: 
        st.number_input('Total Base',key='base_tabla_contrato',value=valor_base_tabla_contrato,disabled=True)
    with col3: 
        st.number_input('Total IVA',key='iva_tabla_contrato',value=valor_IVA_tabla_contrato,disabled=True)
                     
        
    #-------------------------------------------------------------------------#
    # 7. Simulacion
    st.write('---')
    st.write('Simulacion')

    facto_descuento = st.number_input('Factor de descuento', value=float(data['factordescuento'].iloc[0]),min_value=0.0,step=0.1)
    data.loc[0,'factordescuento'] = facto_descuento
    facto_descuento = facto_descuento/100
    
    col1,col2 = st.columns(2)
    with col1:
        ipc_alquiler_1 = st.number_input('Incre Alquileres (ano 1)', value=float(data['incrementoalquileresano1'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'incrementoalquileresano1'] = ipc_alquiler_1
    with col2:
        ipc_general_1 = st.number_input('IPC (ano 1)', value=float(data['ipcano1'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'ipcano1'] = ipc_general_1
        
    col1,col2 = st.columns(2)
    with col1:
        ipc_alquiler_2 = st.number_input('Incre Alquileres (ano 2)', value=float(data['incrementoalquileresano2'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'incrementoalquileresano2'] = ipc_alquiler_2
    with col2:
        ipc_general_2 = st.number_input('IPC (ano 2)', value=float(data['ipcano2'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'ipcano2'] = ipc_general_2
        
    ipc_alquiler = [1]+[1]*12+[1+(ipc_alquiler_1/100)]*12+ [(1+(ipc_alquiler_1/100))*(1+(ipc_alquiler_2/100))]*12 
    ipc_general  = [1]+[1]*12+[1+(ipc_general_1/100)]*12+ [(1+(ipc_general_1/100))*(1+(ipc_general_2/100))]*12 

    filas    = ['IVA adeudado (-) Habs', 'Base Facturación Habs', 'Facturación Habs', 'IVA Alquiler (+)', 'Base Alquiler', 'Alquiler Mensual', 'IVA Gastos (+)', 'Base Gastos', 'Gastos Mensuales', 'IVA Firma Contrato (+)', 'Base Firma Contrato', 'Total Costo Firma Contrato', 'Saldo IVA Periodo', 'IVA a favor acumulado', 'Saldo Contable Periodo', 'Saldo Caja Periodo', 'FC IVA', 'FC Contable', 'FC Real']
    columnas = list(range(1, 37))
    df       = pd.DataFrame(index=filas, columns=columnas)
    
    # Mes 1:
    i_0            = ['IVA adeudado (-) Habs', 'Base Facturación Habs', 'Facturación Habs', 'IVA Alquiler (+)', 'Base Alquiler', 'Alquiler Mensual', 'IVA Gastos (+)', 'Base Gastos', 'Gastos Mensuales']
    df.loc[i_0, 1] = 0
    df.loc['IVA Firma Contrato (+)', 1]     = valor_IVA_tabla_contrato
    df.loc['Base Firma Contrato', 1]        = valor_base_tabla_contrato
    df.loc['Total Costo Firma Contrato', 1] = valor_total_tabla_contrato
    df.loc['Saldo IVA Periodo', 1]          = valor_IVA_tabla_contrato
    df.loc['IVA a favor acumulado', 1]      = valor_IVA_tabla_contrato
    df.loc['Saldo Contable Periodo', 1]     = (-1)*valor_base_tabla_contrato
    df.loc['Saldo Caja Periodo', 1]         = (-1)*valor_total_tabla_contrato
    df.loc['FC IVA', 1]                     = valor_IVA_tabla_contrato
    df.loc['FC Contable', 1]                = (-1)*valor_base_tabla_contrato
    df.loc['FC Real', 1]                    = (-1)*valor_total_tabla_contrato

    # Mes 2:
    df.loc['Base Facturación Habs', 2] = (valor_total_recaudado/(1+facto_descuento))*2
    df.loc['Facturación Habs', 2]      = valor_total_recaudado+(valor_total_recaudado/(1+facto_descuento))
    df.loc['IVA adeudado (-) Habs', 2] = df.loc['Facturación Habs', 2]-df.loc['Base Facturación Habs', 2]
    
    df.loc['Base Alquiler', 2]    = base_renta_mensual
    df.loc['Alquiler Mensual', 2] = monto_renta_mensual
    df.loc['IVA Alquiler (+)', 2] = df.loc['Alquiler Mensual', 2]-df.loc['Base Alquiler', 2]
    
    df.loc['Base Gastos', 2]      = valor_base_servicio
    df.loc['Gastos Mensuales', 2] = valor_total_servicio
    df.loc['IVA Gastos (+)', 2]   = df.loc['Gastos Mensuales', 2]-df.loc['Base Gastos', 2]
    
    df.loc['IVA Firma Contrato (+)', 2]     = 0
    df.loc['Base Firma Contrato', 2]        = 0
    df.loc['Total Costo Firma Contrato', 2] = 0

    df.loc['Saldo IVA Periodo', 2]          = (-1)*df.loc['IVA adeudado (-) Habs', 2] + df.loc['IVA Alquiler (+)', 2] + df.loc['IVA Gastos (+)', 2] + df.loc['IVA Firma Contrato (+)', 2] 
    df.loc['IVA a favor acumulado', 2]      = df.loc['IVA a favor acumulado', 1]+df.loc['Saldo IVA Periodo', 2]

    df.loc['Saldo Contable Periodo', 2]     = df.loc['Base Facturación Habs', 2]-df.loc['Base Alquiler', 2]-df.loc['Base Gastos', 2]-df.loc['Base Firma Contrato', 2]
    df.loc['Saldo Caja Periodo', 2]         = df.loc['Facturación Habs', 2]-df.loc['Alquiler Mensual', 2]-df.loc['Gastos Mensuales', 2]-df.loc['Total Costo Firma Contrato', 2]

    df.loc['FC IVA', 2]                     = df.loc['FC IVA', 1]+df.loc['Saldo IVA Periodo', 2]
    df.loc['FC Contable', 2]                = df.loc['FC Contable', 1]+df.loc['Saldo Contable Periodo', 2]
    df.loc['FC Real', 2]                    = df.loc['FC Real', 1]+df.loc['Saldo Caja Periodo', 2]
    
    # Mes 3 a 36:
    for i in range(3,37):
        df.loc['Base Facturación Habs', i] = (valor_total_recaudado/(1+facto_descuento))*ipc_alquiler[i]
        df.loc['Facturación Habs', i]      = valor_total_recaudado*ipc_alquiler[i]
        df.loc['IVA adeudado (-) Habs', i] = df.loc['Facturación Habs', i]-df.loc['Base Facturación Habs', i]

        df.loc['Base Alquiler', i]    = base_renta_mensual*ipc_general[i]
        df.loc['Alquiler Mensual', i] = monto_renta_mensual*ipc_general[i]
        df.loc['IVA Alquiler (+)', i] = df.loc['Alquiler Mensual', i]-df.loc['Base Alquiler', i]

        df.loc['Base Gastos', i]      = valor_base_servicio
        df.loc['Gastos Mensuales', i] = valor_total_servicio
        df.loc['IVA Gastos (+)', i]   = df.loc['Gastos Mensuales', i]-df.loc['Base Gastos', i]
 
        df.loc['IVA Firma Contrato (+)', i]     = 0
        df.loc['Base Firma Contrato', i]        = 0
        df.loc['Total Costo Firma Contrato', i] = 0

        df.loc['Saldo IVA Periodo', i]          = (-1)*df.loc['IVA adeudado (-) Habs', i] + df.loc['IVA Alquiler (+)', i] + df.loc['IVA Gastos (+)', i] + df.loc['IVA Firma Contrato (+)', i] 
        df.loc['IVA a favor acumulado', i]      = df.loc['IVA a favor acumulado', i-1]+df.loc['Saldo IVA Periodo', i]

        df.loc['Saldo Contable Periodo', i]     = df.loc['Base Facturación Habs', i]-df.loc['Base Alquiler', i]-df.loc['Base Gastos', i]-df.loc['Base Firma Contrato', i]
        df.loc['Saldo Caja Periodo', i]         = df.loc['Facturación Habs', i]-df.loc['Alquiler Mensual', i]-df.loc['Gastos Mensuales', i]-df.loc['Total Costo Firma Contrato', i]

        df.loc['FC IVA', i]                     = df.loc['FC IVA', i-1]+df.loc['Saldo IVA Periodo', i]
        df.loc['FC Contable', i]                = df.loc['FC Contable', i-1]+df.loc['Saldo Contable Periodo', i]
        df.loc['FC Real', i]                    = df.loc['FC Real', i-1]+df.loc['Saldo Caja Periodo', i]

    st.dataframe(df)
    
    #-------------------------------------------------------------------------#
    # 8. Renttee
    st.write('---')
    st.write('Renttee')

    filas      = ['Flujo Contable / mes','Saldo IVA / mes','FC Real / mes']
    columnas   = list(range(1, 4))
    df_renttee = pd.DataFrame(index=filas, columns=columnas)

    df_renttee.loc['Flujo Contable / mes',1] = df.loc['Saldo Contable Periodo',3]
    df_renttee.loc['Flujo Contable / mes',2] = df.loc['Saldo Contable Periodo',13]
    df_renttee.loc['Flujo Contable / mes',3] = df.loc['Saldo Contable Periodo',25]
 
    df_renttee.loc['Saldo IVA / mes',1] = df.loc['Saldo IVA Periodo',3]
    df_renttee.loc['Saldo IVA / mes',2] = df.loc['Saldo IVA Periodo',13]
    df_renttee.loc['Saldo IVA / mes',3] = df.loc['Saldo IVA Periodo',25]
 
    df_renttee.loc['FC Real / mes',1] = df.loc['Saldo Caja Periodo',3]
    df_renttee.loc['FC Real / mes',2] = df.loc['Saldo Caja Periodo',13]
    df_renttee.loc['FC Real / mes',3] = df.loc['Saldo Caja Periodo',25]    
    
    st.dataframe(df_renttee)
    
    #-------------------------------------------------------------------------#
    # 9. Metricas
    st.write('---')
    st.write('Metricas')
    result_tabla_metricas = []
    precio_compra = 1 if precio_compra==0 else precio_compra
    
    col1,col2,col3 = st.columns(3)
    with col1:
        ibi = st.number_input("IBI",value=float(data['ibi'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'ibi'] = ibi
    with col2:
        basegestoriames = st.number_input("Base Gestoria Mes",value=float(data['basegestoriames'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'basegestoriames'] = basegestoriames
    with col3:
        carry = st.number_input("Carry",value=float(data['carry'].iloc[0]),min_value=0.0,step=0.1)
        data.loc[0,'carry'] = carry
        
    fotmato = [
        {'variable':'Base alquiler mes','disabled':True,'value':base_renta_mensual},
        {'variable':'Base alquiler anual','disabled':True,'value':base_renta_mensual*12},
        {'variable':'Alquiler mes IVA','disabled':True,'value':monto_renta_mensual},
        {'variable':'Alquiler anual IVA','disabled':True,'value':monto_renta_mensual*12},
        {'variable':'Precio Compra','disabled':True,'value':precio_compra},
        {'variable':'Yield','disabled':True,'value':valor_renta_total*12/precio_compra*100},
        {'variable':'Gestoria Mes (IVA)','disabled':True,'value':basegestoriames*(1+IVA)},
        {'variable':'ROI','disabled':True,'value': base_renta_mensual*12/total_cashflow_iva*100}
            ]
    
    col1, col2 = st.columns(2)
    for j in fotmato:
        with col1: 
            variable = j['variable']
            disabled = j['disabled']
            value    = j['value']
            st.number_input(variable,key=f'{variable}_seccion8',value=value,disabled=disabled)
        result_tabla_metricas.append(j)
    
    fotmato = [
        {'variable':'Ing Alq Aµo 1','disabled':True,'value':df.loc['Base Alquiler',[1,2,3,4,5,6,7,8,9,10,11,12]].sum()},
        {'variable':'Ing Alq Aµo 2','disabled':True,'value':df.loc['Base Alquiler',[13,14,15,16,17,18,19,20,21,22,23,24]].sum()},
        {'variable':'Ing Alq Aµo 3','disabled':True,'value':df.loc['Base Alquiler',[25,26,27,28,29,30,31,32,33,34,35,36]].sum()},
        {'variable':'Total Ing Alq','disabled':True,'value':df.loc['Base Alquiler',:].sum()},
        {'variable':'Ingresos x Venta','disabled':True,'value':0},
        {'variable':'Total Ingresos','disabled':True,'value':0},
        {'variable':'Base Gestoria Aµo','disabled':True,'value':0},
        {'variable':'Gestoria Aµo (IVA)','disabled':True,'value':0},
        {'variable':'C Oper + IBI','disabled':True,'value':0},
        {'variable':'Rent Neta','disabled':True,'value':0},
            ]
    for j in fotmato:
        with col2: 
            variable = j['variable']
            disabled = j['disabled']
            value    = j['value']
            st.number_input(variable,key=f'{variable}_seccion8',value=value,disabled=disabled)
        result_tabla_metricas.append(j)
        
    
    col1,col2 = st.columns(2)
    with col1:
        nombreproyecto     = None
        datalistaproyectos = listaproyectos()
        
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