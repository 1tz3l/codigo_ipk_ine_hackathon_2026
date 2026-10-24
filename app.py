import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Panel de control del slider 2009 - 2024
st.sidebar.header("Panel de control")
st.sidebar.info(
    "**ⓘ Información:** Utiliza el control deslizante para visualizar los resultados históricos."
)

election_year = [2009, 2012, 2015, 2018, 2021, 2024]

selected_year = st.sidebar.select_slider(
    "Año de elección:",
    options=election_year,
    value=2009,
)

st.sidebar.markdown("---")
st.sidebar.caption("Fuente: Conteos Censales de Participación Ciudadana (CCPC), INE")

df, geojson_data = load_data_for_year(selected_year)

# Título y subtítulo del dashboard
st.title("¿Cuántas mujeres votaron en tu estado?")
st.subheader(f"Año de elección: {selected_year}")

# Columnas
col1, col2 = st.columns([1.3, 0.7])

## Columna 1: Mapas
with col1:
    df_map = df[df["AELEC"] == selected_year]
    map_grouped = (
        df_map.groupby(["EDOCVE", "EDONOM"])[["SV", "NV"]]
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

    st.subheader("Participación por Estado (2009 - 2024)")

    df_heatmap = df[df["AELEC"].isin(election_year)]
    heatmap_grouped = (
        df_heatmap.groupby(["AELEC", "EDONOM"])[["SV", "NV"]]
        .sum()
        .reset_index()
    )
    heatmap_grouped["Participación"] = (
        heatmap_grouped["SV"] / (heatmap_grouped["SV"] + heatmap_grouped["NV"]) * 100
    )

    pivot_heat = heatmap_grouped.pivot(
        index="AELEC", columns="EDONOM", values="Participación"
    )

    fig_heat = px.imshow(
        pivot_heat,
        labels=dict(x="Estado", y="Año", color="Participación (%)"),
        x=pivot_heat.columns,
        y=pivot_heat.index.astype(str),
        color_continuous_scale="Blues",
        aspect="auto",
    )
    fig_heat.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0}, height=300)
    st.plotly_chart(fig_heat,use_container_width=True)

## Columna 2: Lista con los estados que más votaron
with col2:
    st.subheader(f"Top 15 Estados que más votaron en {selected_year}")

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
