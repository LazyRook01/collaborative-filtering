# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load data
@st.cache
def load_data():
    movies = pd.read_parquet('movies.parquet')
    ratings = pd.read_parquet('ratings.parquet')
    return movies, ratings

# Merge data and perform collaborative filtering
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

# Recommend movies based on user input
def recommend_movie(movie_title, user_item_matrix, cosine_sim):
    # Get the index of the movie
    movie_index = user_item_matrix.columns.get_loc(movie_title)
    
    # Get similarity scores with other movies
    sim_scores = list(enumerate(cosine_sim[movie_index]))
    
    # Sort movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the top 10 similar movies
    top_similar_movies = sim_scores[1:11]
    
    # Get movie titles and similarity scores
    movie_titles = [user_item_matrix.columns[i[0]] for i in top_similar_movies]
    similarity_scores = [i[1] for i in top_similar_movies]
    
    return movie_titles, similarity_scores


# Main function
def main():
    st.title("FilmFinder - Recommendations")
    
    # Load data
    movies, ratings = load_data()
    
    # Collaborative filtering
    user_item_matrix, cosine_sim = collaborative_filtering(movies, ratings)
    
    # Select a movie
    movie_title = st.selectbox("Select a movie you liked:", user_item_matrix.columns)
    
    if st.button("Get Recommendations"):
        recommendations, similarity_scores = recommend_movie(movie_title, user_item_matrix, cosine_sim)
        st.write("Recommended Movies and Similarity Scores:")
        for movie, score in zip(recommendations, similarity_scores):
            st.write(f"Movie: {movie}, Similarity Score: {score}")


if __name__ == '__main__':
    main()
