import csv

import requests

BASE_URL = "https://imdb-api.com/en"
API_KEY = ["k_zwp5i4yu",
           "k_p7h75hc0",
           "k_pu9wbz8u",
           "k_q514guzp",
           "k_2uzksic3",
           "k_21f13b32",
           "k_33j1rc5f",
           "k_z218xks1",
           "k_jme3zq72",
           "k_x8130z3o",
           "k_0fquph46"]


def get_movie_rating(imdb_id):
    for API in API_KEY:
        response = requests.get(f"{BASE_URL}/API/Ratings/{API}/{imdb_id}").json()
        if response['errorMessage'] == '':
            break
    imDb = response['imDb']
    metacritic = response['metacritic']
    theMovieDb = response['theMovieDb']
    if imDb == '':
        imDb = 0
    if metacritic == '':
        metacritic = 0
    if theMovieDb == '':
        theMovieDb = 0
    return {
        "imdb_id": imdb_id,
        "title": response['title'],
        "imDb": imDb,
        "metacritic": metacritic,
        "theMovieDb": theMovieDb
    }


if __name__ == '__main__':
    keys = ['imdb_id', 'title', 'imDb', 'metacritic', 'theMovieDb']
    with open("movie_imdb.csv", encoding='utf-8') as file:
        data_list = file.readlines()
        with open('movie_rating.csv', 'w', encoding='utf-8', newline="") as my_file:
            writer = csv.DictWriter(my_file, keys)
            i = 1
            for data in data_list:
                result = get_movie_rating(data.strip('\n'))
                writer.writerow(result)
                print(i, result)
                i += 1
