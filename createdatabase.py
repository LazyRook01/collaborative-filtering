import streamlit as st
import pandas as pd
import sqlite3

def show_create_database_tab():
    st.header("Create Database", divider="rainbow")
    # Load movies.parquet into pandas dataframe
    df1 = pd.read_parquet("movies.parquet")

    # Load ratings.parquet into pandas dataframe
    df2 = pd.read_parquet("ratings.parquet")

    # Streamlit UI
    #st.title("Create Database")

    # Button to create the database
    if st.button("Create Database"):
        # Step 1: Create SQLite database
        conn = sqlite3.connect('database.db')

        # Step 2: Write df1 into movies table
        df1.to_sql('movies', conn, if_exists='replace', index=False)

        # Step 3: Write df2 into ratings table
        df2.to_sql('ratings', conn, if_exists='replace', index=False)

        # Close connection
        conn.close()

        st.write("SQLite database 'database.db' created successfully.")

    # Select table to display
    selected_table = st.selectbox("Select table", ['movies', 'ratings'])

    # Display selected table
    if selected_table == 'movies':
        st.write("Displaying movies table:")
        st.write(df1)
    elif selected_table == 'ratings':
        st.write("Displaying ratings table:")
        st.write(df2)
