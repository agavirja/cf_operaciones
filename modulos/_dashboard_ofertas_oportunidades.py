import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import folium
import pymysql
import streamlit.components.v1 as components
from sqlalchemy import create_engine
from folium.plugins import Draw
from streamlit_folium import st_folium
from shapely.geometry import Point,Polygon,mapping,shape
from datetime import datetime

from scripts.dataproyectos import datacalculadora as getdatacalculadora
from scripts.getdatamarket import datamarket

from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from st_aggrid.shared import JsCode

user     = st.secrets["user_cf_pdfcf"]
password = st.secrets["password_cf_pdfcf"]
host     = st.secrets["host_cf_pdfcf"]
schema   = st.secrets["schema_cf_pdfcf"]

def main(codigo):

    formato = {
               'show':False,
               'polygonfilter':None,
               'latitud':40.407027,
               'longitud':-3.690974,
               'zoom_start':12,
               
               }

    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
            
    datasavedlist   = getsavedlist(codigo)
    datacalculadora = getdatacalculadora(codigo)

    if not datacalculadora.empty:
        try:
            datacalculadora = pd.DataFrame([json.loads(datacalculadora['json'].iloc[0])])
            try: datacalculadora["habitaciones"] = datacalculadora["habitaciones"].apply(lambda x: json.loads(x))
            except: pass
        except: pass

    inputvar = {}
    if not datacalculadora.empty:
        if 'preciocompra' in datacalculadora and datacalculadora['preciocompra'].iloc[0]>0: 
            inputvar['preciocompra'] = datacalculadora['preciocompra'].iloc[0]
        if 'superficiereal' in datacalculadora and datacalculadora['superficiereal'].iloc[0]>0:
            inputvar['superficiereal'] = datacalculadora['superficiereal'].iloc[0]
       
    col1, col2 = st.columns(2)
    with col1:
        value        = inputvar['preciocompra'] if 'preciocompra' in inputvar and inputvar['preciocompra']>0 else 0
        preciocompra = st.number_input('Precio de compra',value=value,min_value=0)
        inputvar['preciocompra'] = preciocompra
    with col2:
        value          = inputvar['superficiereal'] if 'superficiereal' in inputvar and inputvar['superficiereal']>0 else 0
        superficiereal = st.number_input('Superficie',value=value,min_value=0)
        inputvar['superficiereal'] = superficiereal
        
    col1, col2 = st.columns([3,1])
    with col2:
        if st.button('Buscar'):
            st.session_state.show = True
        
    #-------------------------------------------------------------------------#
    # Tabla de oportundiades
    #-------------------------------------------------------------------------#
    if not datasavedlist.empty:
        st.write('Oportunidades guardadas')
        variables = [x for x in ['id_inmueble','barrio','precio','area','habitaciones','banos','numero_piso','garaje','url_activo'] if x in datasavedlist]
        df = datasavedlist.copy()
        df = df[variables]
        df.rename(columns={'url_activo':'link'},inplace=True)
        
        gb = GridOptionsBuilder.from_dataframe(df,editable=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        cell_renderer =  JsCode("""function(params) {return `<a href=${params.value} target="_blank">${params.value}</a>`}""")
        
        gb.configure_column(
            "link",
            headerName="link",
            width=100,
            cellRenderer=JsCode("""
                class UrlCellRenderer {
                  init(params) {
                    this.eGui = document.createElement('a');
                    this.eGui.innerText = 'Link';
                    this.eGui.setAttribute('href', params.value);
                    this.eGui.setAttribute('style', "text-decoration:none");
                    this.eGui.setAttribute('target', "_blank");
                  }
                  getGui() {
                    return this.eGui;
                  }
                }
            """)
        )
        
        response = AgGrid(df,
                    gridOptions=gb.build(),
                    columns_auto_size_mode="FIT_CONTENTS",
                    theme=AgGridTheme.STREAMLIT,
                    updateMode=GridUpdateMode.VALUE_CHANGED,
                    allow_unsafe_jscode=True)
        
        if response['selected_rows']:  
            df = pd.DataFrame(response['selected_rows'])
            df = df[['id_inmueble']]
            df['codigo_proyecto'] = codigo
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Eliminar',key='guardar_oportunidades'):
                    with st.spinner('Guardando'):
                        updatetable(df)
                        st.session_state.show = False
                        st.session_state.polygonfilter = None
                        st.cache_data.clear()
                        st.rerun()
        
    #-------------------------------------------------------------------------#
    # Mapa
    #-------------------------------------------------------------------------#
    if st.session_state.show:
        dataoportundiades =  getdataoportunidades(inputvar,polygon=str(st.session_state.polygonfilter))

        #---------------------------------------------------------------------#
        # Mapa de transacciones en el radio
        m = folium.Map(location=[st.session_state.latitud, st.session_state.longitud], zoom_start=st.session_state.zoom_start,tiles="cartodbpositron")
        draw = Draw(
                    draw_options={"polyline": False,"marker": False,"circlemarker":False,"rectangle":False,"circle":False},
                    edit_options={"poly": {"allowIntersection": False}}
                    )
        draw.add_to(m)

        if st.session_state.polygonfilter is not None:
            geojson_data                = mapping(st.session_state.polygonfilter)
            polygon_shape               = shape(geojson_data)
            centroid                    = polygon_shape.centroid
            st.session_state.latitud    = centroid.y
            st.session_state.longitud   = centroid.x
            st.session_state.zoom_start = 14
            folium.GeoJson(geojson_data, style_function=style_function).add_to(m)
            
        geopoints = point2geopandas(dataoportundiades)
        popup     = folium.GeoJsonPopup(
            fields=["popup"],
            aliases=[""],
            localize=True,
            labels=True,
        )
        folium.GeoJson(geopoints,popup=popup).add_to(m)

        st_map = st_folium(m,width=1600,height=600)
        
        polygonType = ''
        if 'all_drawings' in st_map and st_map['all_drawings'] is not None:
            if st_map['all_drawings']!=[]:
                if 'geometry' in st_map['all_drawings'][0] and 'type' in st_map['all_drawings'][0]['geometry']:
                    polygonType = st_map['all_drawings'][0]['geometry']['type']
            
        if 'polygon' in polygonType.lower():
            coordenadas   = st_map['all_drawings'][0]['geometry']['coordinates']
            st.session_state.polygonfilter = Polygon(coordenadas[0])
            st.rerun()
            
    if st.session_state.show:
        col1, col2 = st.columns([3,1])
        with col2:
            if st.button('resetear busqueda'):
                st.session_state.polygonfilter = None
                st.session_state.zoom_start = 12
                st.session_state.show = False
                st.rerun()
                
        #---------------------------------------------------------------------#
        # Guardad oportundiades
        #---------------------------------------------------------------------#
        variables = [x for x in ['id_inmueble','barrio','precio','area','habitaciones','banos','numero_piso','garaje','url_activo'] if x in dataoportundiades]
        df = dataoportundiades.copy()
        df = df[variables]
        df.rename(columns={'url_activo':'link'},inplace=True)
        
        gb = GridOptionsBuilder.from_dataframe(df,editable=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        cell_renderer =  JsCode("""function(params) {return `<a href=${params.value} target="_blank">${params.value}</a>`}""")
        
        gb.configure_column(
            "link",
            headerName="link",
            width=100,
            cellRenderer=JsCode("""
                class UrlCellRenderer {
                  init(params) {
                    this.eGui = document.createElement('a');
                    this.eGui.innerText = 'Link';
                    this.eGui.setAttribute('href', params.value);
                    this.eGui.setAttribute('style', "text-decoration:none");
                    this.eGui.setAttribute('target', "_blank");
                  }
                  getGui() {
                    return this.eGui;
                  }
                }
            """)
        )
        
        response = AgGrid(df,
                    gridOptions=gb.build(),
                    height=400,
                    columns_auto_size_mode="FIT_CONTENTS",
                    theme=AgGridTheme.STREAMLIT,
                    updateMode=GridUpdateMode.VALUE_CHANGED,
                    allow_unsafe_jscode=True)

        if response['selected_rows']:  
            df = pd.DataFrame(response['selected_rows'])
            if '_selectedRowNodeInfo' in df: del df['_selectedRowNodeInfo']
            idd = dataoportundiades['id_inmueble'].isin(df['id_inmueble'])
            data2export = dataoportundiades[idd]
            data2export['codigo_proyecto'] = codigo
            data2export['created_at'] = datetime.now().strftime('%Y-%m-%d')
            data2export['updated_at'] = datetime.now().strftime('%Y-%m-%d')
            data2export['activo'] = 1
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Guardar',key='guardar_oportunidades'):
                    with st.spinner('Guardando'):
                        engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}') 
                        data2export.to_sql('cj_lista_oportunidades', engine, if_exists='append', index=False, chunksize=1)
                        st.success('Oportundiades guardadas exitosamente')
                        engine.dispose()
                        st.session_state.show = False
                        st.session_state.polygonfilter = None
                        st.cache_data.clear()
                        st.rerun()
            
    components.html(
        """
    <script>
    const elements = window.parent.document.querySelectorAll('.stButton button')
    elements[0].style.backgroundColor = '#B98C65';
    elements[0].style.fontWeight = 'bold';
    elements[0].style.color = 'white';
    elements[0].style.width = '100%';
    
    elements[1].style.backgroundColor = '#B98C65';
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
    </script>
    """
    )

@st.cache_data
def getdataoportunidades(inputvar,polygon=None):

    if isinstance(polygon, str) and polygon!='' and not 'none' in polygon.lower():
        dataoportundiades = datamarket(inputvar,polygon=polygon)
    else:
        dataoportundiades = datamarket(inputvar,polygon=None)

    dataoportundiades = dataoportundiades.iloc[0:100,:]
    return dataoportundiades
   
@st.cache_data
def getsavedlist(codigo):
    data = pd.DataFrame()
    if codigo is not None:
        engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')
        data   = pd.read_sql_query(f"SELECT * FROM {schema}.cj_lista_oportunidades WHERE codigo_proyecto = '{codigo}' AND activo=1" , engine)
        engine.dispose()
        return data
     
@st.cache_data
def point2geopandas(data):
    
    geojson = pd.DataFrame().to_json()
    if 'latitud' in data and 'longitud' in data:
        data = data[(data['latitud'].notnull()) & (data['longitud'].notnull())]
    if not data.empty:
        data['geometry'] = data.apply(lambda x: Point(x['longitud'],x['latitud']),axis=1)
        data             = gpd.GeoDataFrame(data, geometry='geometry')
        
        data['popup'] = None
        data.index    = range(len(data))
        img_style = '''
        <style>               
            .property-image{
              flex: 1;
            }
            img{
                width:200px;
                height:120px;
                object-fit: cover;
                margin-bottom: 2px; 
            }
        </style>
                '''
        for idd,items in data.iterrows():
            try:    precio = f"<b> Precio:</b> {items['precio']}<br>"
            except: precio = "<b> Empresa:</b> Sin información <br>" 
            try:    area = f"<b> Área:</b> {items['area']}<br>"
            except: area = "<b> Área:</b> Sin información <br>" 
            
            try:    habitaciones = f"<b> Habitaciones:</b> {int(items['habitaciones'])}<br>"
            except: habitaciones = "<b> Habitaciones:</b> Sin información <br>" 
            try:    banos = f"<b> Baños:</b> {int(items['banos'])}<br>"
            except: banos = "<b> Baños:</b> Sin información <br>"     
            try:    garajes = f"<b> Garajes:</b> {int(items['garaje'])}<br>"
            except: garajes = "<b> Garajes:</b> Sin información <br>"                 
            try:    ascensor = f"<b> Ascensor:</b> {items['ascensor']}<br>"
            except: ascensor = "<b> Ascensor:</b> Sin información <br>"  
            try:    barrio = f"<b> Barrio:</b> {items['barrio']}<br>"
            except: barrio = "<b> Barrio:</b> Sin información <br>" 
            try:    numeropiso = f"<b> Planta:</b> {items['numero_piso']}<br>"
            except: numeropiso = "<b> Planta:</b> Sin información <br>"
            try:    url = f"""<b> url:</b> <a href="{items['url_activo']}" target="_blank" style="color: black;">{items['url_activo']}</a>"""
            except: url = "<b> url:</b> Sin información <br>"    
            popup_content =  f'''
            <!DOCTYPE html>
            <head>
              {img_style}
            </head>
            <html>
                <body>
                    <div id="popupContent" style="cursor:pointer; display: flex; flex-direction: column; flex: 1;width:200px;">
                        <a href="http://localhost:8501/Dashboard_ofertas?idinmueble={items['id_inmueble']}" target="_blank" style="color: black;">
                            <div class="property-image">
                                <img src="{items['url_img1']}"  alt="property image" onerror="this.src='https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/sin_imagen.png';">
                            </div>
                            {barrio}
                            {precio}
                            {area}
                            {habitaciones}
                            {banos}
                            {garajes}
                            {numeropiso}
                            {ascensor}
                        </a>
                    </div>
                    {url}
                </body>
            </html>
            '''
            data.loc[idd,'popup'] = popup_content
        data    = data[['popup','geometry']]
        geojson = data.to_json()
    return geojson

def updatetable(datachange):
    conn = pymysql.connect(host=host,
                   user=user,
                   password=password,
                   db=schema)
    with conn.cursor() as cursor:
        sql = "UPDATE pdfcf.cj_lista_oportunidades SET activo=0  WHERE id_inmueble=%s AND codigo_proyecto=%s "
        list_of_tuples = datachange.to_records(index=False).tolist()
        cursor.executemany(sql, list_of_tuples)
    conn.commit()
    conn.close() 
    
def style_function(feature):
    return {
        'fillColor': '#ffaf00',
        'color': 'blue',
        'weight': 0, 
    }    