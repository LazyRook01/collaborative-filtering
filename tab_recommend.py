# Import necessary libraries
import streamlit as st
import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

# Load data
@st.cache(allow_output_mutation=True)
def load_data():
    movies = pd.read_parquet('movies.parquet')
    ratings = pd.read_parquet('ratings.parquet')
    return movies, ratings

# Collaborative filtering
def collaborative_filtering(movies, ratings):
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
    
    return user_item_matrix, cosine_sim

# Get similar movies based on the given movie title
def get_similar_movies(movie_title, user_item_matrix, cosine_sim, top_n=10):
    # Use fuzzy string matching to find similar titles
    similar_movie, score = process.extractOne(movie_title, user_item_matrix.columns)
    
    # Run collaborative filtering on the suggested movie title
    idx = user_item_matrix.columns.get_loc(similar_movie)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Exclude the 0th index and select the top N similar movies
    movie_indices = [i[0] for i in sim_scores]
    similar_movies = user_item_matrix.columns[movie_indices]
    similarity_scores = [i[1] for i in sim_scores]
    return pd.DataFrame({'Movie': similar_movies, 'Similarity': similarity_scores})

# Main function
def main():
    st.title("FilmFinder - Recommendations")
    
    # Load data
    movies, ratings = load_data()
    
    # Collaborative filtering
    user_item_matrix, cosine_sim = collaborative_filtering(movies, ratings)
    
    # Create SQLite database
    conn = sqlite3.connect('database.db')
    movies.to_sql('movies', conn, if_exists='replace', index=False)
    ratings.to_sql('ratings', conn, if_exists='replace', index=False)
    conn.close()
    
    # Allow user to type in the name of the movie
    movie_title = st.text_input("Type in the name of a movie you liked:")
    
    if st.button("Get Recommendations"):
        if movie_title:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Query movie data from database
            cursor.execute("SELECT * FROM movies WHERE title=?", (movie_title,))
            movie_data = cursor.fetchone()
            
            if movie_data:
                similar_movies_df = get_similar_movies(movie_title, user_item_matrix, cosine_sim)
                st.write("Recommended Movies and Similarity Scores:")
                st.write(similar_movies_df)
            else:
                st.write("Movie not found. Please try another movie.")
            
            conn.close()
        else:
            st.write("Please type in the name of a movie.")

if __name__ == '__main__':
    main()
