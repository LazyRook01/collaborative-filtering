import streamlit as st

st.title("FilmFinder")
tab_recommend, tab_rate = st.tabs(["Recommendations","Update"])

with tab_recommend:
    st.title("Recommend a Movie")


with tab_rate:
    st.title("Rate a Movie")


