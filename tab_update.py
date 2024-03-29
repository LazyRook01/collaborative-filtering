import streamlit as st
import sqlite3
import pandas as pd

# Function to create SQLite database and tables
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create ratings table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings
                      (userId INT, movieId INT, rating FLOAT, timestamp INT)''')

    # Create movies table
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                      (movieId INT, title TEXT, genres TEXT)''')

    conn.commit()
    conn.close()

# Function to import data from parquet files
def import_data():
    ratings_df = pd.read_parquet('ratings.parquet')
    movies_df = pd.read_parquet('movies.parquet')

    conn = sqlite3.connect('database.db')

    # Insert data into ratings table
    ratings_df.to_sql('ratings', conn, if_exists='replace', index=False)

    # Insert data into movies table
    movies_df.to_sql('movies', conn, if_exists='replace', index=False)

    conn.close()

# Function to add new entry to database
def add_entry(userId, movieId, rating, timestamp, title, genres):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert new entry into ratings table
    cursor.execute('''INSERT INTO ratings (userId, movieId, rating, timestamp) 
                      VALUES (?, ?, ?, ?)''', (userId, movieId, rating, timestamp))

    # Insert new entry into movies table
    cursor.execute('''INSERT INTO movies (movieId, title, genres) 
                      VALUES (?, ?, ?)''', (movieId, title, genres))

    conn.commit()
    conn.close()

# Main function to run the Streamlit app
def main():
    st.title('Movie Ratings Database')

    # Create database and import data if it hasn't been done yet
    create_database()
    import_data()

    # Add new entry form
    st.header('Add New Entry')
    userId = st.number_input('User ID', min_value=1)
    movieId = st.number_input('Movie ID', min_value=1)
    rating = st.number_input('Rating', min_value=0.0, max_value=5.0, step=0.1)
    timestamp = st.number_input('Timestamp', min_value=0)
    title = st.text_input('Title')
    genres = st.text_input('Genres')

    if st.button('Add Entry'):
        add_entry(userId, movieId, rating, timestamp, title, genres)
        st.success('Entry added successfully!')

if __name__ == '__main__':
    main()
