# hangman_streamlit.py
import random
import string
import streamlit as st

# ---------- 1. Word bank ----------
WORDS = [
    "python", "developer", "cannabis", "screen", "work",
    "internet", "science", "sea", "soccer", "drive"
]

# ---------- 2. Reset / initialise game ----------
def reset_game() -> None:
    """Populate st.session_state with a fresh game."""
    word = random.choice(WORDS).lower()
    st.session_state.update(
        word=word,
        discovered=["_" for _ in word],
        attempts_left=6,
        attempted_letters=[],
    )

# Initialise only once
if "word" not in st.session_state:
    reset_game()

# ---------- 3. Process a single guess ----------
def process_guess(guess: str) -> None:
    """Update state for one letter."""
    if len(guess) != 1 or guess not in string.ascii_lowercase:
        st.error("❌ Invalid input – only a single letter (a‑z) is allowed.")
        return
    if guess in st.session_state.attempted_letters:
        st.warning("⚠️ You already tried that letter.")
        return

    st.session_state.attempted_letters.append(guess)

    if guess in st.session_state.word:
        # Reveal all positions that match the guessed letter
        for i, letter in enumerate(st.session_state.word):
            if letter == guess:
                st.session_state.discovered[i] = guess
        st.success(f"✅ Good job! '{guess}' is in the word.")
    else:
        st.session_state.attempts_left -= 1
        st.error(f"❌ Oops! '{guess}' is not in the word.")

# ---------- 4. Check if the game is over ----------
def check_game_over() -> bool:
    if "_" not in st.session_state.discovered:
        st.balloons()
        st.success(f"🎉 You won! The word was **{st.session_state.word}**.")
        return True
    if st.session_state.attempts_left <= 0:
        st.error(f"💀 Game over – you lost. The word was **{st.session_state.word}**.")
        return True
    return False

# ---------- 5. Streamlit UI ----------
st.set_page_config(page_title="Hang‑man", layout="centered")
st.title("🕹️ Hang‑man (Streamlit Edition)")

# --- 5.1  Status display (after any state change) ---
st.subheader("Word:")
st.write(" ".join(st.session_state.discovered))

st.subheader("Attempts left:")
st.write(st.session_state.attempts_left)

st.subheader("Letters tried:")
st.write(", ".join(st.session_state.attempted_letters) or "None")

# --- 5.2  Text input + Guess button ---
# Create a form to handle input
with st.form(key='guess_form'):
    guess = st.text_input("Enter a letter (a‑z)", max_chars=1, key="guess_input")
    submitted = st.form_submit_button("Guess")

if submitted and guess:
    process_guess(guess.lower())
    # Clear the input by using a form and letting it reset

# --- 5.3  Check game status ---
if check_game_over():
    st.info("Game over! Click 'Restart' to play again.")

# --- 5.4  Restart button ---
if st.button("Restart"):
    reset_game()
    st.rerun()
