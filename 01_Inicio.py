import streamlit as st

st.set_page_config(
    page_title="Inicio", layout="wide"
)

def load_css():
  with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.markdown(
    '<div class="hero-title">Participación Electoral en México'
    " (2009–2024)</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">Una mirada profunda a la evolución del voto'
    " ciudadano en los últimos 15 años.</div>",
    unsafe_allow_html=True,
)

st.divider()

col1, col2 = st.columns([1.2, 0.8], gap="large")

with col1:
  st.markdown(
      """
    <div class="story-card">
        <h3>Propósito del Estudio</h3>
        <p class="content-text">
        El comportamiento electoral mexicano ha mostrado patrones geográficos y demográficos cambiantes. 
        Este proyecto consolida los datos de participación a nivel federal para analizar la evolución temporal 
        y la influencia del tipo de sección (Urbana, Rural y Mixta).
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col2:
  st.info(
      "📌 **Navegación:** Utilice el menú de la izquierda para avanzar por las"
      " distintas secciones o ir directamente a la **Página 4: Visualización**."
  )
