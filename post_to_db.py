import csv
from operator import itemgetter

import requests

base_url = "https://api.themoviedb.org/3"
api_key = "b5c1777f2517bee552407c1bbcd8dbfa"
movies, companies, persons = [], [], []
keys = ["id", "title", "genres", "release_date", "imdb_id", "cast", "production_companies"]


def get_movies_by_year(y):
    global movies, companies, persons, keys
    params = {
        "api_key": api_key,
        "primary_release_year": y,
        'region': "TH"
    }
    this_file = open(f'movie_{y}.csv', 'w', encoding='utf-8', newline="")
    dict_writer = csv.DictWriter(this_file, keys)
    response = requests.get(f"{base_url}/discover/movie?page={1}", params=params)
    page = int(response.json()['total_pages'])
    for i in range(1, page + 1):
        response = requests.get(f"{base_url}/discover/movie?page={i}", params=params)
        result = response.json().get("results")
        for j in result:
            detail = requests.get(f"{base_url}/movie/{j['id']}?api_key={api_key}").json()
            if detail["imdb_id"] is None or detail["imdb_id"] == "":
                pass
            else:
                cast = requests.get(f"{base_url}/movie/{j['id']}/credits?api_key={api_key}").json()
                movie = {
                    "id": int(detail["id"]),
                    "title": detail["title"],
                    "genres": {"genre": detail["genres"]},
                    "release_date": detail["release_date"],
                    "imdb_id": detail["imdb_id"],
                    "cast": {"cast": cast["cast"]},
                    "production_companies": {"production_company": detail["production_companies"]}
                }
                movies.append(movie)
                dict_writer.writerow(movie)

                for c in cast["cast"]:
                    persons.append({
                        "id": int(c["id"]),
                        "name": c["name"]
                    })

                for k in detail["production_companies"]:
                    companies.append({
                        "id": int(k['id']),
                        "name": k["name"]
                    })


if __name__ == '__main__':
    for r in range(5):
        year = 2021 - r
        get_movies_by_year(year)
    with open(f'movie.csv', 'w', encoding='utf-8', newline="") as my_file:
        writer = csv.DictWriter(my_file, keys)
        for m in movies:
            writer.writerow(m)

    sorted_movies = sorted(movies, key=itemgetter('title'))
    with open(f'movie_title.csv', 'w', encoding='utf-8', newline="") as my_file:
        for m in sorted_movies:
            my_file.writelines(f"{m['title']}\n")

    res_list = [i for n, i in enumerate(persons) if i not in persons[n + 1:]]
    with open(f'persons.csv', 'w', encoding='utf-8', newline="") as my_file:
        writer = csv.DictWriter(my_file, ['id', 'name'])
        for p in res_list:
            writer.writerow(p)

    res_list = [i for n, i in enumerate(companies) if i not in companies[n + 1:]]
    with open(f'production_companies.csv', 'w', encoding='utf-8', newline="") as my_file:
        writer = csv.DictWriter(my_file, ['id', 'name'])
        for c in res_list:
            writer.writerow(c)
