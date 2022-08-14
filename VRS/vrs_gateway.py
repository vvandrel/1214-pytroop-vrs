from flask import Flask, request, jsonify
from flask_restful import Api
from vrs_movie_data import MovieData
import vrs_dataset as vrs_ds
import vrs_ml_model as vrs_ml
import vrs_recommendation as vrs_rec
import vrs_utils as vrs_utils

app = Flask(__name__)
api = Api(app)


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
    movie = vrs_utils.create_movie_data_from_json(movie, content)
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
        movies_list = vrs_utils.create_movies_list_from_df(df)
    return jsonify(movies_list)


def vrs_gateway_run(host='0.0.0.0', port=8181, debug=False):
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    vrs_gateway_run()
