# hangman_app.py
# -----------------------------------------------
# A Streamlit version of the classic Hang‑man game.
# -----------------------------------------------

import random
import string
import streamlit as st

# ---------- 1. Word list ----------
WORDS = [
    "python", "developer", "cannabis", "screen", "work",
    "internet", "science", "sea", "soccer", "drive"
]

# ---------- 2. Helper functions ----------
def init_game() -> tuple[str, list[str], int, list[str]]:
    """Return a fresh game state."""
    word = random.choice(WORDS).lower()
    discovered = ["_" for _ in word]
    attempts_left = 6
    attempted_letters = []
    return word, discovered, attempts_left, attempted_letters


def update_state(
    guess: str,
    word: str,
    discovered: list[str],
    attempts_left: int,
    attempted_letters: list[str]
) -> tuple[list[str], int, list[str]]:
    """Process a single letter guess and update the state."""
    if len(guess) != 1 or guess not in string.ascii_lowercase:
        st.error("❌ Invalid input, enter only one letter (a‑z).")
    elif guess in attempted_letters:
        st.warning("⚠️ You've already attempted this letter.")
    else:
        attempted_letters.append(guess)
        if guess in word:
            for idx, letter in enumerate(word):
                if letter == guess:
                    discovered[idx] = guess
            st.success(f"✅ Good attempt! '{guess}' is in the word.")
        else:
            attempts_left -= 1
            st.error(f"❌ Oh no! '{guess}' is not in the word.")
    return discovered, attempts_left, attempted_letters


def check_game_over(word: str, discovered: list[str], attempts_left: int) -> bool:
    """Return True if the game has finished, otherwise False."""
    if "_" not in discovered:
        st.balloons()
        st.success(f"🎉 Congratulations! You won! The word was: **{word}**")
        return True
    if attempts_left <= 0:
        st.emoji("💀")
        st.error(f"💀 Game Over! You lost. The word was: **{word}**")
        return True
    return False


# ---------- 3. Streamlit UI ----------
st.title("🕹️ Hang‑man (Streamlit Edition)")

# Initialise session state variables if they don't exist
if "word" not in st.session_state:
    st.session_state["word"], st.session_state["discovered"], \
    st.session_state["attempts_left"], st.session_state["attempted_letters"] = init_game()

# Show current game status
st.subheader("Word:")
st.write(" ".join(st.session_state["discovered"]))
st.subheader("Attempts left:")
st.write(st.session_state["attempts_left"])
st.subheader("Letters tried:")
st.write(", ".join(st.session_state["attempted_letters"]) or "None")

# Input box + Guess button
guess = st.text_input("Enter a letter (a‑z)", key="guess_input")
if st.button("Guess"):
    if guess:
        st.session_state["discovered"], st.session_state["attempts_left"], \
        st.session_state["attempted_letters"] = update_state(
            guess.lower(),
            st.session_state["word"],
            st.session_state["discovered"],
            st.session_state["attempts_left"],
            st.session_state["attempted_letters"]
        )
        if check_game_over(
            st.session_state["word"],
            st.session_state["discovered"],
            st.session_state["attempts_left"]
        ):
            # Disable input after game over
            st.session_state["guess_input"] = ""

# Restart button
if st.button("Restart"):
    st.session_state["word"], st.session_state["discovered"], \
    st.session_state["attempts_left"], st.session_state["attempted_letters"] = init_game()
    st.session_state["guess_input"] = ""

