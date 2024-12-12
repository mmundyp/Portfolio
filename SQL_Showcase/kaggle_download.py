import kagglehub
import sqlite3
import pandas as pd
import os

# Define paths
dataset_name = "refiaozturk/spotify-songs-dataset"
db_path = '/Users/mundy/Desktop/Github projects/spotify_songs.db'

# Step 1: Download the Spotify dataset using KaggleHub
spotify_data = kagglehub.dataset_download(dataset_name)

# Locate the CSV file in the downloaded folder
# Adjust the path if necessary, assuming the dataset contains a file named "spotify_songs.csv"
csv_file_path = [file for file in os.listdir(spotify_data) if file.endswith('.csv')][0]
csv_full_path = os.path.join(spotify_data, csv_file_path)

# Step 2: Load the CSV data into a Pandas DataFrame
df = pd.read_csv(csv_full_path)

# Step 3: Create a connection to a local SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 4: Create the SQL table schema based on the dataset columns
create_table_query = """
CREATE TABLE IF NOT EXISTS spotify_songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_name TEXT,
    artist_name TEXT,
    album_name TEXT,
    release_date TEXT,
    duration_ms INTEGER,
    popularity INTEGER,
    danceability REAL,
    energy REAL,
    loudness REAL,
    speechiness REAL,
    acousticness REAL,
    instrumentalness REAL,
    liveness REAL,
    valence REAL,
    tempo REAL
);
"""

# Execute the table creation query
cursor.execute(create_table_query)

# Step 5: Insert the DataFrame records into the SQL table
df.to_sql('spotify_songs', conn, if_exists='replace', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database created successfully at: {db_path}")

