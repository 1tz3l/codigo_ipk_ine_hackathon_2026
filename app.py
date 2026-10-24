import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configurar el ancho del layout para los mapas
st.set_page_config(
    page_title="Participación electoral de las mujeres en México", layout="wide"
)

elections_by_year = [2009, 2012, 2015, 2018, 2021, 2024]

STATE_NAME_MAPPING = {
    "AGUASCALIENTES": "Aguascalientes",
    "BAJA CALIFORNIA": "Baja California",
    "BAJA CALIFORNIA SUR": "Baja California Sur",
    "CAMPECHE": "Campeche",
    "COAHUILA": "Coahuila",
    "COLIMA": "Colima",
    "CHIAPAS": "Chiapas",
    "CHIHUAHUA": "Chihuahua",
    "DISTRITO FEDERAL": "Ciudad de México",
    "CIUDAD DE MEXICO": "Ciudad de México",
    "CIUDAD DE MÉXICO": "Ciudad de México",
    "DURANGO": "Durango",
    "GUANAJUATO": "Guanajuato",
    "GUERRERO": "Guerrero",
    "HIDALGO": "Hidalgo",
    "JALISCO": "Jalisco",
    "MEXICO": "Estado de México",
    "MÉXICO": "Estado de México",
    "MICHOACAN": "Michoacán",
    "MORELOS": "Morelos",
    "NAYARIT": "Nayarit",
    "NUEVO LEON": "Nuevo León",
    "OAXACA": "Oaxaca",
    "PUEBLA": "Puebla",
    "QUERETARO": "Querétaro",
    "QUINTANA ROO": "Quintana Roo",
    "SAN LUIS POTOSI": "San Luis Potosí",
    "SINALOA": "Sinaloa",
    "SONORA": "Sonora",
    "TABASCO": "Tabasco",
    "TAMAULIPAS": "Tamaulipas",
    "TLAXCALA": "Tlaxcala",
    "VERACRUZ": "Veracruz",
    "YUCATAN": "Yucatán",
    "ZACATECAS": "Zacatecas",
}

@st.cache_data
def load_heatmap_data():
    df_all =  pd.read_parquet(
        "steps/process_geo_data_2/voting_data.parquet",
        columns=["AELEC", "EDONOM", "SV", "NV"],
        filters=[("AELEC", "in", elections_by_year)],
    )

    df_all["EDONOM"] = df_all["EDONOM"].replace(STATE_NAME_MAPPING)

    grouped = (
        df_all.groupby(["AELEC", "EDONOM"])[["SV", "NV"]]
        .sum()
        .reset_index()
    )
    grouped["Participación"] = (
        grouped["SV"] / (grouped["SV"] + grouped["NV"]) * 100
    )
    return grouped

@st.cache_data
def load_data_for_year(selected_year):
    df_year = pd.read_parquet(
        "steps/process_geo_data_2/voting_data.parquet",
        columns=["AELEC", "EDOCVE", "EDONOM", "SEXO", "EDAD", "SV", "NV"],
        filters=[("AELEC", "==", selected_year)],
    )

    df_year["EDONOM"] = df_year["EDONOM"].replace(STATE_NAME_MAPPING)

    return df_year

@st.cache_data
def load_geojson():
    with open("steps/process_geo_data_2/matched_geo_data.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

geojson_data = load_geojson()
df_heatmap_static = load_heatmap_data()

# Panel de control del slider 2009 - 2024
st.sidebar.header("Panel de control")
st.sidebar.info(
    "**ⓘ Información:** Utiliza el control deslizante para visualizar los resultados históricos."
)

selected_year = st.sidebar.select_slider(
    "Año de elección:",
    options=elections_by_year,
    value=2009,
)

st.sidebar.markdown("---")
st.sidebar.caption("Fuente: Conteos Censales de Participación Ciudadana (CCPC), INE")

df_selected_year = load_data_for_year(selected_year)

# Título y subtítulo del dashboard
st.title("¿Cuántas mujeres votaron en tu estado?")
st.subheader(f"Año de elección: {selected_year}")

# Columnas
col1, col2 = st.columns([1.3, 0.7])

## Columna 1: Mapas
with col1:
    map_grouped = (
        df_selected_year.groupby(["EDOCVE", "EDONOM"])[["SV", "NV"]]
        .sum()
        .reset_index()
    )
    map_grouped["Participación"] = (
        map_grouped["SV"] / (map_grouped["SV"] + map_grouped["NV"]) * 100
    )
    map_grouped["EDOCVE"] = map_grouped["EDOCVE"].astype(int)

    fig_map = px.choropleth_map(
        map_grouped,
        geojson=geojson_data,
        locations="EDOCVE",
        featureidkey="properties.matched_edocve",
        color="Participación",
        color_continuous_scale="Blues",
        range_color=[0, 100],
        map_style="carto-positron",
        center={"lat": 23.6345, "lon": -102.5528}, 
        zoom=4.2,
    )
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=400)
    st.plotly_chart(fig_map, use_container_width=True)

    st.divider()

    st.subheader("Histórico de la participación electoral por Estado")

    pivot_heat = df_heatmap_static.pivot(
        index="AELEC", columns="EDONOM", values="Participación"
    )

    years_order = [2024, 2021, 2018, 2015, 2012, 2009]
    pivot_heat = pivot_heat.reindex(years_order)

    years_str = [str(y) for y in pivot_heat.index]

    fig_heat = px.imshow(
        pivot_heat,
        labels=dict(x="Estado", y="Año", color="Participación (%)"),
        x=list(pivot_heat.columns),
        y=years_str,
        color_continuous_scale="Blues",
        aspect="auto",
    )
    fig_heat.update_yaxes(
        type="category",
        tickmode="array",
        tickvals=years_str,
        ticktext=years_str,
        categoryorder="array",
        categoryarray=years_str,
    )
    fig_heat.update_layout(margin={"r": 0, "t": 20, "l": 0, "b": 0}, height=320)
    st.plotly_chart(fig_heat,use_container_width=True)

## Columna 2: Lista con los estados que más votaron
with col2:
    st.subheader(f"Estados que más votaron en {selected_year}")

    top_15_list = (
        map_grouped.sort_values(by="SV", ascending=False).head(15).reset_index(drop=True)
    )

    fig_list = px.bar(
        top_15_list,
        x="SV",
        y="EDONOM",
        orientation="h",
        text="SV",
        color="SV",
        color_continuous_scale="Reds",
    )
    fig_list.update_layout(
        xaxis_title="Total de votos emitidos",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
        margin={"r": 0, "t": 10, "l": 0, "b": 0}, 
        height=650,
        showlegend=False,
        coloraxis_showscale=False,
    )
    fig_list.update_traces(texttemplate="%{text:,}", textposition="outside")
    st.plotly_chart(fig_list, use_container_width=True)
