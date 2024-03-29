import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import sqlite3

def show_recommend_tab():
    st.header("Recommend a Movie", divider="rainbow")
    # Load data from SQLite database
    conn = sqlite3.connect('database.db')
    ratings = pd.read_sql_query("SELECT * FROM ratings", conn)
    movies = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()

    # Merge data
    ratings = pd.merge(movies, ratings).drop(['genres', 'timestamp'], axis=1)

    # Step 2: Pivot the DataFrame to create a user-item matrix
    user_item_matrix = ratings.pivot_table(index='userId', columns='title', values='rating')

    # Step 3: Normalize the ratings
    scaler = MinMaxScaler()
    user_item_matrix_normalized = pd.DataFrame(scaler.fit_transform(user_item_matrix.fillna(0)),
                                            columns=user_item_matrix.columns,
                                            index=user_item_matrix.index)

    # Step 4: Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(user_item_matrix_normalized.T)

    # Step 5: Make recommendations based on similarity scores
    def get_similar_movies(movie_title, cosine_sim=cosine_sim, top_n=10):
        idx = user_item_matrix.columns.get_loc(movie_title)
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  # Exclude the 0th index and select the top N similar movies
        movie_indices = [i[0] for i in sim_scores]
        similar_movies = user_item_matrix.columns[movie_indices]
        similarity_scores = [i[1] for i in sim_scores]
        return pd.DataFrame({'Movie': similar_movies, 'Similarity': similarity_scores})

    # Streamlit UI
    #st.title('Movie Recommendation')

    # Step 6: Take input from the user
    movie_title_input = st.text_input("Enter the movie title:")

    if movie_title_input:
        # Step 7: Use fuzzy string matching to find similar titles
        similar_movie, score = process.extractOne(movie_title_input, user_item_matrix.columns)

        # Step 8: Output the suggested movie title
        st.write(f"Suggested movie title: {similar_movie} (score: {score})")

        # Step 9: Run collaborative filtering on the suggested movie title
        similar_movies = get_similar_movies(similar_movie)
        st.write(f"Top 10 similar movies to '{similar_movie}':")
        st.write(similar_movies)
