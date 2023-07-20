import chess
import chess.pgn
import chess.engine
import matplotlib.pyplot as plt
from datetime import datetime

# Chess engine initialization
engine_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Load the PGN file
pgn_file = "blitz.pgn"

# Create a list to store all games
games = []

with open(pgn_file) as f:
    while True:
        # Read each game from the PGN file
        game = chess.pgn.read_game(f)
        if game is None:
            break

        games.append(game)

# Initialize lists to store timestamps, total accuracies per game, and end times
timestamps = []
total_accuracies = []
end_times = []

# Process each game
for game in games:
    # Extract player usernames from PGN headers
    player1_username = game.headers.get("White", "Player 1")
    player2_username = game.headers.get("Black", "Player 2")

    if player1_username.lower() == "jibrealfiaraz" or player2_username.lower() == "jibrealfiaraz":
        # Set up the board
        board = game.board()

        # Initialize accuracy counters for the specific player
        total_moves = 0
        accurate_moves = 0

        # Analyze each move in the game
        depth_limit = 10  # Set the desired depth limit for analysis
        for node in game.mainline():
            move = node.move

            # Check if the move is legal
            if move in board.legal_moves:
                if (board.turn and player1_username.lower() == "jibrealfiaraz") or (not board.turn and player2_username.lower() == "jibrealfiaraz"):
                    total_moves += 1

                    # Analyze the current position with depth limit
                    result = engine.play(board, chess.engine.Limit(depth=depth_limit))

                    # Get the suggested move from engine analysis
                    suggested_move = result.move

                    # Compare the suggested move with the player's move
                    if suggested_move == move:
                        accurate_moves += 1

                # Play the move on the board
                board.push(move)

        # Calculate accuracy percentage for the specific game
        if total_moves == 0:
            game_accuracy = 0  # Set accuracy to 0 if there are no moves
        else:
            game_accuracy = (accurate_moves / total_moves) * 100

        # Store the timestamp, total accuracy, and end time
        timestamps.append(game.headers["Date"])
        total_accuracies.append(game_accuracy)
        end_times.append(game.headers.get("EndTime"))

# Convert timestamps to datetime objects for sorting
timestamps = [datetime.strptime(timestamp, "%Y.%m.%d") for timestamp in timestamps]  # Update the date format if needed

# Sort the games based on timestamps
sorted_games = sorted(zip(timestamps, end_times, total_accuracies))
timestamps, end_times, total_accuracies = zip(*sorted_games)

# Plot the accuracy over time
plt.plot(end_times, total_accuracies)
plt.xlabel("End Time")
plt.ylabel("Total Accuracy (%)")
plt.title("Total Accuracy of jibrealfiaraz per Game")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Close the engine
engine.quit()
