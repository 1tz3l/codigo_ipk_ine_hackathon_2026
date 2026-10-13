import json
import pandas as pd
import plotly.express as px
import streamlit as st

# Configurar el ancho del layout para los mapas
st.set_page_config(
    page_title="La participación electoral entre diferentes grupos de edad", layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_parquet("steps/process_geo_data_2/voting_data.parquet")
    with open("steps/process_geo_data_2/matched_geo_data.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
    return df, geojson

df, geojson_data = load_data()

st.sidebar.title("Línea del tiempo")
# Time playback slider 2009 - 2024
selected_year = st.sidebar.slider(
    "Año de elección:",
    min_value=2009,
    max_value=2024,
    step=1,
    value=2009,
)

# Seleccionar estado
state_options = {"Todos los estados": None}
state_mapping_dict = (
    df[["EDONOM", "EDOCVE"]].drop_duplicates().set_index("EDONOM")["EDOCVE"].to_dict()
)
state_options.update(state_mapping_dict)

selected_state_name = st.sidebar.selectbox(
    "Estado:", options=list(state_options.keys())
)
selected_state_key = state_options[selected_state_name]
