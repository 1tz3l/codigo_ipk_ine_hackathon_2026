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