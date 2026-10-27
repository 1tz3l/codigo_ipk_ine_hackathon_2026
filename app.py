import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from constants import (
    STATE_NAME_MAPPING,
    SECTION_TYPE_MAPPING,
    CUSTOM_MAP_SCALE, 
    CUSTOM_HEATMAP_SCALE, 
    CUSTOM_BAR_SCALE
)

# Configurar el ancho del layout para los mapas
st.set_page_config(
    page_title="Participación electoral de las mujeres en México", layout="wide"
)

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

elections_by_year = [2009, 2012, 2015, 2018, 2021, 2024]

@st.cache_data
def load_heatmap_data():
    df_all =  pd.read_parquet(
        "steps/process_geo_data_2/voting_data_summary.parquet",
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
    ).round(1)
    return grouped

@st.cache_data
def load_data_for_year(selected_year):
    df_year = pd.read_parquet(
        "steps/process_geo_data_2/voting_data_summary.parquet",
        columns=["AELEC", "EDOCVE", "EDONOM", "TIPOSEC", "SEXO", "SV", "NV"],
        filters=[("AELEC", "==", selected_year)],
    )

    df_year["TIPOSEC"] = df_year["TIPOSEC"].astype(str).str.strip().str.upper()

    df_year["EDONOM"] = df_year["EDONOM"].replace(STATE_NAME_MAPPING)

    return df_year

@st.cache_data
def load_geojson():
    with open("steps/process_geo_data_2/matched_geo_data.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

geojson_data = load_geojson()
df_heatmap_static = load_heatmap_data()

# Panel de control del slider 2009 - 2024
st.sidebar.header(
    "**Panel de control**",
    help=("Utilice los filtros para visualizar los resultados históricos por año y por sección."),
)

selected_year = st.sidebar.select_slider(
    "Año de elección:",
    options=elections_by_year,
    help=("Arrastre el punto para visualizar los resultados históricos por año de elección."),
    value=2009,
)

selected_section_type_labels = st.sidebar.multiselect(
    "Tipo de sección:",
    options=list(SECTION_TYPE_MAPPING.keys()),
    default=[],
    help=("Se mostrarán por defecto todas las secciones. Seleccione una sección o dos secciones en específico para filtrar." 
    ),
)

if selected_section_type_labels:
    selected_section_type_codes = [
        SECTION_TYPE_MAPPING[label] for label in selected_section_type_labels
    ]
else:
    selected_section_type_codes = ["U", "M", "R"]

st.sidebar.image(
    "assets/ine_200px.png", 
    width="content", #For `use_container_width=True`, use `width='stretch'`. 
    #For `use_container_width=False`, use `width='content'`.
)

df_selected_year = load_data_for_year(selected_year)

# Título y subtítulo del dashboard
st.title("La participación electoral de las mujeres en México")
st.markdown("---")
st.subheader(f"Distribución territorial del voto femenino en {selected_year}")

# Columnas
col1, col2 = st.columns([1.3, 0.7])

## Columna 1: Mapas
with col1:
    df_filtered_sections = df_selected_year[
        df_selected_year["TIPOSEC"].isin(selected_section_type_codes)
    ]

    map_grouped = (
        df_selected_year.groupby(["EDOCVE", "EDONOM"])[["SV", "NV"]]
        .sum()
        .reset_index()
    )
    map_grouped = (
        df_filtered_sections.groupby(["EDOCVE", "EDONOM"])[["SV", "NV"]]
        .sum()
        .reset_index()
    )
    map_grouped["Participación"] = (
        map_grouped["SV"] / (map_grouped["SV"] + map_grouped["NV"]) * 100
    ).round(1)

    map_grouped["EDOCVE"] = map_grouped["EDOCVE"].astype(int)

    section_type_text_displayed = (
        ", ".join(selected_section_type_labels) if selected_section_type_labels else "Todas"
    )

    map_grouped["tipo_seccion"] = section_type_text_displayed

    map_grouped["EDOCVE"] = map_grouped["EDOCVE"].astype(int)

    fig_map = px.choropleth_map(
        map_grouped,
        geojson=geojson_data,
        locations="EDOCVE",
        featureidkey="properties.matched_edocve",
        color="Participación",
        hover_name="EDONOM",
        hover_data={
            "EDOCVE": False,
            "tipo_seccion": True,
        },
        labels={
            "Participación": "% Participación",
            "tipo_seccion": "Tipo de sección"
        },
        color_continuous_scale=CUSTOM_MAP_SCALE,
        range_color=[0, 100],
        map_style="carto-positron",
        center={"lat": 23.6345, "lon": -102.5528}, 
        zoom=4.2,
    )
    fig_map.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, 
        height=400,
        coloraxis_colorbar=dict(title="Participación (%)"),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.divider()

    st.subheader("Histórico de la participación electoral por Estado")
    st.markdown(
        "En más de una década, los datos estatales confirman que las mujeres han demostrado ser un pilar importante en la participación democrática del país."
    )

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
        color_continuous_scale=CUSTOM_HEATMAP_SCALE,
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

    st.markdown(
        "Cada periodo electoral es un peldaño ganado con esfuerzo y tu voto individual suma una fuerza colosal. Desistir hoy es frenar una marcha que tomó décadas consolidar."
    )
    st.markdown(
            "**Sigue abriendo el camino, tu voz es indispensable para mantener vivo el balance de tu estado.**"
        )

## Columna 2: Lista con los estados que más votaron
with col2:
    st.subheader(f"¿Cuántos votos emitieron las mujeres?")
    st.markdown(f"Las entidades con mayor volumen de votos emitidos en {selected_year}")

    top_12_list = (
        map_grouped.sort_values(by="SV", ascending=False).head(12).reset_index(drop=True)
    )

    fig_list = px.bar(
        top_12_list,
        x="SV",
        y="EDONOM",
        orientation="h",
        text="SV",
        color="SV",
        hover_data={
            "SV": ":,",
        },
        labels={
            "SV": "Votos emitidos",
            "EDONOM": "Estado",
        },
        color_continuous_scale=CUSTOM_BAR_SCALE,
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

    st.markdown("---")
    st.markdown("### **Haz la diferencia**")
    st.markdown(
        "Cuando un estado demuestra una alta participación electoral, significa que su ciudadanía está viva y vigilante. No votar es debilitar nuestra propia fuerza colectiva."
    )
    st.markdown(
            "**¡Tu voto sí importa, ejércelo!**"
    )

st.markdown("---")
st.caption("Fuente: Conteos Censales de Participación Ciudadana (CCPC), INE")
