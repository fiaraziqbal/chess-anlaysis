import chess
import chess.pgn
import chess.engine

# Load the PGN file
pgn_file = "game.pgn"
with open(pgn_file) as f:
    game = chess.pgn.read_game(f)

# Initialize the chess engine
engine_path = "C:\\Users\\jibreal\\Downloads\\stockfish-windows-x86-64-avx2 (1)\\stockfish\\stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

# Set up the board
board = game.board()

# Initialize accuracy counter
total_moves = 0
accurate_moves = 0

# Play through the moves and analyze the game
for move in game.mainline_moves():
    total_moves += 1
    board.push(move)

    # Analyze the current position
    result = engine.play(board, chess.engine.Limit(time=2.0))
    suggested_move = result.move

    # Convert the suggested move to SAN
    suggested_move_san = board.san(suggested_move)

    # Compare the suggested move with the actual move
    if suggested_move_san == str(move):
        accurate_moves += 1

    print("Move:", move)
    print("Suggested move:", suggested_move_san)
    print()

# Calculate accuracy percentage
accuracy = (accurate_moves / total_moves) * 100

# Print accuracy result
print("Accuracy:", accuracy)

# Close the engine
engine.quit()
