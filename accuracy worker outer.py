import chess
import chess.pgn
import chess.engine

# Chess engine initialization
engine_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Load the PGN file
pgn_file = "game.pgn"
with open(pgn_file) as f:
    # Read the PGN game
    game = chess.pgn.read_game(f)

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
    depth_limit = 14  # Set the desired depth limit for analysis
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
    player1_accuracy = (player1_accurate_moves / player1_total_moves) * 100
    player2_accuracy = (player2_accurate_moves / player2_total_moves) * 100

    # Print accuracy result for each player
    print(f"{player1_username} Accuracy: {player1_accuracy:.2f}%")
    print(f"{player2_username} Accuracy: {player2_accuracy:.2f}%")

# Close the engine
engine.quit()
