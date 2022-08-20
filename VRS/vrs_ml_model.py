from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vrs_result_data import Result
from vrs_utils import log
import numpy as np
import pandas as pd
import vrs_dataset as ds

__module = '[VRS-ML-MODEL]'
__model_path = 'model/'


# Return list of top 3 elements or entire list , which ever is more
def __get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        # Checking if the length of list is more than 3 or not
        if len(names) > 3:
            names = names[:3]
        return names
    return []


# Function to convert string to lowercase and remove spaces
def __clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        # check if director exists
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return []


def __merged_features(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + ' '.join(x['director']) + ' ' + ' '.join(
        x['genres'])


def create_ml_model(customer_id):
    result = Result()

    log(__module, customer_id, 'Creating model for the company ' + customer_id)

    # try:
    # Get all the active movies recorded to generate the model
    movie_filter = {}
    movies_df = ds.find_all(customer_id, movie_filter)
    if not movies_df.empty:

        log(__module, customer_id, '============ There are {len(movies_df)} movies registered')

        log(__module, customer_id, '============ Preparing the features: cast, genre and keywords ... ')

        # Cast, genre and Keywords cleaning and preparation
        features = ['cast', 'keywords', 'genres']
        for feature in features:
            movies_df[feature] = movies_df[feature].apply(lambda x: literal_eval(str(x)))

        for feature in features:
            movies_df[feature] = movies_df[feature].apply(__get_list)

        log(__module, customer_id, '============ Cleaning the features: cast, genre, keywords, director')
        # Applying clean_data function to features
        features = ['cast', 'keywords', 'genres', 'director']
        for feature in features:
            movies_df[feature] = movies_df[feature].apply(__clean_data)

        log(__module, customer_id, '============ Creating merged_feature to base recommender')
        movies_df['merged_features'] = movies_df.apply(__merged_features, axis=1)

        log(__module, customer_id, '============ Creating the model ... ')
        # Creating Count Matrix
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(movies_df['merged_features'])
        model_cosine_similarity = cosine_similarity(count_matrix, count_matrix)
        log(__module, customer_id, '=================== Done ... ')

        # Save the model and index map in a file
        # ###### Model
        log(__module, customer_id, '============ Saving the model ... ')
        np.savetxt(__model_path + customer_id + '.ml', model_cosine_similarity)
        log(__module, customer_id, '=================== Done ... ')

        result.set_result(1, "Success")
        """
        except Exception as e:
            result.set_result(0, "ERROR: Something happened while creating the model!")
        finally:
            del movies_df
            del model_cosine_similarity
        """
    return result


def get_ml_model(customer_id):
    log(__module, customer_id, 'Getting the saved model for the company: ' + customer_id)

    # Getting the model
    model_cosine_similarity = np.loadtxt(__model_path + customer_id + '.ml')

    # return the model
    return model_cosine_similarity


if __name__ == '__main__':
    print('vrs_ml_model :: test')
    customer_id_test = 'movies_db'
    print(create_ml_model(customer_id_test))
    model = get_ml_model(customer_id_test)
    print(model)
