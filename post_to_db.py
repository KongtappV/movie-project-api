import csv
import requests

base_url = "https://api.themoviedb.org/3"
api_key = "b5c1777f2517bee552407c1bbcd8dbfa"


def get_movies_by_year(year):
    params = {
        "api_key": api_key,
        "primary_release_year": year,
        'region': "TH"
    }
    movies = []
    response = requests.get(f"{base_url}/discover/movie?page={1}", params=params)
    page = int(response.json()['total_pages'])
    for i in range(1, page):
        response = requests.get(f"{base_url}/discover/movie?page={i}", params=params)
        result = response.json().get("results")
        for j in result:
            detail = requests.get(f"{base_url}/movie/{j['id']}?api_key={api_key}").json()
            cast = requests.get(f"{base_url}/movie/{j['id']}/credits?api_key={api_key}").json()
            mi = {
                "id": int(detail["id"]),
                "title": detail["title"],
                "genres": {"genre": detail["genres"]},
                "release_date": detail["release_date"],
                "imdb_id": detail["imdb_id"],
                "cast": {"cast": cast["cast"]},
                "production_companies": {"production_company": detail["production_companies"]}
            }
            movies.append(mi)
    return movies


if __name__ == '__main__':
    for y in range(5):
        with open(f'movie_{2021 - y}.csv', 'w', encoding='utf-8', newline="") as my_file:
            m_list = get_movies_by_year(2021 - y)
            keys = m_list[0].keys()
            writer = csv.DictWriter(my_file, keys)
            # writer.writeheader()
            for m in m_list:
                writer.writerow(m)
