import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import base64
import folium.plugins
import leafmap.foliumap as leafmap

st.set_page_config(page_title="Combate a Arbovirose")

with st.container():
    st.title("Mapeamento Aéreo by Eng Wagner Cunha ")
    st.subheader("Prefeitura Municipal de Arraial do Cabo - Arbovirose")
    st.write("Geolocalização de Piscinas, Caixas d'água e Hidromassagens descobertas")

with st.sidebar:
    st.sidebar.markdown("*Eng Wagner Cunha*")
    st.sidebar.write("🔵 Pontos a verificar")
    st.sidebar.write("🔴 Pontos suspeitos")
    st.sidebar.write("🟢 Pontos verificados")

with st.container():
    # Função para carregar dados do CSV
    def load_data(file_path):
        df = pd.read_csv(file_path)
        if 'status' not in df.columns:
            df['status'] = False
        return df

    file_path = 'pages/piscinas.csv'
    original_df = load_data(file_path)
    numero = len(original_df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write(f"{numero} pontos")
    with col3:
        st.write("PMAC")

    # Inicia o mapa centrado na coordenada fixa
    m = folium.Map(location=[-22.973356, -42.025602], zoom_start=16)

    # Adicionando o plugin LocateControl para mostrar a localização atual
    folium.plugins.LocateControl(keepCurrentZoomLevel=True, drawMarker=True).add_to(m)

    # Adicionando camadas de mapa
    folium.TileLayer('OpenStreetMap').add_to(m)
    esri_satellite_url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    folium.TileLayer(tiles=esri_satellite_url, attr='Esri', name='Esri Satellite', overlay=False, control=True).add_to(m)
    folium.LayerControl().add_to(m)

    # Adiciona marcadores para todos os pontos com condições de cores específicas
    for idx, row in original_df.iterrows():
        if row['status']:
            icon_color = 'green'
        else:
            icon_color = 'red' if row['Suspeito'] == 1 else 'blue'
        
        image_path = f"imagens/{row['id_campo']}.jpg"
        
        try:
            encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode()
            image_html = f"<img src='data:image/jpeg;base64,{encoded_image}' width='200' height='200'><br>ID: {row['id_campo']}"
            iframe = folium.IFrame(image_html, width=220, height=220)
            popup = folium.Popup(iframe, max_width=2650)
        except FileNotFoundError:
            popup = folium.Popup(f"ID: {row['id_campo']} - Status: {'Verificado' if row['status'] else 'Não Verificado'} - Suspeito: {'Sim' if row['Suspeito'] == 1 else 'Não'}", max_width=2650)
        
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=popup,
            tooltip=f"ID: {row['id_campo']}",
            icon=folium.Icon(color=icon_color)
        ).add_to(m)

    folium_static(m)
