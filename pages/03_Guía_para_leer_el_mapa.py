import streamlit as st

st.set_page_config(
    page_title="Guía", layout="wide"
)


def load_css():
  with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.markdown(
    '<div class="hero-title">Metodología y Procesamiento</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="story-card">
    <h3>Cálculo de Participación</h3>
    <p class="content-text">
    La tasa de participación se calcula de forma exacta sumando el Total de Votos Emitidos (SV) 
    y dividiéndolo entre la Lista Nominal Total (SV + NV):
    </p>
    <code>Participación (%) = [ SV / (SV + NV) ] * 100</code>
</div>
""",
    unsafe_allow_html=True,
)
