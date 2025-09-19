# hangman_streamlit.py
# -----------------------------------------------
# Hang‑man for Streamlit – instant counter updates.
# -----------------------------------------------

import random
import string
import streamlit as st

# --------------------------------------------------
# 1. Word list
# --------------------------------------------------
WORDS = [
    "python", "developer", "cannabis", "screen", "work",
    "internet", "science", "sea", "soccer", "drive"
]

# --------------------------------------------------
# 2. Initialise / reset the game state
# --------------------------------------------------
def reset_game() -> None:
    """Populate st.session_state with a fresh game."""
    word = random.choice(WORDS).lower()
    st.session_state.word = word
    st.session_state.discovered = ["_" for _ in word]
    st.session_state.attempts_left = 6
    st.session_state.attempted_letters = []
    st.session_state.guess_input = ""          # clear the textbox

# Initialise on first run
if "word" not in st.session_state:
    reset_game()

# --------------------------------------------------
# 3. Helper that processes a single guess
# --------------------------------------------------
def process_guess(guess: str) -> None:
    """Update the game state for one letter."""
    if len(guess) != 1 or guess not in string.ascii_lowercase:
        st.error("❌ Invalid input – only a single letter (a‑z) is allowed.")
        return

    if guess in st.session_state.attempted_letters:
        st.warning("⚠️ You already tried that letter.")
        return

    st.session_state.attempted_letters.append(guess)

    if guess in st.session_state.word:
        # Reveal all positions that match the guessed letter
        for idx, letter in enumerate(st.session_state.word):
            if letter == guess:
                st.session_state.discovered[idx] = guess
        st.success(f"✅ Good job! '{guess}' is in the word.")
    else:
        st.session_state.attempts_left -= 1
        st.error(f"❌ Oops! '{guess}' is not in the word.")

# --------------------------------------------------
# 4. Check whether the game is finished
# --------------------------------------------------
def check_game_over() -> bool:
    """Return True if the game has finished, otherwise False."""
    if "_" not in st.session_state.discovered:
        st.balloons()
        st.success(f"🎉 You won! The word was **{st.session_state.word}**.")
        return True
    if st.session_state.attempts_left <= 0:
        st.emoji("💀")
        st.error(f"💀 Game over – you lost. The word was **{st.session_state.word}**.")
        return True
    return False

# --------------------------------------------------
# 5. Streamlit UI
# --------------------------------------------------
st.set_page_config(page_title="Hang‑man", layout="centered")
st.title("🕹️ Hang‑man (Streamlit Edition)")

# --- 5.1  Game status (shown *after* any state change) ---
st.subheader("Word:")
st.write(" ".join(st.session_state.discovered))

st.subheader("Attempts left:")
st.write(st.session_state.attempts_left)

st.subheader("Letters tried:")
st.write(", ".join(st.session_state.attempted_letters) or "None")

# --- 5.2  Input & Guess button ---
guess = st.text_input(
    "Enter a letter (a‑z)",
    value=st.session_state.guess_input,
    key="guess_input"
)

if st.button("Guess"):
    if guess:  # only process if something was typed
        process_guess(guess.lower())
        # clear the input field immediately
        st.session_state.guess_input = ""

        # If the game has finished, disable further input
        if check_game_over():
            st.session_state.guess_input = ""

# --- 5.3  Restart button ---
if st.button("Restart"):
    reset_game()
