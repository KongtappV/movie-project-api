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
    response = requests.get(f"{BASE_URL}/API/Ratings/{API_KEY[0]}/{imdb_id}").json()
    return {
        "imdb_id": imdb_id,
        "title": response['title'],
        "imDb": response['imDb'],
        "metacritic": response['metacritic'],
        "theMovieDb": response['theMovieDb'],
        "rottenTomatoes": response['rottenTomatoes'],
        "tV_com": response['tV_com'],
        "filmAffinity": response['filmAffinity'],
        "errorMessage": response['errorMessage']
    }


if __name__ == '__main__':
    print(get_movie_rating("tt1477834"))
