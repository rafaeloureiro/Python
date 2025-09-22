import streamlit as st

# 1️⃣ Page configuration – must be the *first* Streamlit call
st.set_page_config(
    page_title="Rafael Fernandes - Portfolio",
    page_icon="💻",
    layout="wide"
)

def show_header():
    """Display the main header and introductory text."""
    st.markdown(
        "<h1 style='text-align: center; color:#f18016;'>Rafael's portfolio</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; color:black;'><b>Welcome to my portfolio!</b></p>",
        unsafe_allow_html=True
    )
    st.markdown("")

def show_about_me():
    """Display the About Me section with contact links and articles."""
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
    st.markdown("<h3 style='color:#f18016;'>Connect with me</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        - [LinkedIn](https://www.linkedin.com/in/rafaeloureiro/)  
        - [GitHub](https://github.com/rafaeloureiro)  
        """
    )
    st.markdown("<h3 style='color:#f18016;'>Articles (written in portuguese)</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        - [Por uma taxonomia do delivery: a emergência do Restaurante Digital](https://www.linkedin.com/pulse/por-uma-taxonomia-do-delivery-emerg%C3%AAncia-restaurante-rafael-fernandes-geayf/?trackingId=s6HGlOCDRneJ5bfGQFjUYg%3D%3D)
        - [Análise IPO Raízen e o Brasil](https://www.linkedin.com/pulse/an%25C3%25A1lise-ipo-ra%25C3%25ADzen-e-o-brasil-rafael-loureiro/?trackingId=nkQVZ0OgTAuNhuTZThXZ2w%3D%3D)
        """
    )
    st.divider()

def show_projects():
    """List all projects with titles, descriptions, and links."""
    st.markdown("<h2 style='color:#f18016;'>Python projects</h2>", unsafe_allow_html=True)

    # Project 01 – Personal assistant in Python programming
    st.markdown("**🤖 Personal assistant in Python programming**")
    st.markdown(
        """
        <p style='color:black;'>
        A Python agent developed during the Data Science Academy course "Python Language Fundamentals - From Basics to AI Applications".  
        This assistant helps users with Python programming questions, offering clear explanations, example code, code details, and official documentation.  
        Designed to support those learning and coding in Python.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        - [Open App](https://dsa-python-assistant.streamlit.app/)  
        - [View on GitHub](https://github.com/rafaeloureiro/Phyton/blob/main/dsa_assistente.py)
        """
    )
    st.markdown("")

    # Project 02 – Rock, paper, scissors
    st.markdown("**✊🤚✌️ Rock, paper, scissors game**")
    st.markdown(
        """
        <p style='color:black;'>
        Play the classic Rock, Paper, Scissors game against the computer!  
        Choose your move and see if you can beat the computer in this simple but fun game.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        - [Open App](https://phyton-rockpaperscissors.streamlit.app/)
        - [View on GitHub](https://github.com/rafaeloureiro/Phyton/blob/main/rock-paper-scissors-app.py)
        """
    )
    st.markdown("")

    # Project 03 – Hangman
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
        - [Open App](https://hangman-game-app.streamlit.app/)
        - [View on GitHub](https://github.com/rafaeloureiro/Phyton/blob/main/hangman-app.py)
        """
    )
    st.markdown("")

    # Project 04 – CPF validator
    st.markdown("**🔢 CPF validator**")
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
        - [Open App](https://cpf-validator-app.streamlit.app/)
        - [View on GitHub](https://github.com/rafaeloureiro/Phyton/blob/main/cpf-validator-app.py)
        """
    )    

def main():
    """Orchestrate the layout of the Streamlit app."""
    show_header()
    show_about_me()
    show_projects()

if __name__ == "__main__":
    main()
