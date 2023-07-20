import sqlite3
import os

# Connect to the SQLite database
conn = sqlite3.connect('games.db')
cursor = conn.cursor()

# Create a table to store the PGN data
cursor.execute('''CREATE TABLE IF NOT EXISTS games
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pgn TEXT)''')

# Specify the folder path where the PGN files are located
folder_path = 'games'

# Get a list of all PGN files in the folder
pgn_files = [f for f in os.listdir(folder_path) if f.endswith('.pgn')]

# Iterate through each PGN file and insert its content into the database
for file_name in pgn_files:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        pgn_data = file.read()
        cursor.execute("INSERT INTO games (pgn) VALUES (?)", (pgn_data,))

# Commit the changes and close the connection to the database
conn.commit()
conn.close()

print("PGN files imported successfully into the database.")
