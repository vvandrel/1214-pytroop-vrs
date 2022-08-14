from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from vrs_movie_data import MovieData, MovieKeywords, MovieGenre, MovieCastData
import vrs_dataset as vrs_ds
import vrs_ml_model as vrs_ml
import vrs_recommendation as vrs_rec

app = Flask(__name__)
api = Api(app)


def get_movie_keywords_from_json(keywords_js):
    lst_keyw = []
    for keyword in keywords_js:
        print(keyword)
        mv_keyw = MovieKeywords()
        mv_keyw.id = keyword['id']
        mv_keyw.name = keyword['name']
        lst_keyw.append(mv_keyw.__dict__)
    return str(lst_keyw)


def get_movie_genres_from_json(genres_js):
    lst_genre = []
    for genre in genres_js:
        mv_genre = MovieGenre()
        mv_genre.id = genre['id']
        mv_genre.name = genre['name']
        lst_genre.append(mv_genre.__dict__)
    return str(lst_genre)


def get_movie_cast_from_json(cast_js):
    lst_cast = []

    for cast in cast_js:
        mv_cast = MovieGenre()
        mv_cast.id = cast['id']
        mv_cast.name = cast['name']
        mv_cast.cast_id = cast['cast_id']
        mv_cast.character = cast['character']
        mv_cast.credit_id = cast['credit_id']
        mv_cast.gender = cast['gender']
        mv_cast.order = cast['order']
        lst_cast.append(mv_cast.__dict__)
    return str(lst_cast)


def create_movie_data_from_json(mv, json_content):
    mv.id = json_content['id']
    mv.title = json_content['title']
    mv.overview = json_content['overview']
    mv.keywords = get_movie_keywords_from_json(json_content['keywords'])
    mv.genres = get_movie_genres_from_json(json_content['genres'])
    mv.original_language = json_content['original_language']
    mv.director = json_content['director']
    mv.cast = get_movie_cast_from_json(json_content['cast'])
    mv.status = json_content['status']
    return mv


def create_movies_list_from_df(df):
    movies_list = []
    df = df.reset_index()  # make sure indexes pair with number of rows
    for index, row in df.iterrows():
        mv = MovieData()
        mv.id = row['id']
        mv.title = row['title']
        mv.overview = row['overview']
        # mv.keywords = get_movie_keywords_from_json(json_content['keywords'])
        # mv.genres = get_movie_genres_from_json(json_content['genres'])
        mv.original_language = row['original_language']
        mv.director = row['director']
        # mv.cast = get_movie_cast_from_json(json_content['cast'])
        mv.status = row['status']
        movies_list.append(mv.__dict__)
    return movies_list


@app.route('/vrs/dataset/<customer_id>')
def get_movies(customer_id):
    params = {}
    for counter, arg in enumerate(request.args):
        params[arg] = request.args.get(arg)
        print(f'Param {counter}: {arg}: {request.args.get(arg)}')
    df = vrs_ds.find_all(customer_id, params)
    json_result = df.to_json(orient='records')
    return json_result


@app.route('/vrs/dataset/<customer_id>/<movie_id>')
def get_movie(customer_id, movie_id):
    df = vrs_ds.find_by_id(customer_id, int(movie_id))
    json_result = df.to_json(orient='records')
    return json_result


@app.route('/vrs/dataset/<customer_id>/save', methods=['POST'])
def save_movie(customer_id):
    # if request.method == 'POST':
    content = request.json
    movie = MovieData()
    movie = create_movie_data_from_json(movie, content)
    response = vrs_ds.save(customer_id, movie)
    return response.__dict__


@app.route('/vrs/dataset/<customer_id>/<movie_id>/del')
def del_movie(customer_id, movie_id):
    response = vrs_ds.delete(customer_id, int(movie_id))
    return response.__dict__


@app.route('/vrs/model/<customer_id>/create')
def create_ml_model(customer_id):
    response = vrs_ml.create_ml_model(customer_id)
    return response.__dict__


@app.route('/vrs/recommendation/<customer_id>/<movie_title>')
def get_movies_recommendation(customer_id, movie_title):
    movies_list = []
    df = vrs_rec.get_recommendation(customer_id, movie_title)
    if len(df) > 0:
        movies_list = create_movies_list_from_df(df)
    return jsonify(movies_list)


def vrs_gateway_run(host='0.0.0.0', port=8181, debug=False):
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    vrs_gateway_run()
