import streamlit as st
import random
import string

# --- 1. Load words ---
WORDS = ["python", "developer", "streamlit", "hangman", "programming", "database", "science", "cloud"]

# --- 2. Functions ---

def init_game():
    """Inicializa o estado do jogo se ainda não existir."""
    if "word" not in st.session_state:
        st.session_state.word = random.choice(WORDS).lower()
    if "discovered" not in st.session_state:
        st.session_state.discovered = ["_" for _ in st.session_state.word]
    if "attempts_left" not in st.session_state:
        st.session_state.attempts_left = 6
    if "attempted_letters" not in st.session_state:
        st.session_state.attempted_letters = []

def display_state():
    """Exibe o estado atual do jogo."""
    st.title("🎮 Hangman Game")
    st.write("Word: ", " ".join(st.session_state.discovered))
    st.write("Attempts left:", st.session_state.attempts_left)
    st.write(
        "Letters already tried:", 
        ", ".join(st.session_state.attempted_letters) if st.session_state.attempted_letters else "None"
    )

def process_guess(guess):
    """Processa o chute do usuário."""
    if len(guess) != 1 or guess not in string.ascii_lowercase:
        st.warning("❌ Invalid input, enter only one letter (a-z).")
    elif guess in st.session_state.attempted_letters:
        st.warning("⚠️ You've already attempted this letter.")
    else:
        st.session_state.attempted_letters.append(guess)
        if guess in st.session_state.word:
            for i, letter in enumerate(st.session_state.word):
                if letter == guess:
                    st.session_state.discovered[i] = guess
            st.success(f"✅ Good attempt! '{guess}' is in the word.")
        else:
            st.session_state.attempts_left -= 1
            st.error(f"❌ Oh no! '{guess}' is not in the word.")

def check_game_over():
    """Verifica se o jogo terminou."""
    if "_" not in st.session_state.discovered:
        st.balloons()
        st.success(f"🎉 Congratulations! You won! The word was: {st.session_state.word}")
        return True
    elif st.session_state.attempts_left <= 0:
        st.error(f"💀 Game Over! You lost. The word was: {st.session_state.word}")
        return True
    return False

def restart_game():
    """Reinicia o jogo definindo novamente o estado do jogo sem usar clear()."""
    st.session_state.word = random.choice(WORDS).lower()
    st.session_state.discovered = ["_" for _ in st.session_state.word]
    st.session_state.attempts_left = 6
    st.session_state.attempted_letters = []

# --- 3. Main App ---

init_game()
display_state()

# --- 4. User Input ---
guess = st.text_input("Enter a letter (a-z)").lower()
if guess:
    process_guess(guess)

# --- 5. Check Game Over ---
check_game_over()

# --- 6. Restart Button ---
if st.button("Restart Game"):
    restart_game()
    st.experimental_rerun()  # safe now, because we não usamos clear()

