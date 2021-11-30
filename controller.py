import msilib

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
            SELECT id, imdb_id, title, release_date, genres
            FROM movie
            """)
        result = []
        for i in cs.fetchall():
            genres = []
            j = list(eval(i[4]))
            for k in j:
                genres.append(models.Genre(k['id'], k['name']))
            result.append(models.MovieShort(i[0], i[1], i[2], i[3], genres))
        if result:
            return result
        else:
            abort(404)


def get_movies_details_id(imdb_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT id, imdb_id, title, release_date, cast, genres, production_companies
            FROM movie 
            WHERE imdb_id=%s
            """, [imdb_id])
        result = []
        for i in cs.fetchall():
            genres = []
            g = list(eval(i[4]))
            for j in g:
                genres.append(models.Genre(j['id'], j['name']))
            cast = []
            c = list(eval(i[5]))
            for j in c:
                cast.append(models.Person(j['id'], j['name']))
            company = []
            p = list(eval(i[6]))
            for j in p:
                company.append(models.ProductionCompany(j['id'], j['name']))
            result.append(models.Movie(i[0], i[1], i[2], i[3], genres, cast, company))
        if result:
            return result
        else:
            abort(404)


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
