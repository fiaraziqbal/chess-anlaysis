import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('games.db')
cursor = conn.cursor()

# Retrieve all dates from every game in the table
cursor.execute("SELECT DISTINCT SUBSTR(pgn, INSTR(pgn, '[Date \"') + 7, 10) FROM games")
dates = cursor.fetchall()

# Print the dates
print("Dates in the database:")
for date in dates:
    print(date[0])

# Close the connection to the database
conn.close()
