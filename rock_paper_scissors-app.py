import streamlit as st

st.markdown("## Rock, Paper, Scissors Game (2 players)")

st.write("Welcome! Each player must choose one of the options below.")
play_options = ("rock", "paper", "scissors")
st.write(f"Play options: {play_options}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    player01_play = st.selectbox("Player 01, choose your play option:", play_options)
with col2:
    player02_play = st.selectbox("Player 02, choose your play option:", play_options)

if st.button("Play!"):
    st.divider()
    st.write(f"Player 01 chose: **{player01_play}**")
    st.write(f"Player 02 chose: **{player02_play}**")
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
        st.warning("Result: Player 02 won!")
