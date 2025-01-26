import streamlit as st

# Função JavaScript para capturar coordenadas do navegador
geo_js = """
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById('latitude').value = latitude;
            document.getElementById('longitude').value = longitude;
            document.getElementById('submit-coords').click();
        }
    );
    </script>
"""

# Exibe o JavaScript na página
st.title("Captura de Coordenadas GPS")
st.markdown(geo_js, unsafe_allow_html=True)

# Campos escondidos para receber as coordenadas
lat = st.text_input("Latitude", "", key="latitude")
lon = st.text_input("Longitude", "", key="longitude")

# Botão para capturar coordenadas
if st.button("Capturar Coordenadas GPS"):
    if lat and lon:
        # Salvar coordenadas no arquivo txt
        with open("coordenadas.txt", "a") as file:
            file.write(f"Latitude: {lat}, Longitude: {lon}\n")
        st.success("Coordenadas salvas com sucesso!")
    else:
        st.warning("Coordenadas não capturadas. Por favor, tente novamente.")

# Botão escondido para enviar as coordenadas capturadas
st.button("submit", key="submit-coords", visible=False)
