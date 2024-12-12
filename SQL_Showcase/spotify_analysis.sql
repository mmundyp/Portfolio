-- spotify_queries.sql
PRAGMA table_info(spotify_songs);

--convert duration to minutes:seconds
UPDATE spotify_songs
SET duration = printf('%d:%02d', duration / 60, duration % 60);

--top 10 most popular songs
SELECT 
    song_title AS "Song Title", 
    artist AS "Artist", 
    popularity AS "Popularity"
FROM spotify_songs
WHERE popularity = 1 
AND release_date BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY popularity DESC
LIMIT 10;

--top 5 popular genres
SELECT 
    genre AS "Genre", 
    COUNT(song_title) AS "Genre Count"
FROM spotify_songs
WHERE popularity <= 1000
AND release_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY genre
ORDER BY "Genre Count" DESC
LIMIT 5;

--song duration by genre
DROP TABLE IF EXISTS genre_duration;
CREATE TABLE genre_duration AS
SELECT
    genre AS "Genre", 
    AVG(duration) AS "Average Duration", 
    MAX(duration) AS "Longest Song", 
    MIN(duration) AS "Shortest Song"
FROM spotify_songs
WHERE release_date BETWEEN '2024-01-01' AND '2024-12-31'
AND popularity >= 100 
AND duration > 300
GROUP BY genre;

-- Display genre duration table
SELECT *
FROM genre_duration
LIMIT 5;

-- Temporary Table for Duration Calculations

DROP TABLE IF EXISTS duration_calc;
CREATE TABLE duration_calc AS
SELECT 
    s.song_title AS "Song Title", 
    s.genre AS "Genre", 
    s.duration AS "Duration", 
    gd."Average Duration",
    s.duration - gd."Average Duration" AS "Duration Variance"
    -- (CAST(SUBSTR(gd."Average Duration", 1, INSTR(gd."Average Duration", ':') - 1) AS INTEGER) * 60 + 
    -- CAST(SUBSTR(gd."Average Duration", INSTR(gd."Average Duration", ':') + 1) AS INTEGER)) AS "Duration Variance"
FROM spotify_songs s
JOIN genre_duration gd ON s.genre = gd."Genre"
WHERE s.release_date BETWEEN '2024-01-01' AND '2024-12-31'
AND s.popularity >= 100 
AND s.duration > 300;

-- Display duration calculation table
SELECT *
FROM duration_calc
LIMIT 5;

-- Final Query: Top Songs with Duration Close to Genre Average
SELECT *
FROM duration_calc
WHERE "Duration Variance" <= (duration * 1.03)
LIMIT 10;