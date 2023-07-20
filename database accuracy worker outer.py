import chess
import chess.pgn
import chess.engine
import sqlite3
from io import StringIO

# Chess engine initialization
engine_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Connect to the SQLite database
conn = sqlite3.connect("games.db")
cursor = conn.cursor()

# Query all games from the database
cursor.execute("SELECT pgn FROM games")
games_pgn = cursor.fetchall()

# Process each game
for pgn_data in games_pgn:
    pgn_str = pgn_data[0]
    pgn_io = StringIO(pgn_str)
    game = chess.pgn.read_game(pgn_io)

    # Extract player usernames from PGN headers
    player1_username = game.headers.get("White", "Player 1")
    player2_username = game.headers.get("Black", "Player 2")

    # Set up the board
    board = game.board()

    # Initialize accuracy counters for both players
    player1_total_moves = 0
    player1_accurate_moves = 0
    player2_total_moves = 0
    player2_accurate_moves = 0

    # Analyze each move in the game
    depth_limit = 10  # Set the desired depth limit for analysis
    for node in game.mainline():
        move = node.move

        # Check if the move is legal
        if move in board.legal_moves:
            if board.turn:  # Player 1 (White)
                player1_total_moves += 1

                # Analyze the current position with depth limit
                result = engine.play(board, chess.engine.Limit(depth=depth_limit))

                # Get the suggested move from engine analysis
                suggested_move = result.move

                # Compare the suggested move with the player's move
                if suggested_move == move:
                    player1_accurate_moves += 1
            else:  # Player 2 (Black)
                player2_total_moves += 1

                # Analyze the current position with depth limit
                result = engine.play(board, chess.engine.Limit(depth=depth_limit))

                # Get the suggested move from engine analysis
                suggested_move = result.move

                # Compare the suggested move with the player's move
                if suggested_move == move:
                    player2_accurate_moves += 1

            # Play the move on the board
            board.push(move)

    # Calculate accuracy percentage for each player
    player1_accuracy = (player1_accurate_moves / player1_total_moves) * 100 if player1_total_moves != 0 else None
    player2_accuracy = (player2_accurate_moves / player2_total_moves) * 100 if player2_total_moves != 0 else None

    # Print usernames and accuracy result for each player
    print(f"{player1_username}, {player2_username}")
    if player1_accuracy is not None:
        print(f"{player1_accuracy:.2f}% accuracy")
    if player2_accuracy is not None:
        print(f"{player2_accuracy:.2f}% accuracy")

    # Add a new line for separation
    print()

# Close the database connection
conn.close()

# Close the engine
engine.quit()
