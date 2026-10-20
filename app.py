import json
import pandas as pd
import plotly.express as px
import streamlit as st

# Configurar el ancho del layout para los mapas
st.set_page_config(
    page_title="¿Las mujeres votan?", layout="wide"
)

@st.cache_data
def load_data():
    # Carga solo las columnas necesarias para filtros y cálculos
    columns_needed = [
        "AELEC",
        "EDOCVE",
        "EDONOM",
        "EDAD",
        "SEXO",
        "SV",
        "NV",
    ]
    df = pd.read_parquet("steps/process_geo_data_2/voting_data.parquet", columns=columns_needed)
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

# Funcion para calcular el porcentaje de participación por edad y año
ipython_link = None # marcador (placeholder) para la lógica

def get_participation_rate_df(data, year, min_age, max_age):
    filtered = data[
        (data["AELEC"] == year)
        & (data["EDAD"] >= min_age)
        & (data["EDAD"] <= max_age)
    ]

    # Agrupado por EDOCVE; suma de SV y NV
    grouped = (
        filtered.groupby(["EDOCVE", "EDONOM"])[["SV", "NV"]].sum().reset_index()
    )

    # Se calcula el porcentaje de participación
    grouped["participacion"] = (
        grouped["SV"] / (grouped["SV"] + grouped["NV"])
    ) * 100

    # Se asegura que EDOCVE coincida con el formato de GeoJSON (int o str)
    grouped["EDOCVE"] = grouped["EDOCVE"].astype(int)
    return grouped

# Se obtienen los datos para el mapa izquierdo (Edades: 18 - 45)
df_younger_gen = get_participation_rate_df(df, selected_year, 18, 45)

# Se obtienen los datos para el mapa derecho (Edades: 46 - 140)
df_older_gen = get_participation_rate_df(df, selected_year, 46, 140)

# Renderizar mapas
st.title("Participación electoral por rangos de edad")
st.markdown(f"**Año seleccionado:** {selected_year}")

# Se crean 2 columnas para los mapas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Jóvenes (18 - 45 años)")
    fig1 = px.choropleth_map(
        df_younger_gen,
        geojson=geojson_data,
        locations="EDOCVE",
        featureidkey="properties.matched_edocve",
        color="participacion",
        color_continuous_scale="Reds",
        range_color=[0, 100],
        map_style="carto-positron",
        center={"lat": 23.6345, "lon": -102.5528}, 
        zoom=4.0,
    )
    fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=450)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Adultas (46 - 140 años)")
    fig2 = px.choropleth_map(
        df_older_gen,
        geojson=geojson_data,
        locations="EDOCVE",
        featureidkey="properties.matched_edocve",
        color="participacion",
        color_continuous_scale="Blues",
        range_color=[0, 100],
        map_style="carto-positron",
        center={"lat": 23.6345, "lon": -102.5528}, 
        zoom=4.0,
    )
    fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=450)
    st.plotly_chart(fig2, use_container_width=True)

# Otras métricas
st.divider()

if selected_state_key is not None:
    st.subheader(f"Desglose detallado: {selected_state_name} ({selected_year})")

    # Filtro por estado y año seleccionados
    state_data = df[(df["AELEC"] == selected_year) & (df["EDOCVE"] == selected_state_key)]

    # Grupo por género
    gender_group = state_data.groupby("SEXO")[["SV", "NV"]].sum().reset_index()
    gender_group["participacion"] = (gender_group["SV"] / (gender_group["SV"] + gender_group["NV"])) * 100

    # Muestra las métricas
    grp_col1, grp_col2 = st.columns(2)
    # 0 = Hombre, 1 = Mujer, 2 = No binario
    with grp_col1:
        st.metric("Participación general por estado", f"{state_data["SV"].sum() / (state_data["NV"].sum()) * 100:.1f}%")
    with grp_col2:
        st.metric("Sí votaron", f"{state_data["SV"].sum():,}")
else:
    st.info("💡 Selecciona un estado en la barra lateral para ver el desglose detallado por género.")
