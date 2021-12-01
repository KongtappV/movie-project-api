from autogen.openapi_server import models
from flask import abort
from config import OPENAPI_AUTOGEN_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME
import sys
import pymysql as mysql

sys.path.append(OPENAPI_AUTOGEN_DIR)


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


def get_movie_details_id(imdb_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT id, imdb_id, title, release_date, cast, genres, production_companies
            FROM movie 
            WHERE imdb_id=%s
            """, [imdb_id])
        i = cs.fetchone()
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
        result = models.Movie(i[0], i[1], i[2], i[3], genres, cast, company)
    if result:
        return result
    else:
        abort(404)


def get_movies_latest():
    with db_cursor() as cs:
        cs.execute("""
            SELECT m.id, m.imdb_id, m.title, m.release_date, m.genres
            FROM movie m
            ORDER BY m.release_date desc
            LIMIT 30
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


def get_movie_rating(imdb_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT r.imdb_id, r.title, r.imDb, r.metacritic, r.theMovieDb
            FROM rating r
            WHERE r.imdb_id = %s
            """, [imdb_id])
        return models.Rating(*cs.fetchone())


def get_movie_average_rating_id(imdb_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT r.imdb_id, r.title, (r.imdb + r.metacritic + r.theMovieDb)/3 as average_rating
            FROM rating r
            WHERE r.imdb_id = %s
            """, [imdb_id])
        return models.AverageRating(*cs.fetchone())

def get_movie_average_rating():
    with db_cursor() as cs:
        cs.execute("""
            SELECT r.imdb_id, r.title, (r.imdb + r.metacritic + r.theMovieDb)/3 as average_rating
            FROM rating r
            """)
        result = [
            models.AverageRating(imdb_id, title, average_rating)
            for imdb_id, title, average_rating in cs.fetchall()
        ]
        return result

def get_movie_average_rating_limit(limit):
    with db_cursor() as cs:
        cs.execute("""
            SELECT r.imdb_id, r.title, (r.imdb + (r.metacritic/10) + r.theMovieDb)/3 as average_rating
            FROM rating r
            ORDER BY r.title
            LIMIT %s
            """, [limit])
        result = [
            models.AverageRating(imdb_id, title, average_rating)
            for imdb_id, title, average_rating in cs.fetchall()
        ]
        return result

def get_movie_review(imdb_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT r.movie_name, r.recommend, r.score, r.review
            FROM review r
            INNER JOIN movie m ON r.movie_name=m.title
            WHERE m.imdb_id = %s
            """, [imdb_id])
        result = [
            models.Reviews(movie_name, recommend, score, review)
            for movie_name, recommend, score, review in cs.fetchall()
        ]
        return result


def get_movies_average_review():
    with db_cursor() as cs:
        cs.execute("""
            SELECT m.imdb_id, r.movie_name, COUNT(r.recommend) as total_count,(SUM((CASE WHEN r.recommend = "Yes" THEN 1 ELSE 0 END))/COUNT(r.recommend))*100 as recommend, AVG(r.score) as avg_score
            FROM review r INNER JOIN movie m ON m.title = r.movie_name
            GROUP BY r.movie_name
            """)
        result = [
            models.AverageReview(imdb_id, movie_name, total_count, recommend, avg_score)
            for imdb_id, movie_name, total_count, recommend, avg_score in cs.fetchall()
        ]
        return result


def get_movies_average_review_limit(limit):
    with db_cursor() as cs:
        cs.execute("""
            SELECT m.imdb_id, r.movie_name, COUNT(r.recommend) as total_count,(SUM((CASE WHEN r.recommend = "Yes" THEN 1 ELSE 0 END))/COUNT(r.recommend))*100 as recommend, AVG(r.score) as avg_score
            FROM review r INNER JOIN movie m ON m.title = r.movie_name
            GROUP BY r.movie_name
            ORDER BY r.movie_name
            LIMIT %s
            """, [limit])
        result = [
            models.AverageReview(imdb_id, movie_name, total_count, recommend, avg_score)
            for imdb_id, movie_name, total_count, recommend, avg_score in cs.fetchall()
        ]
        return result


def get_movies_average_review_id(imbd_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT m.imdb_id, r.movie_name, COUNT(r.recommend) as total_count,(SUM((CASE WHEN r.recommend = "Yes" THEN 1 ELSE 0 END))/COUNT(r.recommend))*100 as recommend, AVG(r.score) as avg_score
            FROM review r INNER JOIN movie m ON m.title = r.movie_name
            WHERE m.imdb_id = %s
            GROUP BY r.movie_name
            """, [imbd_id])
        i = cs.fetchone()
        result = models.AverageReview(*i)
        return result


def get_movies_cast(cast_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT id, imdb_id, title, release_date, genres, cast
            FROM movie
        """)
        result = []
        for i in cs.fetchall():
            cast = list(eval(i[5]))
            for c in cast:
                if c['id'] == cast_id:
                    genres = []
                    j = list(eval(i[4]))
                    for k in j:
                        genres.append(models.Genre(k['id'], k['name']))
                    result.append(models.MovieShort(i[0], i[1], i[2], i[3], genres))
        if result:
            return result
        else:
            abort(404)


def get_movies_company(company_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT id, imdb_id, title, release_date, genres, production_companies
            FROM movie
        """)
        result = []
        for i in cs.fetchall():
            company = list(eval(i[5]))
            for c in company:
                if c['id'] == company_id:
                    genres = []
                    j = list(eval(i[4]))
                    for k in j:
                        genres.append(models.Genre(k['id'], k['name']))
                    result.append(models.MovieShort(i[0], i[1], i[2], i[3], genres))
        if result:
            return result
        else:
            abort(404)


def get_movies_genre(genre_id):
    with db_cursor() as cs:
        cs.execute("""
            SELECT id, imdb_id, title, release_date, genres
            FROM movie
        """)
        result = []
        for i in cs.fetchall():
            is_category = False
            genres = []
            g = list(eval(i[4]))
            for k in g:
                if k['id'] == genre_id:
                    is_category = True
                genres.append(models.Genre(k['id'], k['name']))
            if is_category:
                result.append(models.MovieShort(i[0], i[1], i[2], i[3], genres))
        if result:
            return result
        else:
            abort(404)


def get_genres():
    with db_cursor() as cs:
        cs.execute("""
            SELECT *
            FROM genre
        """)
        result = []
        for row in cs.fetchall():
            result.append(models.Genre(row[0], row[1]))
        if result:
            return result
        else:
            abort(404)


def get_companies():
    with db_cursor() as cs:
        cs.execute("""
            SELECT *
            FROM company
        """)
        result = []
        for row in cs.fetchall():
            result.append(models.ProductionCompany(row[0], row[1]))
        if result:
            return result
        else:
            abort(404)


def get_persons():
    with db_cursor() as cs:
        cs.execute("""
            SELECT *
            FROM person
        """)
        result = []
        for row in cs.fetchall():
            result.append(models.Person(row[0], row[1]))
        if result:
            return result
        else:
            abort(404)


def get_movie_year(year):
    with db_cursor() as cs:
        cs.execute("""
            SELECT m.id, m.imdb_id, m.title, m.release_date, m.genres
            FROM movie m
            WHERE YEAR(m.release_date)=%s
            """, [year])
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
