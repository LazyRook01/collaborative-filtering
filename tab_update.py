import streamlit as st
import sqlite3
import pandas as pd

def show_update_tab():
    st.header("Rate a Movie", divider="rainbow")

    # Function to add new entry to database
    def add_entry(userId, movieId, rating, timestamp, title, genres):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Insert new entry into ratings table
            cursor.execute('''INSERT INTO ratings (userId, movieId, rating, timestamp) 
                            VALUES (?, ?, ?, ?)''', (userId, movieId, rating, timestamp))

            # Insert new entry into movies table
            cursor.execute('''INSERT INTO movies (movieId, title, genres) 
                            VALUES (?, ?, ?)''', (movieId, title, genres))

            conn.commit()
            st.success('Entry added successfully!')
        except sqlite3.Error as e:
            st.error(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    # Function to select and display table
    def display_table(table_name):
        try:
            conn = sqlite3.connect('database.db')

            # Retrieve data from selected table
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)

            # Display the table
            st.write(df)
        except sqlite3.Error as e:
            st.error(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    # Main function to run the Streamlit app
    def main():
        #st.title('Movie Ratings Database')

        # Add new entry form
        st.subheader('Add New Entry')
        userId = st.number_input('User ID', min_value=1)
        movieId = st.number_input('Movie ID', min_value=1)
        rating = st.number_input('Rating', min_value=0.0, max_value=5.0, step=0.1)
        timestamp = st.number_input('Timestamp', min_value=0)
        title = st.text_input('Title')
        genres = st.text_input('Genres')

        if st.button('Add Entry'):
            add_entry(userId, movieId, rating, timestamp, title, genres)

        st.write("---")
        # Select table to display
        st.subheader('Select Table to Display')
        table_name = st.selectbox('Select Table', ['ratings', 'movies'])

        if table_name:
            display_table(table_name)

    main()

if __name__ == '__main__':
    show_update_tab()
