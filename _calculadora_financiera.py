import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def main():
    IVA = 0.21
    
    #-------------------------------------------------------------------------#
    # 1. Cifras generales
    st.write('Cifras Generales')
    col1, col2 = st.columns(2)
    with col1:
        precio_compra = st.number_input("Precio Compra", value=0)
    with col2:
        moneda = st.selectbox('Tipo de Moneda',options=["EUR", "USD", "COP", "MXN", "ARS", "CLP"])
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_inversor = st.selectbox("Tipo Inversor", ["General","Reducido","Sujeto Pasivo"])
    
    if "General" in tipo_inversor:
        value = precio_compra * 0.07
    elif "Reducido" in tipo_inversor:
        value = precio_compra * 0.03
    elif "Sujeto Pasivo" in tipo_inversor:
        value = precio_compra * 0.01
    else:
        value = 0
    with col2:
        itp_registro        = st.number_input("ITP / Registro", value=value,disabled=True)
    
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        porcentaje_comision_compra = st.number_input("Porcentaje Comision Compra (%)", value=3.0,min_value=0.0,step=0.1)
    with col2:
        comision_compra     = st.number_input("Comision Compra", value=porcentaje_comision_compra*precio_compra/100,disabled=True)
    with col3:
        comision_iva        = st.number_input("Comision + IVA", value=comision_compra*(1+IVA),disabled=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        hipoteca = st.selectbox("Hipoteca", ["Si","No"])
    with col2:
        gastos_escritura_hipoteca = st.number_input("Gastos de Escritura de Hipoteca", value=0)
    with col3:
        comision_hipoteca = st.number_input("Comision Hipoteca", value=0)
    with col4:
        seguro = st.number_input("Seguro", value=1000)
    
    col1, col2 = st.columns(2)
    with col1:
        superficie_registro = st.number_input("superficie registro", value=0)
    with col2:
        superficie_real = st.number_input("superficie real", value=0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        e_obra_m2           = st.number_input("$ obra / m2", value=780.0)
    with col2:
        value               = e_obra_m2*(1+IVA)
        e_obra_m2_iva       = st.number_input("$ obra / m2 + IVA", value=value,disabled=True)
    with col3:
        costo_obra_base     = st.number_input("Costo Obra (Base)", value=e_obra_m2*superficie_real,disabled=True)
    with col4:
        costo_obra_iva      = st.number_input("Costo Obra (IVA)", value=costo_obra_base*(1+IVA),disabled=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        markup_cf_obra      = st.number_input("Markup CF obra (%)", value=19.0,min_value=0.0,step=0.1)
    with col2:
        obra_mt2_total      = st.number_input("$ Obra / m² (TOTAL)", value=e_obra_m2_iva*(1+markup_cf_obra/100),disabled=True)
    with col3:
        valor_obra_total    = st.number_input("Budget Obra (Base)", value=costo_obra_base*(1+markup_cf_obra/100),disabled=True)
    with col4:
        valor_obra_total_iva = st.number_input("Budget Obra (IVA)", value=costo_obra_iva*(1+markup_cf_obra/100),disabled=True)
    
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        porcentaje_fee_cf = st.number_input("% Fee CF", value=3.5,min_value=0.0,step=0.1)
    with col2:
        value  = 7000 if (porcentaje_fee_cf/100)*precio_compra<7000 else (porcentaje_fee_cf/100)*precio_compra
        fee_cf = st.number_input("Fee CF", value=value,disabled=True)
    with col3:
        fee_cf_iva = st.number_input("Fee CF (IVA)", value=fee_cf*(1+IVA),disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        value               = precio_compra+itp_registro+comision_compra+gastos_escritura_hipoteca+seguro+comision_hipoteca+valor_obra_total+fee_cf
        total_invertido     = st.number_input("TOTAL INVERTIDO", value=value,disabled=True)
    with col2:
        value               = precio_compra+itp_registro+comision_iva+gastos_escritura_hipoteca+seguro+comision_hipoteca+valor_obra_total_iva+fee_cf_iva
        total_cashflow_iva  = st.number_input("TOTAL CashFlow (IVA)", value=value,disabled=True)


    #-------------------------------------------------------------------------#
    # 2. Friend stay
    st.write('---')
    st.write(' Friend Stay')
    result_doorms = []
    col1,col2     = st.columns(2)    
    with col1:
        tipo_arriendo = st.selectbox('Tipo de arriendo', options=['Propiedad completa','Friend Stay'])
    if 'Propiedad completa' in tipo_arriendo:
        tasa_ocupacion    = 1
        value_spread      = 0
        num_prod          = 1
        iva_renta_mensual = 0
        with col2:
            valor_total_recaudado = st.number_input('Valor total renta',value=0.0)
    
    elif 'Friend Stay' in tipo_arriendo:
        value_spread = 130
        with col1: 
            tasa_ocupacion    = st.number_input('Tasa de ocupacion', value=95.0,step=0.1)
            tasa_ocupacion    = tasa_ocupacion/100
            iva_renta_mensual = IVA*100
        for j in range(2):
            col1, col2, col3, col4 = st.columns(4)
            with col1: 
                tipo_hab = st.selectbox(f'Tipo de habitacion ({j+1})', options=['Doble','Sencilla'])
            with col2:
                num_hab  = st.selectbox(f'Número de habitaciones ({j+1})', options=[1,2,3,4,5,6])
            with col3:
                if 'Doble' in tipo_hab: value = 690.0
                elif 'Sencilla' in tipo_hab: value = 565.0
                renta_mes_hab = st.number_input(f'Renta mes ({j+1})', value=value,min_value=0.0)
            with col4:
                subtotal = st.number_input(f'Subtotal ({j+1})', value=renta_mes_hab*num_hab,disabled=True)
            result_doorms.append({'tipo_hab':tipo_hab,'num_hab':num_hab,'renta_mes_hab':renta_mes_hab,'subtotal':subtotal})
        
        valor_total_recaudado = 0
        num_prod              = 0
        for j in result_doorms:
            if 'subtotal' in j:
                valor_total_recaudado += j['subtotal']
            if 'num_hab'  in j:
                num_prod += j['num_hab']
                
        col1,col2 = st.columns(2)  
        with col1:
            valor_renta_total = st.number_input('Renta TOTAL',value=valor_total_recaudado,disabled=True)
        with col2:
            valor_total_recaudado = st.number_input('Renta RECAUDADA',value=valor_total_recaudado*tasa_ocupacion,disabled=True)


    #-------------------------------------------------------------------------#
    # 3. Margen operativo
    st.write('---')
    st.write(' Margen Operativo')
    col1,col2,col3 = st.columns(3)
    with col1:
        margen_hab = st.number_input('Margen x hab',value=value_spread)
    with col2:
        spread_renttee = st.number_input('Spread Renttee',value=margen_hab*num_prod)
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
        iva_renta_mensual = st.number_input('IVA',value=iva_renta_mensual)
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
        fotmato = [
                    {"variable": "Electricidad", "value": 70, "IVA": IVA*100},
                    {"variable": "Gas", "value": 80, "IVA": IVA*100},
                    {"variable": "Agua", "value": 30, "IVA": 10},
                    {"variable": "Limpieza", "value": 50, "IVA": IVA*100},
                    {"variable": "CRM", "value": 15, "IVA": IVA*100},
                    {"variable": "Gestor", "value": 50, "IVA": IVA*100},
                    {"variable": "Portero/Responsable", "value": 0, "IVA": IVA*100},
                    {"variable": "Seguro", "value": 15, "IVA": 0},
                    {"variable": "Internet", "value": 30, "IVA": IVA*100}
                ]
        conteo = 0
        for j in fotmato:
            conteo += 1
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: 
                tipo_servicio = st.text_input('Tipo de servicio',key=f'tipo_servicio_({conteo+1})',value=j["variable"])
            with col2:
                valor_servicio  = st.number_input('Valor del servicio',key=f'valor_servicio_({conteo+1})',value=j['value'])
            with col3:
                iva_servicio  = st.number_input('IVA del servicio',key=f'iva_servicio_({conteo+1})',value=j['IVA'])
            with col4:
                base_servicio  = st.number_input('Base',key=f'base_servicio_({conteo+1})',value=valor_servicio/(1+(iva_servicio/100)))
            with col5:
                pagoiva_servicio  = st.number_input('IVA',key=f'pagoiva_servicio_({conteo+1})',value=valor_servicio-base_servicio)
            result_services.append({'tipo_servicio':tipo_servicio,'valor_servicio':valor_servicio,'iva_servicio':iva_servicio,'base_servicio':base_servicio,'pagoiva_servicio':pagoiva_servicio})
    
    valor_total_servicio = 0
    valor_base_servicio  = 0
    valor_IVA_servicio   = 0
    for j in result_services:
        if 'valor_servicio' in j:
            valor_total_servicio += j['valor_servicio']
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
    fotmato = [
                {"variable": "Mes en Curso", "value": monto_renta_mensual, "IVA": IVA*100},
                {"variable": "Depósito","value": 0.0, "IVA": 0},
                {"variable": "Fianza","value": 0.0, "IVA": 0},
                {"variable": "Agencia","value": 0.0, "IVA": IVA*100},
            ]
    conteo = 0
    for j in fotmato:
        conteo += 1
        isdisabled = False
        col1, col2, col3, col4, col5,col6 = st.columns(6)
        with col1: 
            tabla_contrato_tipo = st.text_input('Descripción',key=f'tabla_contrato_tipo_({conteo+1})',value=j["variable"])
        with col2:
            tabla_contrato_cantidad = st.selectbox('Cantidad',key=f'tabla_contrato_cantidad_({conteo+1})',options=[1,0])
            
        if tabla_contrato_cantidad==0: isdisabled = True
        
        with col3:
            tabla_contrato_monto  = st.number_input('Monto',key=f'tabla_contrato_monto_({conteo+1})',value=j['value']*tabla_contrato_cantidad,disabled=isdisabled)
        with col4:
            tabla_contrato_iva  = st.number_input('IVA',key=f'tabla_contrato_iva_({conteo+1})',value=j["IVA"],disabled=isdisabled)
        with col5:
            tabla_contrato_base  = st.number_input('Base',key=f'tabla_contrato_base_({conteo+1})',value=tabla_contrato_monto/(1+(tabla_contrato_iva/100)),disabled=isdisabled)
        with col6:
            tabla_contrato_pagoiva  = st.number_input('Pago IVA',key=f'tabla_contrato_pagoiva_({conteo+1})',value=tabla_contrato_monto-tabla_contrato_base,disabled=isdisabled)
        result_tabla_contrato.append({'tabla_contrato_tipo':tabla_contrato_tipo,'tabla_contrato_cantidad':tabla_contrato_cantidad,'tabla_contrato_monto':tabla_contrato_monto,'tabla_contrato_iva':tabla_contrato_iva,'tabla_contrato_base':tabla_contrato_base,'tabla_contrato_pagoiva':tabla_contrato_pagoiva})
        
    valor_total_tabla_contrato = 0
    valor_base_tabla_contrato  = 0
    valor_IVA_tabla_contrato   = 0
    for j in result_tabla_contrato:
        if 'tabla_contrato_monto' in j:
            valor_total_tabla_contrato += j['tabla_contrato_monto']
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

    facto_descuento = st.number_input('Factor de descuento', value=10.0,min_value=0.0,step=0.1)
    facto_descuento = facto_descuento/100
    
    col1,col2 = st.columns(2)
    with col1:
        ipc_alquiler_1 = st.number_input('Incre Alquileres (ano 1)', value=6.25,min_value=0.0,step=0.1)
    with col2:
        ipc_general_1 = st.number_input('IPC (ano 1)', value=3.25,min_value=0.0,step=0.1)
        
    col1,col2 = st.columns(2)
    with col1:
        ipc_alquiler_2 = st.number_input('Incre Alquileres (ano 2)', value=6.25,min_value=0.0,step=0.1)
    with col2:
        ipc_general_2 = st.number_input('IPC (ano 2)', value=3.25,min_value=0.0,step=0.1)

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
    result_tabla_renttee = []
    
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
    # 8. Metricas
    st.write('---')
    st.write('Metricas')
    result_tabla_metricas = []
    fotmato = [
        {'variable':'Base alquiler mes','disabled':True,'value':base_renta_mensual},
        {'variable':'Base alquiler anual','disabled':True,'value':base_renta_mensual*12},
        {'variable':'Alquiler mes IVA','disabled':True,'value':monto_renta_mensual},
        {'variable':'Alquiler anual IVA','disabled':True,'value':monto_renta_mensual*12},
        {'variable':'Precio Compra','disabled':True,'value':precio_compra},
        {'variable':'Yield','disabled':True,'value':valor_renta_total*12/precio_compra*100},
        {'variable':'Base Gestoria Mes','disabled':False,'value':150},
        {'variable':'Gestoria Mes (IVA)','disabled':True,'value':150},
        {'variable':'IBI','disabled':False,'value':0},
        {'variable':'Carry','disabled':False,'value':0},
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



