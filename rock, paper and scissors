# --- 1. Rules and presentation ---

print("------------------------------------------------------")
print("--- Game rock, paper and scissors (2 players) ---")
print("------------------------------------------------------")
print("Welcome, each player must choose one of the options.")

#Tuple is used here because we shouldn't modify the options we do use do play
play_options = ("rock", "paper", "scissors")
print(f"Play options: {play_options}")
print("------------------------------------------------------")

# --- 2. Data input ---
player01_initial_play = input("Player 01, choose your play option: ")
player02_initial_play = input("Player 02, choose your play option: ")
print("------------------------------------------------------")

# --- 3. Data processing ---
#The inputed data through input funcion is always typed as string
#In order to avoid data processing errors, we convert the input data to lowercase and remove spaces.
player01_play = player01_initial_play.lower().strip()
player02_play = player02_initial_play.lower().strip()
print("------------------------------------------------------")
print(f"Player 01 chose: {player01_play}")
print(f"Player 02 chose: {player02_play}")
print("------------------------------------------------------")

# Checks if the plays are valid
if player01_play not in play_options or player02_play not in play_options:
    print("One or both plays are invalid. Please, choose only 'rock', 'paper' or 'scissors'.")

# --- 4. Game logic and result ---
#Case01: WIN!
elif (player01_play == "pedra" and player02_play == "scissors") or \
     (player01_play == "scissors" and player02_play == "paper") or \
     (player01_play == "paper" and player02_play == "rock"):
    print("Result: Player 01 won! Congratulations!")

#Case02: TIE!
elif player01_play == player02_play:
    print("Result: TIE!")

#Case03: LOSS!
else:
    print("Result: Player 02 won!")

