import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("games.db")
cursor = conn.cursor()

# Count the number of games in the database
cursor.execute("SELECT COUNT(*) FROM games")
total_games = cursor.fetchone()[0]

# Print the number of games
print(f"Total games in the database: {total_games}")

# Close the cursor and connection
cursor.close()
conn.close()
