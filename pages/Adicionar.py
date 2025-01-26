import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from folium.plugins import LocateControl, Draw
from datetime import datetime
import os

# Função para carregar dados do CSV
def load_data(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=['id_campo', 'data', 'obs', 'LON', 'LAT'])
    return df

# Função para adicionar uma nova linha ao DataFrame e salvar no CSV
def add_to_csv(file_path, lon, lat, obs):
    df = load_data(file_path)
    id_campo = int(df['id_campo'].max()) + 1 if not df.empty else 1
    data_atual = datetime.now().strftime("%Y-%m-%d")
    new_data = pd.DataFrame([[id_campo, data_atual, obs, lon, lat]], columns=['id_campo', 'data', 'obs', 'LON', 'LAT'])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_path, index=False)
    return df

st.subheader("Visitas")
file_path = 'pages/visita.csv'

# Inicializando os campos de entrada com session_state para limpeza
if 'coords_input' not in st.session_state:
    st.session_state['coords_input'] = ""
if 'obs' not in st.session_state:
    st.session_state['obs'] = ""

coords_input = st.text_input("Coordenadas (formato LON,LAT):", value=st.session_state.coords_input)
obs = st.text_area("Observações:", value=st.session_state.obs)

# Botão para adicionar as coordenadas ao CSV e limpeza dos campos
if st.button("Adicionar Visita"):
    try:
        lon, lat = [float(coord.strip()) for coord in coords_input.split(',')]

        # Convertendo latitude e longitude para string para checar o início
        lon_str, lat_str = str(lon), str(lat)

        # Validação simplificada das coordenadas
        if not lon_str.startswith('-42') or not lat_str.startswith('-22'):
            st.error("As coordenadas não correspondem à região especificada. Longitude deve começar com -42 e Latitude com -22.")
        else:
            add_to_csv(file_path, lon, lat, obs)
            st.success("Visita adicionada com sucesso!")

    except ValueError:
        st.error("Formato de coordenadas inválido. Use o formato LON,LAT.")

# Carregando dados e exibindo o mapa
df = load_data(file_path)
m = folium.Map(location=[-22.973356, -42.025602], zoom_start=16, tiles='OpenStreetMap')
# Adicionando Esri Satellite com URL específica
esri_satellite_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
folium.TileLayer(
    tiles=esri_satellite_url,
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True,
).add_to(m)

LocateControl().add_to(m)
Draw().add_to(m)

for idx, row in df.iterrows():
    folium.Marker(location=[row['LAT'], row['LON']],
                  popup=f"ID: {row['id_campo']}\nData: {row['data']}\nObs: {row['obs']}",
                  icon=folium.Icon(color='green')).add_to(m)


folium_static(m)
