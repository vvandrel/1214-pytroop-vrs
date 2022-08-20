from vrs_movie_data import MovieData, MovieKeywords, MovieGenre
from datetime import datetime


def get_date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log(module, customer_id, description, level='INFO'):
    _level = 'UNKNOWN' if level != 'INFO' and level != 'WARN' and level != 'ERROR' else level
    print(f'{get_date()} :: {module} :: [{customer_id}] :: [{_level}] :: {description}')


def get_movie_keywords_from_json(keywords_js):
    lst_keyw = []
    for keyword in keywords_js:
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
