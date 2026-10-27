import streamlit as st

st.set_page_config(page_title="Trivia", layout="wide")


def load_css():
  with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.markdown(
    '<div class="hero-title">Conclusiones y Hallazgos Clave</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="story-card">
    <h3>Patrones Detectados</h3>
    <ul>
        <li><strong>Brecha Urbana-Rural:</strong> Se observa una participación proporcionalmente más alta en secciones rurales.</li>
        <li><strong>Elecciones Presidenciales vs Intermedias:</strong> Los años 2012, 2018 y 2024 registran mayor volumen comparado con intermedias.</li>
    </ul>
</div>
""",
    unsafe_allow_html=True,
)
