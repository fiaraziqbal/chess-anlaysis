import os
import chess
import chess.pgn
import chess.engine
import matplotlib.pyplot as plt
from datetime import datetime

# Chess engine initialization
engine_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Folder path containing the PGN files
folder_path = "games"

# Lists to store accuracy values and corresponding dates for games played by the specific player
accuracy_values = []
game_dates = []

# Player's username to filter the games
target_player_username = "jibrealfiaraz"

# Depth limit for analysis
depth_limit = 10

# Iterate over the files in the folder
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".pgn"):
        pgn_file = os.path.join(folder_path, filename)
        with open(pgn_file) as f:
            # Read the PGN game
            game = chess.pgn.read_game(f)

            # Check if the target player is playing in the game
            if target_player_username in [game.headers.get("White"), game.headers.get("Black")]:
                # Set up the board
                board = game.board()

                # Initialize accuracy counters for the target player
                total_moves = 0
                accurate_moves = 0

                # Analyze each move in the game
                for node in game.mainline():
                    move = node.move

                    # Check if the move is legal
                    if move in board.legal_moves:
                        total_moves += 1

                        # Analyze the current position with depth limit
                        result = engine.play(board, chess.engine.Limit(depth=depth_limit))
                        suggested_move = result.move

                        # Compare the suggested move with the actual move
                        if suggested_move == move:
                            accurate_moves += 1

                        # Play the move on the board
                        board.push(move)

                # Calculate accuracy percentage for the game
                accuracy = (accurate_moves / total_moves) * 100

                # Add accuracy value and game date to the lists
                accuracy_values.append(accuracy)
                game_dates.append(datetime.strptime(game.headers.get("Date"), "%Y.%m.%d").date())

# Close the engine
engine.quit()

# Sort the accuracy and date lists based on the game dates
accuracy_values, game_dates = zip(*sorted(zip(accuracy_values, game_dates)))

# Plot the scatter graph
plt.scatter(game_dates, accuracy_values, c='blue', edgecolors='black')
plt.xlabel("Date")
plt.ylabel("Accuracy (%)")
plt.title(f"Accuracy of Games Played by {target_player_username}")
plt.xticks(rotation=45)
plt.ylim(0)  # Set the y-axis minimum value to 0
plt.tight_layout()
plt.show()
