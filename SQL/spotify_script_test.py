import sqlite3

# Specify the database file path
db_path = '/Desktop/Github projects/spotify_songs.db'
sql_file_path = '/Desktop/Github projects/spotify_analysis.sql'

# Establish connection to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define your specific SQL query
query = ["""
CREATE TEMPORARY TABLE genre_duration AS
SELECT genre, avg(duration) as avg_duration, max(duration) as longest_song, min(duration) as shortest_song
FROM spotify_songs
WHERE release_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY genre;
"""
"""
--top 10 songs where duration is less than 3% from genre avg
CREATE TEMPORARY TABLE duration_calc AS
SELECT song_title, 
genre, 
duration, 
(SELECT avg_duration FROM genre_duration WHERE genre=spotify_songs.genre) as avg_duration,
(SELECT genre FROM genre_duration WHERE genre = spotify_songs.genre) as avg_duration_genre,
duration - (SELECT avg_duration FROM genre_duration WHERE genre = spotify_songs.genre) as duration_variance
FROM spotify_songs
WHERE release_date BETWEEN '2024-01-01' AND '2024-12-31'
limit 10;
"""

"""SELECT *
FROM duration_calc
WHERE duration_variance < avg_duration * 1.03
AND duration_variance > avg_duration * 0.97;"""
]

try:
    # Execute the SQL queries
    cursor.execute("DROP TABLE IF EXISTS genre_duration")  # Ensure the table doesn't exist
    cursor.execute("DROP TABLE IF EXISTS duration_calc")  # Ensure the table doesn't exist
    for q in query:
        cursor.executescript(q)
    print("Tables created successfully.")

    # Optionally fetch and print the results from genre_duration
    cursor.execute("SELECT * FROM genre_duration")
    rows = cursor.fetchall()
    print("Data in 'genre_duration':")
    headers = [description[0] for description in cursor.description]
    print(headers)
    for row in rows:
        print(row)

    # Optionally fetch and print the results from duration_calc
    cursor.execute("SELECT * FROM duration_calc")
    rows = cursor.fetchall()
    print("Data in 'duration_calc':")
    headers = [description[0] for description in cursor.description]
    print(headers)
    for row in rows:
        print(row)

except sqlite3.Error as e:
    # Handle errors
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    conn.commit()
    conn.close()
