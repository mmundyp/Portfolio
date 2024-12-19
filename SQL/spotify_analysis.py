import sqlite3

# Define the database and SQL file paths
db_path = '/Desktop/Github projects/spotify_songs.db'
sql_file_path = '/Desktop/Github projects/spotify_analysis.sql'

def read_queries(sql_file_path):
    with open(sql_file_path, 'r') as file:
        return file.read().split(';')  # Split queries by semicolon

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Load and execute queries
queries = read_queries(sql_file_path)
for query in queries:
    query = query.strip()  # Remove extra whitespace
    if query:  # Skip empty queries
        print(f"Executing query:\n{query}\n")
        cursor.execute(query)
        # Fetch column names (headers)
        if cursor.description is not None:
            column_names = [desc[0] for desc in cursor.description]
            print(column_names)
        for row in cursor.fetchall():
            print(row)
        print()

# Close connection
conn.close()
