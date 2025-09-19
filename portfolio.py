# app.py
import streamlit as st
from components.header import show_header
from components.about_me import show_about_me
from components.projects import show_projects

# 1️⃣ Page configuration – must be the *first* Streamlit call
st.set_page_config(
    page_title="Rafael Fernandes - Portfolio",
    page_icon="💻",
    layout="wide"
)

def main():
    """Orchestrate the layout of the Streamlit app."""
    show_header()     # Header + page config (already called above)
    show_about_me()   # About Me section
    show_projects()   # Projects list

if __name__ == "__main__":
    main()
    # components/header.py
import streamlit as st

def show_header():
    """Display the main header and introductory text."""
    st.markdown(
        "<h1 style='text-align: center; color:#f18016;'>Rafael's portfolio</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; color:black;'><b>Welcome to my Python portfolio! 🚀</b></p>",
        unsafe_allow_html=True
    )
    # components/about_me.py
import streamlit as st

def show_about_me():
    """Display the About Me section with contact links."""
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
    st.markdown(
        """
        **🔗 Connect with me**  
        - [LinkedIn](https://www.linkedin.com/in/rafaeloureiro/)  
        - [GitHub](https://github.com/rafaeloureiro)  
        """
    )
    st.divider()
    # components/projects.py
import streamlit as st

def show_projects():
    """List all projects with titles, descriptions, and links."""
    st.markdown("<h2 style='color:#f18016;'>Projects</h2>", unsafe_allow_html=True)

    # Project 01 – CPF Validator
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
    st.markdown(
        """
        - [Open App](https://phyton-5wygoo5pv5qwkhs8b2rktu.streamlit.app/)
        - [View on GitHub](https://github.com/rafaeloureiro)
        """
    )

    # Project 02 – Hangman
    st.markdown("**🕹️ Hangman game**")
    st.markdown(
        """
        <p style='color:black;'>
        Hangman is a classic word‑guessing game for one player on which he
        tries to guess a random word by suggesting letters one by one within a limited number of incorrect guesses.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        - [Open App](https://phyton-cn6wsape5vnb5elwrdzwb6.streamlit.app/)
        - [View on GitHub](https://github.com/rafaeloureiro/Phyton/edit/main/portfolio.py)
        """
    )
