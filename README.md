Movie Review
================

### Members

| Members | StudentID | Github |
| :---: | :---: | :---: |
| Chonchanok	Chevaisrakul | 6210545459 | [KongtappV](https://github.com/KongtappV) |
| Narawish 	Sangsiriwut     | 6210545971 | [NarawishS](https://github.com/NarawishS) |
| Kongtapp 	Veerawattananun     | 6210546374 | [boom210232](https://github.com/boom210232) |

### Project description

this project is for searching movies with specific genre/company/year/cast and reviews scores from various critics from
API and Questionnaires

### Project requirement

| Name | Version | Description |
| :---: | :---: | :---: |
|Python  | 3.7 and above | Use for running APIs.|
| Pip| 21 or later| Use for installing extra extension for Python|
|Java|8 or above|for executing jar file|
|Nodejs|lastest|for executing graphql|

install OpenAPI-to-GraphQL
```commandline
npm install -g openapi-to-graphql-cli@2.5.0
```

### Data Collection

#### Primary Data

- [Questionnaire provided by Google Form](https://docs.google.com/forms/d/e/1FAIpQLSeowh_YJuN-eWCO2ahBSGyoyLNL8E78wraUG2INRLrgP50RrA/viewform)
#### Secondary data
- [The Movie Database(TMDB)](https://www.themoviedb.org/documentation/api)
- [Internet Movie Database](https://imdb-api.com/swagger/index.html)
- [Metacritic API](https://www.internetvideoarchive.com/apis/metacritic-api/)

#### Get started

Before starting the process, Create a virtual environment using these command

For MacOS and Linux

```commandline
python -m venv env
```

```commandline
. env/bin/activate
```

For Windows<br>
create environment

```commandline
python -m venv env
```

activate env

```commandline
env\Scripts\activate
```

Create autogen

For mac linux and windows
```commandline
java -jar .\openapi\openapi-generator-cli-5.3.0.jar generate -i .\openapi\movie-api.yaml -o autogen -g python-flask
```

download requirements

```commandline
python -m pip install -r requirements.txt
```

start app

```commandline
python app.py
```

open another terminal and run

For mac linux and windows
```commandline
openapi-to-graphql --cors -u http://localhost:8080/movie-api/v1 openapi/movie-api.yaml
```

swagger ui

```
http://localhost:8080/movie-api/v1/ui/#
```

visualize graph open file `html/avg-review.html` on your preferred browser
