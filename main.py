import streamlit as st
from tab_recommend import show_recommend_tab
from tab_update import show_update_tab
from createdatabase import show_create_database_tab

st.title("🎬🎥🍿FilmFinder🎦📽️")
st.divider()
st.subheader("Developed By Gaurav Ojha")
st.write("This app demonstrates collaborative filtering and MLOps techniques for movie recommendation.")
st.write("Powered by several algorithms, it suggests personalized movie recommendations based on user preferences.")
st.write("Contact me by email: ojhagaurav36@gmail.com")
st.divider()

tab_recommend, tab_rate, tab_create = st.columns(3)
tab1, tab2, tab3 = st.tabs(["Create", "Update", "Recommendations"])

with tab3:
    show_recommend_tab()

with tab2:
    show_update_tab()

with tab1:
    show_create_database_tab()
