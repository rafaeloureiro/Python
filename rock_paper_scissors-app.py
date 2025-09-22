import streamlit as st
import random

st.markdown("## Rock, Paper, Scissors Game (Player vs Computer)")

st.write("Welcome! You (Player 01) will choose your move, and the computer will guess randomly.")
play_options = ("rock", "paper", "scissors")
st.write(f"Play options: {play_options}")

st.divider()

player01_play = st.selectbox("Player 01, choose your play option:", play_options)

if st.button("Play!"):
    player02_play = random.choice(play_options)
    st.divider()
    st.write(f"Player 01 chose: **{player01_play}**")
    st.write(f"Computer (Player 02) chose: **{player02_play}**")
    st.divider()

    # --- Game logic ---
    if player01_play not in play_options or player02_play not in play_options:
        st.error("One or both plays are invalid. Please, choose only 'rock', 'paper' or 'scissors'.")
    elif (
        (player01_play == "rock" and player02_play == "scissors") or
        (player01_play == "scissors" and player02_play == "paper") or
        (player01_play == "paper" and player02_play == "rock")
    ):
        st.success("Result: Player 01 won! Congratulations!")
    elif player01_play == player02_play:
        st.info("Result: TIE!")
    else:
        st.warning("Result: Computer won! Try again!")
