import streamlit as st
import boto3

@st.cache_data
def doc2nube(subfolder,file,filename):
    
    ACCESS_KEY  = st.secrets["ACCESS_KEY_cf"]
    SECRET_KEY  = st.secrets["SECRET_KEY_cf"]
    REGION      = st.secrets["REGION_cf"]
    BUCKET_NAME = 'operaciones'
    
    session = boto3.session.Session()
    client = session.client('s3', region_name=REGION, endpoint_url=f'https://{REGION}.digitaloceanspaces.com',
                            aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        fileimport = file.name
        dominio    = fileimport.split('.')[-1]
        filename   = f'{filename}.{dominio}'
        filename   = f'{subfolder}/{filename}'  # Nombre del archivo en el bucket
        file.seek(0) 
        client.upload_fileobj(file, BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read'})
        url = f'https://{BUCKET_NAME}.{REGION}.digitaloceanspaces.com/{filename}'
        st.success("¡Archivo subido exitosamente!")
    except: 
        url = None
        st.error("Hubo un error al subir el archivo")
    return url