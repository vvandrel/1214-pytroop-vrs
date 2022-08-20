from flask import Flask, request, jsonify
from flask_restful import Api
from vrs_movie_data import MovieData
from vrs_utils import log
import vrs_dataset as vrs_ds
import vrs_ml_model as vrs_ml
import vrs_recommendation as vrs_rec
import vrs_utils as vrs_utils


__module = '[VRS-GATEWAY]'

app = Flask(__name__)
api = Api(app)


@app.route('/vrs/dataset/<customer_id>')
def get_movies(customer_id):
    log(__module, customer_id, 'Getting movies from ' + customer_id + ' dataset ... ')
    params = {}
    for counter, arg in enumerate(request.args):
        params[arg] = request.args.get(arg)
        log(__module, customer_id, ' =====> Param ' + counter + ' ' + arg + ': ' + request.args.get(arg))
    df = vrs_ds.find_all(customer_id, params)
    log(__module, customer_id, '  =====> Found: ' + str(len(df)) + ' records')
    json_result = df.to_json(orient='records')
    return json_result


@app.route('/vrs/dataset/<customer_id>/<movie_id>')
def get_movie(customer_id, movie_id):
    log(__module, customer_id, 'Getting movie id ' + str(movie_id) + ' from ' + customer_id + ' dataset ... ')
    df = vrs_ds.find_by_id(customer_id, int(movie_id))
    log(__module, customer_id, '  =====> Found: ' + str(len(df)) + ' record')
    json_result = df.to_json(orient='records')
    return json_result


@app.route('/vrs/dataset/<customer_id>/save', methods=['POST'])
def save_movie(customer_id):
    log(__module, customer_id, 'Posting (saving) a movie into ' + customer_id + ' dataset ... ')
    content = request.json
    movie = MovieData()
    movie = vrs_utils.create_movie_data_from_json(movie, content)
    log(__module, customer_id, '  =====> ' + str(movie))
    response = vrs_ds.save(customer_id, movie)
    log(__module, customer_id, '  =====> ' + str(response), 'ERROR' if response.result_code != 1 else 'INFO')
    return response.__dict__


@app.route('/vrs/dataset/<customer_id>/<movie_id>/del')
def del_movie(customer_id, movie_id):
    log(__module, customer_id, 'Deleting movie id: ' + str(movie_id) + ' from ' + customer_id + ' dataset ... ')
    response = vrs_ds.delete(customer_id, int(movie_id))
    log(__module, customer_id, '  =====> ' + str(response), 'ERROR' if response.result_code != 1 else 'INFO')
    return response.__dict__


@app.route('/vrs/model/<customer_id>/create')
def create_ml_model(customer_id):
    log(__module, customer_id, 'Creating ML Model to ' + customer_id + ' ... ')
    response = vrs_ml.create_ml_model(customer_id)
    log(__module, customer_id, '  =====> ' + str(response), 'ERROR' if response.result_code != 1 else 'INFO')
    return response.__dict__


@app.route('/vrs/recommendation/<customer_id>/<movie_title>')
def get_movies_recommendation(customer_id, movie_title):
    log(__module, customer_id, 'Getting Movies Recommendation. Movie Title: ' + movie_title + ' ... ')
    movies_list = []
    df = vrs_rec.get_recommendation(customer_id, movie_title)
    if len(df) > 0:
        movies_list = vrs_utils.create_movies_list_from_df(df)
    log(__module, customer_id, '  =====> Recommendations found: ' + str(len(df)))
    return jsonify(movies_list)


def vrs_gateway_run(host='0.0.0.0', port=8181, debug=False):
    log(__module, 'VRS', 'Starting ... ')
    app.run(host=host, port=port, debug=debug)
    log(__module, 'VRS', 'Shutdown')


if __name__ == '__main__':
    vrs_gateway_run()
