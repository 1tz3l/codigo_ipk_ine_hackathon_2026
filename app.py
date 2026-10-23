import json
import pandas as pd
import plotly.express as px
import streamlit as st

# Configurar el ancho del layout para los mapas
st.set_page_config(
    page_title="Participación electoral de las mujeres en México", layout="wide"
)

@st.cache_data
#def load_data():
    # Carga solo las columnas necesarias para filtros y cálculos
    #columns_needed = [
        #"AELEC",
        #"EDOCVE",
        #"EDONOM",
        #"EDAD",
        #"SEXO",
        #"SV",
        #"NV",
    #]
    #df = pd.read_parquet("steps/process_geo_data_2/voting_data.parquet", columns=columns_needed)
    #with open("steps/process_geo_data_2/matched_geo_data.geojson", "r", encoding="utf-8") as f:
        #geojson = json.load(f)
    #return df, geojson

#df, geojson_data = load_data()

def load_data_for_year(selected_year):
    df_year = pd.read_parquet(
        "steps/process_geo_data_2/voting_data.parquet",
        columns=["AELEC", "EDOCVE", "EDONOM", "SEXO", "EDAD", "SV", "NV"],
        filters=[("AELEC", "==", selected_year)],
    )
    with open("steps/process_geo_data_2/matched_geo_data.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
    return df_year, geojson

st.sidebar.header("Panel de control")
st.sidebar.info(
    "**ⓘ Información:** Utiliza el control deslizante para visualizar los resultados históricos."
)
# Time playback slider 2009 - 2024
selected_year = st.sidebar.slider(
    "Año de elección:",
    min_value=2009,
    max_value=2024,
    step=3,
    value=2009,
)
st.sidebar.markdown("---")
st.sidebar.caption("Fuente: Conteos Censales de Participación Ciudadana (CCPC), INE")

df, geojson_data = load_data_for_year(selected_year)

# Funcion para calcular el porcentaje de participación por edad y año
ipython_link = None # marcador (placeholder) para la lógica

def get_participation_rate_df(data, year, min_age, max_age):
    filtered = data[
        (data["AELEC"] == year)
        & (data["EDAD"] >= min_age)
        & (data["EDAD"] <= max_age)
    ]

    ## Agrupado por EDOCVE; suma de SV y NV
    grouped = (
        filtered.groupby(["EDOCVE", "EDONOM"])[["SV", "NV"]].sum().reset_index()
    )

    ## Se calcula el porcentaje de participación
    grouped["Participación"] = (
        grouped["SV"] / (grouped["SV"] + grouped["NV"])
    ) * 100

    ## Se asegura que EDOCVE coincida con el formato de GeoJSON (int o str)
    grouped["EDOCVE"] = grouped["EDOCVE"].astype(int)
    return grouped

# Se obtienen los datos para el mapa izquierdo (Edades: 18 - 45)
df_younger_gen = get_participation_rate_df(df, selected_year, 18, 45)

# Se obtienen los datos para el mapa derecho (Edades: 46 - 140)
df_older_gen = get_participation_rate_df(df, selected_year, 46, 140)

# Renderizar mapas
st.title("¿Cuántas mujeres votaron en tu estado?")
st.subheader(f"Año de elección: {selected_year}")

# Se crean 2 columnas para los mapas
col1, col2 = st.columns(2)

with col1:
    fig1 = px.choropleth_map(
        df_younger_gen,
        geojson=geojson_data,
        locations="EDOCVE",
        featureidkey="properties.matched_edocve",
        color="Participación",
        color_continuous_scale="Blues",
        range_color=[0, 100],
        map_style="carto-positron",
        center={"lat": 23.6345, "lon": -102.5528}, 
        zoom=4.0,
    )
    fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=450)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("46 - 140 años")
    fig2 = px.choropleth_map(
        df_older_gen,
        geojson=geojson_data,
        locations="EDOCVE",
        featureidkey="properties.matched_edocve",
        color="Participación",
        color_continuous_scale="Reds",
        range_color=[0, 100],
        map_style="carto-positron",
        center={"lat": 23.6345, "lon": -102.5528}, 
        zoom=4.0,
    )
    fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=450)
    st.plotly_chart(fig2, use_container_width=True)
