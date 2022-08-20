from vrs_movie_data import MovieData, MovieCastData, MovieKeywords, MovieGenre
from vrs_result_data import Result
import pandas as pd

__movie_data_test = MovieData()
__dataset_path = 'dataset/'
__file_ext = '.csv'


def get_dataset(customer_id):
    try:
        df = pd.read_csv(filepath_or_buffer=__dataset_path + customer_id + __file_ext)
    except FileNotFoundError as ex:
        print(f'get_dataset: error: {str(ex)}')
        df = pd.DataFrame()
    except Exception as e:
        print(f'get_dataset: error: {str(e)}')
        raise Exception("Sorry, no numbers below zero")
    return df


def save_dataset(customer_id, df):
    df.to_csv(path_or_buf=__dataset_path + customer_id + __file_ext,
              index=False)


def find_all(customer_id, movie_filters):
    # Get the dataset
    df_all = get_dataset(customer_id)
    if len(df_all) > 0:
        # Get Filters
        if 'id' in movie_filters:
            df_all = df_all[df_all["id"] == movie_filters['id']]
        else:
            if 'title' in movie_filters:
                df_all = df_all[df_all["title"].str.contains(movie_filters['title'])]
            if 'director' in movie_filters:
                df_all = df_all[df_all["director"].notnull()]
                df_all = df_all[df_all["director"].str.contains(movie_filters['director'])]
            if 'status' in movie_filters:
                df_all = df_all[df_all["status"] == movie_filters['status']]
    return df_all


def find_by_id(customer_id, movie_id):
    # Create the filter by id
    movie_filter = {"id": movie_id}
    # Get the dataset filtering by id
    df_by_id = find_all(customer_id, movie_filter)
    return df_by_id


def insert(customer_id, movie_data):
    response = Result()
    if type(movie_data) is type(__movie_data_test):
        print('Insert: Open the Dataset')
        df = get_dataset(customer_id)
        try:
            movie_data.id = 1
            if len(df) > 0:
                movie_data.id = 0 if pd.isna(df['id'].max()) else df['id'].max() + 1
            df_insert = pd.DataFrame(movie_data.__dict__, index=[0])
            df = pd.concat([df, df_insert])

            # Insert the record
            save_dataset(customer_id, df)
            response.set_result(1, 'Success')
            print(f'The record was inserted on {customer_id} dataset')
        except Exception as ex:
            print("Something went wrong when writing to the file: ", str(ex))
            response.set_result(0, 'Exception')
        finally:
            print('Close the Dataset')
            del df
    else:
        response.set_result(-1, 'Unknown movie data ype')
    return response


def update(customer_id, movie_data):
    response = Result()

    # Open Dataset
    print('Update: Open the Dataset')
    df_update = get_dataset(customer_id)

    # Check if the movie_id exists.
    idx = df_update.index[df_update['id'] == movie_data.id].tolist()
    if len(idx) > 0:
        try:
            idx = idx[0]

            # Update
            df_update.at[idx, 'title'] = movie_data.title

            # Save the dataset
            save_dataset(customer_id, df_update)

            # Response OK
            response.set_result(1, 'Success')
            print(f'The movie id {movie_data.id} was updated on {customer_id} dataset')
        except Exception as ex:
            print("Something went wrong when writing to the file: ", str(ex))
            response.set_result(0, 'Exception')
    else:
        response.set_result(-1, 'Movie not found')
    print('Close the Dataset')
    del df_update
    return response


def save(customer_id, movie_data):
    response = Result()
    movie_title = movie_data.title
    chk_movie = find_all(customer_id, {"title": movie_title})
    if movie_data.id <= 0:
        new_movie = False if len(chk_movie) > 0 else True
        if new_movie:
            response = insert(customer_id, movie_data)
        else:
            response.set_result(2, 'Movie already exists!')
    else:
        if len(chk_movie) > 0:
            if len(chk_movie) == 1:
                if movie_data.id != int(chk_movie['id'][0]):
                    response.set_result(2, 'Movie already exists with other id!')
                    return response
        response = update(customer_id, movie_data)
    return response


def delete(customer_id, movie_id):
    response = Result()

    # Open Dataset
    df_delete = get_dataset(customer_id)

    # Check if the movie_id exists.
    idx = df_delete.index[df_delete['id'] == movie_id].tolist()
    if len(idx) > 0:
        try:
            # Delete the movie
            df_delete.drop(idx, inplace=True)

            # Save the dataset
            save_dataset(customer_id, df_delete)

            # Response OK
            response.set_result(1, 'Success')
            print(f'The movie id {movie_id} was deleted on {customer_id} dataset')
        except Exception as ex:
            print("Something went wrong when writing to the file: ", str(ex))
            response.set_result(0, 'Exception')
    else:
        response.set_result(-1, 'Movie not found')
    print('Close the Dataset')
    del df_delete
    return response


if __name__ == '__main__':
    customer = 'companyABC'
    print(customer, ' :: test')
    mv = MovieData()
    mv.id = 1
    mv.title = 'Avengers'

    lst_cast = []
    mv_cast = MovieCastData()
    mv_cast.id = 1
    mv_cast.name = 'Vinicius'
    lst_cast.append(mv_cast.__dict__)

    mv_cast = MovieCastData()
    mv_cast.id = 2
    mv_cast.name = 'Vandre'
    lst_cast.append(mv_cast.__dict__)

    mv.cast = str(lst_cast)

    lst_keyw = []
    mv_keyw = MovieKeywords()
    mv_keyw.id = 1
    mv_keyw.name = 'culture shock'
    lst_keyw.append(mv_keyw.__dict__)

    mv_keyw = MovieKeywords()
    mv_keyw.id = 2
    mv_keyw.name = 'keywords test'
    lst_keyw.append(mv_keyw.__dict__)

    mv.keywords = str(lst_keyw)

    lst_genre = []
    mv_genre = MovieGenre()
    mv_genre.id = 1
    mv_genre.name = 'culture shock'
    lst_genre.append(mv_genre.__dict__)

    mv_genre = MovieGenre()
    mv_genre.id = 2
    mv_genre.name = 'keywords test'
    lst_genre.append(mv_genre.__dict__)

    mv.genres = str(lst_genre)

    print('Dict: ', mv.__dict__)

    result = insert(customer, mv)
    print('Insert: ', str(result))

    """
    mv.title = 'Avengers End Game'
    result = update(customer, mv)

    print('Update\n', str(result))
    print()
    result = delete(customer, 3)
    print('Delete\n', str(result))
    print()
    print('Select All\n', find_all(customer, {"title": "Avengers"}))    
    print()
    print('Select By Id\n', find_by_id(customer, 1))
    """