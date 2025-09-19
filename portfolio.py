import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Rafael Fernandes - Portfolio",
    page_icon="💻",
    layout="wide"
)

# ===== HEADER =====
st.markdown(
    "<h1 style='text-align: center; color:#f18016;'>Rafael's portfolio</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color:black;'>Welcome to my Python portfolio! 🚀</p>",
    unsafe_allow_html=True
)

# ===== ABOUT ME =====
st.markdown("<h2 style='color:#f18016;'>About Me</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='color:black;'>
    I am a data analyst and Python developer who enjoys working with automation, data analysis, and web applications.  
    This page showcases some of my projects built with Python.
    </p>
    """,
    unsafe_allow_html=True
)

# Links
st.markdown(
    """
    **🔗 Connect with me**  
    - [LinkedIn](https://www.linkedin.com/in/rafaeloureiro/)  
    - [GitHub](https://github.com/rafaeloureiro)  
    """
)

st.divider()

# ===== PROJECTS =====
st.markdown("<h2 style='color:#f18016;'>Projects</h2>", unsafe_allow_html=True)

# Project 01
st.markdown("**🔢 CPF Validator**")
st.markdown(
    """
    <p style='color:black;'>
    This function is designed to validate Brazilian CPF (Cadastro de Pessoas Físicas) numbers, 
    which are identification numbers for individuals in Brazil.
    </p>
    """,
    unsafe_allow_html=True
)

# Links
st.markdown(
    """
    - [👉 Open App](https://phyton-5wygoo5pv5qwkhs8b2rktu.streamlit.app/)
    - [📂 View on GitHub](https://github.com/rafaeloureiro)
    """
)
