import streamlit as st

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Rafael Fernandes - Portfolio",
    page_icon="💻",
    layout="wide"
)

# Header
st.markdown("<h1 style='text-align: center;'>Rafael Fernandes portfolio</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Welcome to my Python portfolio! 🚀</p>", unsafe_allow_html=True)

# About me
st.header("About Me")
st.write("""
I am a data analyst and Python developer who enjoys working with automation, data analysis, and web applications.  
This page showcases some of my projects built with Python.
""")

# Links
st.markdown(
    """
    **🔗 Connect with me:**  
    - [LinkedIn](https://www.linkedin.com/in/rafaeloureiro/)  
    - [GitHub](https://github.com/rafaeloureiro)  
    """
)

st.divider()

# Projects Section
st.header("Projects")

# Project 1
st.subheader("CPF Validator")
st.write("This function is designed to validate Brazilian CPF (Cadastro de Pessoas Físicas) numbers, which are identification numbers for individuals in Brazil.")
st.markdown("[Open App](https://phyton-5wygoo5pv5qwkhs8b2rktu.streamlit.app/)")
st.markdown("[View on GitHub](https://github.com/rafaeloureiro)")
