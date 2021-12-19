import streamlit as st
import pandas as pd
import numpy as np
import ast
import pickle
import requests


# loading the movies list
movies = pickle.load(open('./movie_list.pkl', 'rb'))

# loading the model

similarity = pickle.load(open('./similarity.pkl', 'rb'))

# fetch posters

# fetch images for the corresponding movies


def fetchposter(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# recommendation algo

def recommendmovie(movie):

    get_index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[get_index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for index in distances[1:6]:

        movie_id = movies.iloc[index[0]].movie_id
        recommended_movie_posters.append(fetchposter(movie_id))
        recommended_movie_names.append(movies.iloc[index[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.title('Movie Recommender system')


movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Recommend Movies'):
    recommended_movie_names, recommended_movie_posters = recommendmovie(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
