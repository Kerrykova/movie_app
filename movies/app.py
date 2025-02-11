from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from random import *
import pandas as pd
import movies.movie_prediction as mp

u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code', '#_ratings', 'RMSE']
users = pd.read_csv('matrix_factorization/user_data.csv').drop("Unnamed: 0",axis=1)
# print(list(users["user_id"].values))

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    # u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code', '#_ratings', 'RMSE']
    # users = pd.read_csv('matrix_factorization/user_data.csv').drop("Unnamed: 0",axis=1)
    # print(list(users["user_id"].values))
    if request.method == "GET":
        user_id = randint(1,948)
        user_data = mp.user_data(user_id)
        user_rec = mp.top5rec(user_id)
        return render_template("index.html", user_data=user_data, user_rec=user_rec)

    if request.method == "POST":
        user_id = request.form["userId"]
        if user_id in list(users["user_id"].values.astype(str)):
            user_data = mp.user_data(user_id)
            user_rec = mp.top5rec(user_id)
            return render_template("index.html", user_data=user_data, user_rec=user_rec)
        else:
            return render_template("error.html")

@app.route("/rate")
def rate_movies():
    movies = pd.read_csv("data/ml-20m/movies.csv")
    movie_list = []
    genres =[]
    for i,movie in enumerate(movies.values):
        movie_data = {
            "movie_id": movie[0],
            "movie_title": movie[1],
            "genre": movie[2],
        }
        movie_genre = movie[2].split("|")
        for genre in movie_genre:
            if genre not in genres:
                genres.append(genre)
        movie_list.append(movie_data)
    print(genres)

    return render_template("rate.html", movies_list = movie_list, genres_list = genres)

@app.route("/new_movies")
def new_movies():
    movies = pd.read_csv("data/ml-20m/movies.csv")
    movie_list = []
    for i,movie in enumerate(movies.values):
        movie_data = {
            "movie_id": movie[0],
            "movie_title": movie[1],
            "genre": movie[2],
        }
        movie_list.append(movie_data)
     
    return jsonify(movie_list)

@app.route("/movies")
def movies():
    i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
    'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
    'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']


    items = pd.read_csv("matrix_factorization/data/ml-100k/u.item", sep='|', names=i_cols,
    encoding='latin-1')

    items_dict = []
    for i,row in enumerate(items.values):
        movie = {
            "movie_id": row[0],
            "movie_title": row[1],
            "release_date": row[2],
            "IMDb_URL": row[4]
        }
        items_dict.append(movie)

    return jsonify(items_dict)

@app.route("/movies/recommended/<user_id>")
def movie_rec(user_id):
    rec_movies = mp.top5rec(user_id)

    return jsonify(rec_movies)

@app.route("/user/<user_id>")
def user_data(user_id):
    user_dict = mp.user_data(user_id)

    return jsonify(user_dict)



if __name__ == "__main__":
    app.run()
