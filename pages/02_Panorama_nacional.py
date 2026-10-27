import streamlit as st

st.set_page_config(
    page_title="Panorama nacional", layout="wide"
)


def load_css():
  with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.markdown(
    '<div class="hero-title">Contexto Político e Histórico</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="story-card">
    <p class="content-text">
    A lo largo de los periodos electorales comprendidos entre 2009 y 2024, México ha atravesado transformaciones 
    democráticas determinantes. Comprender la participación requiere analizar la alternancia política y las reformas institucionales.
    </p>
</div>
""",
    unsafe_allow_html=True,
)
