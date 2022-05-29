import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_option_menu import option_menu


#function to fetch the poster using tmdb api call
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        print(data)
        return full_path
    else:
        full_path = "https://www.hifi-zubehoer.shop/sites/hifi2020/public/_v1_/images/no-image-en.png"
        return full_path

#function to get the recommendations which have the movie titles and the posters
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:16]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movie_posters


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
#creating a dataframe from the dictionary
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


with st.sidebar:
    selected = option_menu(None, ["Trending", "Search"],
                            icons = ['tv-fill', 'search'],
                            menu_icon = "cast", default_index = 0, orientation = "horizontal",
                            styles =
                           {
                                "container": {"padding": "0!important", "background-color": "#000"},
                                "icon": {"color": "red", "font-size": "25px"},
                                "nav-link": {"font-size": "28px", "text-align": "left", "margin": "0px", "--hover-color": "#7b7a79"},
                                "nav-link-selected": {"background-color": "#a1a09f"},
                           }
                           )

if selected == "Trending":
    st.markdown("<h1 style='text-align: center; color: red; font-size: 60px;'>Top 10 Trending Movies</h1>", unsafe_allow_html=True)
    st.markdown('##')
    st.markdown('##')
    trending_list = [{"name" : "Minions", "poster" : "https://image.tmdb.org/t/p/w500/AfYGGvHufd8cIosTvBtnzUExxe4.jpg"},
                     {"name" : "Interstellar", "poster" : "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"},
                     {"name" : "Deadpool", "poster" : "https://image.tmdb.org/t/p/w500/fSRb7vyIP8rQpL0I47P3qUsEKX3.jpg"},
                     {"name" : "Guardians of the Galaxy", "poster" : "https://image.tmdb.org/t/p/w500/kFWLxUwcSpiLzszZbxUIZT9g6WR.jpg"},
                     {"name" : "Mad Max: Fury Road", "poster" : "https://image.tmdb.org/t/p/w500/cNzCJnG4wstosen59BhydnUkaZJ.jpg"},
                     {"name" : "Jurassic World", "poster" : "https://image.tmdb.org/t/p/w500/jcUXVtJ6s0NG0EaxllQCAUtqdr0.jpg"},
                     {"name" : "Pirates of the Caribbean: The Curse of the Black Pearl", "poster" : "https://image.tmdb.org/t/p/w500/z8onk7LV9Mmw6zKz4hT6pzzvmvl.jpg"},
                     {"name" : "Dawn of the Planet of the Apes", "poster" : "https://image.tmdb.org/t/p/w500/kScdQEwS9jPEdnO23XjGAtaoRcT.jpg"},
                     {"name" : "The Hunger Games: Mockingjay - Part 1", "poster" : "https://image.tmdb.org/t/p/w500/4FAA18ZIja70d1Tu5hr5cj2q1sB.jpg"},
                     {"name" : "Big Hero 6", "poster" : "https://image.tmdb.org/t/p/w500/2mxS4wUimwlLmI1xp6QW6NSU361.jpg"}]

    for i in range(0,len(trending_list)):
        st.subheader(str(i+1) + ". " +trending_list[i]["name"])
        st.image(trending_list[i]["poster"], None, 256)
        st.markdown('##')


if selected == "Search":
    st.markdown("<h1 style='text-align: center; color: red; font-size: 60px;'>Movie Recommender</h1>", unsafe_allow_html=True)
    st.markdown('##')
    st.markdown('##')

    # displaying the search bar
    selected_movie = st.selectbox(
        'Search your favourite movies!',
        movies['title'].values)

    # to display the recommended movies
    if st.button("Recommend"):
        st.markdown('##')
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        n_cols = 4
        n_rows = 4
        rows = [st.container() for _ in range(n_rows)]
        cols_per_row = [r.columns(n_cols) for r in rows]
        cols = [column for row in cols_per_row for column in row]

        for i in range(0, 16):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])







