import streamlit as st
import random

# --- Game Constants ---
PLAY_OPTIONS = ("rock", "paper", "scissors")

# --- Game Logic as a Function ---
def get_winner(player, computer):
    if player not in PLAY_OPTIONS or computer not in PLAY_OPTIONS:
        return "invalid"
    if player == computer:
        return "tie"
    if (
        (player == "rock" and computer == "scissors") or
        (player == "scissors" and computer == "paper") or
        (player == "paper" and computer == "rock")
    ):
        return "player"
    return "computer"

# --- UI Functions ---
def show_intro():
    st.markdown("## Rock, Paper, Scissors Game (Player vs Computer)")
    st.write("Welcome! You (Player 01) will choose your move, and the computer will guess randomly.")
    st.write(f"Play options: {PLAY_OPTIONS}")
    st.divider()

def play_round():
    player_choice = st.selectbox("Player 01, choose your play option:", PLAY_OPTIONS)
    play_button = st.button("Play!")
    if play_button:
        computer_choice = random.choice(PLAY_OPTIONS)
        st.divider()
        st.write(f"Player 01 chose: **{player_choice}**")
        st.write(f"Computer (Player 02) chose: **{computer_choice}**")
        st.divider()
        result = get_winner(player_choice, computer_choice)
        if result == "invalid":
            st.error("One or both plays are invalid. Please, choose only 'rock', 'paper' or 'scissors'.")
        elif result == "player":
            st.success("Result: Player 01 won! Congratulations!")
        elif result == "tie":
            st.info("Result: TIE!")
        else:
            st.warning("Result: Computer won! Try again!")

# --- Main App ---
def main():
    # Set the tab name
    st.set_page_config(page_title="✊🤚✌️ Rock, paper, scissors game")
    show_intro()
    play_round()

if __name__ == "__main__":
    main()
