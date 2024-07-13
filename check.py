import os

import requests
from dotenv import load_dotenv

load_dotenv("data.env")


def search_movie(movie_title):
    header ={
        "Authorization":f'Bearer {os.getenv('api_key')}',
        "accept": "application/json"
    }

    # respone = requests.get("https://api.themoviedb.org/3/authentication", headers=header)
    # respone.raise_for_status()


    params = {
        "query": movie_title
    }

    response2 = requests.get("https://api.themoviedb.org/3/search/movie", params=params, headers=header)
    response2.raise_for_status()

    list_of_movie = []
    for movie in response2.json()['results']:
        if movie["release_date"] != "" and movie['poster_path']:
            year = movie["release_date"][0:4]
            url = os.getenv('image_path') + movie['poster_path']
            touple = (movie['title'], year, url, movie['overview'])
            list_of_movie.append(touple)

    return list_of_movie

