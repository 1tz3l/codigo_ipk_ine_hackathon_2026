import streamlit as st

st.set_page_config(page_title="Conclusión", layout="wide")


def load_css():
  with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.markdown(
    '<div class="hero-title">Limitaciones de los Datos</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="story-card">
    <p class="content-text">
    Los datos pre-agregados consolidan la lista nominal y los votos válidos. 
    Cambios en la distritación electoral entre 2009 y 2024 han sido homogenizados a nivel estatal para mantener consistencia geográfica.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()
st.info("Coloca el footer / pie de página aquí")