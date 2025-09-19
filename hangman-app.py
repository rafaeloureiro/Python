# hangman_streamlit.py
import random
import string
import streamlit as st

# ---------- 1. Word bank ----------
WORDS = [
    "python", "developer", "cannabis", "screen", "work",
    "internet", "science", "sea", "soccer", "drive"
]

# ---------- 2. Game State Management ----------
def initialize_game():
    """Initialize or reset the game state."""
    if "game_state" not in st.session_state:
        reset_game()

def reset_game():
    """Reset the game to initial state."""
    word = random.choice(WORDS).lower()
    st.session_state.game_state = {
        "word": word,
        "discovered": ["_" for _ in word],  # This creates the underscores
        "attempts_left": 6,
        "attempted_letters": [],
        "game_over": False,
        "message": {"text": "", "type": ""}
    }

def get_game_state():
    """Get the current game state."""
    return st.session_state.game_state

def update_game_state(key, value):
    """Update a specific value in the game state."""
    st.session_state.game_state[key] = value

# ---------- 3. Game Logic ----------
def process_guess(guess):
    """Process a player's guess."""
    game_state = get_game_state()
    
    # Validation
    if len(guess) != 1 or guess not in string.ascii_lowercase:
        update_game_state("message", {"text": "❌ Invalid input – only a single letter (a‑z) is allowed.", "type": "error"})
        return
    
    if guess in game_state["attempted_letters"]:
        update_game_state("message", {"text": "⚠️ You already tried that letter.", "type": "warning"})
        return
    
    # Add to attempted letters
    attempted_letters = game_state["attempted_letters"] + [guess]
    update_game_state("attempted_letters", attempted_letters)
    
    # Check if guess is correct
    if guess in game_state["word"]:
        # Reveal all positions that match the guessed letter
        discovered = game_state["discovered"].copy()
        for i, letter in enumerate(game_state["word"]):
            if letter == guess:
                discovered[i] = guess
        
        update_game_state("discovered", discovered)
        update_game_state("message", {"text": f"✅ Good job! '{guess}' is in the word.", "type": "success"})
    else:
        attempts_left = game_state["attempts_left"] - 1
        update_game_state("attempts_left", attempts_left)
        update_game_state("message", {"text": f"❌ Oops! '{guess}' is not in the word.", "type": "error"})
    
    # Check if game is over
    check_game_over()

def check_game_over():
    """Check if the game has ended and update state accordingly."""
    game_state = get_game_state()
    
    if "_" not in game_state["discovered"]:
        update_game_state("game_over", True)
        st.balloons()
        update_game_state("message", {"text": f"🎉 You won! The word was **{game_state['word']}**.", "type": "success"})
    elif game_state["attempts_left"] <= 0:
        update_game_state("game_over", True)
        update_game_state("message", {"text": f"💀 Game over – you lost. The word was **{game_state['word']}**.", "type": "error"})

# ---------- 4. UI Components ----------
def display_header():
    """Display the game header."""
    st.set_page_config(page_title="Hang‑man", layout="centered")
    st.title("🕹️ Hangman Game")

def display_word():
    """Display the word with underscores for hidden letters."""
    game_state = get_game_state()
    st.subheader("Word:")
    # Display each letter or underscore with proper spacing
    st.markdown(f"**{' '.join(game_state['discovered'])}**")
    st.write("")  # Add some spacing

def display_attempts():
    """Display remaining attempts."""
    game_state = get_game_state()
    st.subheader("Attempts left:")
    st.write(game_state["attempts_left"])

def display_attempted_letters():
    """Display letters that have been tried."""
    game_state = get_game_state()
    st.subheader("Letters tried:")
    st.write(", ".join(game_state["attempted_letters"]) or "None")

def display_game_status():
    """Display the current game status."""
    display_word()
    display_attempts()
    display_attempted_letters()

def display_message():
    """Display any game messages."""
    game_state = get_game_state()
    if game_state["message"]["text"]:
        if game_state["message"]["type"] == "success":
            st.success(game_state["message"]["text"])
        elif game_state["message"]["type"] == "error":
            st.error(game_state["message"]["text"])
        elif game_state["message"]["type"] == "warning":
            st.warning(game_state["message"]["text"])

def display_input_form():
    """Display the input form for guesses."""
    game_state = get_game_state()
    
    with st.form(key='guess_form'):
        guess = st.text_input("Enter a letter (a‑z)", max_chars=1, key="guess_input")
        submitted = st.form_submit_button("Guess", disabled=game_state["game_over"])
    
    if submitted and guess:
        process_guess(guess.lower())
        st.rerun()

def display_restart_button():
    """Display the restart button."""
    if st.button("Restart"):
        reset_game()
        st.rerun()

# ---------- 5. Main Application ----------
def main():
    """Main application function."""
    initialize_game()
    display_header()
    display_game_status()
    display_message()
    display_input_form()
    display_restart_button()

if __name__ == "__main__":
    main()
