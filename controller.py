from autogen.openapi_server import models
from flask import abort
from config import OPENAPI_AUTOGEN_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME
import sys
import requests
import pymysql as mysql

sys.path.append(OPENAPI_AUTOGEN_DIR)

base_url = "https://api.themoviedb.org/3/movie"
tmdb_key = "74324e8ddeedfdab7f79715a3ed8da98"
themoviedb_key = "b5c1777f2517bee552407c1bbcd8dbfa"


def db_cursor():
    return mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME).cursor()


def get_movies():
    with db_cursor() as cs:
        cs.execute("""
            SELECT m.id, m.title, m.release_date, m.genre
            FROM Movies m
            """)
        result = [models.MovieShort(*row) for row in cs.fetchall()]
    if result:
        return result
    else:
        abort(404)

def get_movies_details_id(movie_id):
    url = f"{base_url}/{movie_id}?api_key={themoviedb_key}"
    response = requests.get(url)
    r = {
        "title": response.json().get('title'),
        "budget": response.json().get('budget'),
        "revenue": response.json().get('revenue'),
        "release_date": response.json().get('release_date'),
        "genres": response.json().get('genres'),
        "production_companies": response.json().get('production_companies')
    }
    return r

def get_movies_latest():
    with db_cursor() as cs:
        cs.execute("""
            SELECT m.id, m.title, m.release_date, m.genre
            FROM Movies m
            ORDER BY m.release_date desc
            LIMIT 30
            """)
        result = [
            models.MovieShort(id, title, release_date, genre)
            for id, title, release_date, genre in cs.fetchall()
        ]
        return result

def get_movies_average_rating():
    return