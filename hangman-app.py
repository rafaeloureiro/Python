import streamlit as st
import random
import string

# --- 1. Load words ---
words = ["python", "developer", "streamlit", "hangman", "programming", "database", "science", "cloud"]

# --- 2. Session state to keep the game state ---
if "word" not in st.session_state:
    st.session_state.word = random.choice(words).lower()
if "discovered" not in st.session_state:
    st.session_state.discovered = ["_" for _ in st.session_state.word]
if "attempts_left" not in st.session_state:
    st.session_state.attempts_left = 6
if "attempted_letters" not in st.session_state:
    st.session_state.attempted_letters = []

st.title("🎮 Hangman Game")

# --- 3. Display current state ---
st.write("Word: ", " ".join(st.session_state.discovered))
st.write("Attempts left:", st.session_state.attempts_left)
st.write("Letters already tried:", ", ".join(st.session_state.attempted_letters) if st.session_state.attempted_letters else "None")

# --- 4. Input from user ---
guess = st.text_input("Enter a letter (a-z)").lower()

# --- 5. Process the guess ---
if guess:
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

# --- 6. Check game over ---
if "_" not in st.session_state.discovered:
    st.balloons()
    st.success(f"🎉 Congratulations! You won! The word was: {st.session_state.word}")
elif st.session_state.attempts_left <= 0:
    st.error(f"💀 Game Over! You lost. The word was: {st.session_state.word}")

# --- 7. Restart game button ---
if st.button("Restart Game"):
    st.session_state.clear()  # Clears all session state variables
    st.experimental_rerun()   # Reruns the script

