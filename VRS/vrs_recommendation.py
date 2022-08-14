import pandas as pd
import vrs_dataset as ds
import vrs_ml_model as model


def get_recommendation(customer_id, movie_title):
    # Getting the Dataset
    movies_df = ds.find_all(customer_id, {})

    # Getting the model
    vrs_model = model.get_ml_model(customer_id)

    # ###### Constructing a reverse map of indices and movie titles
    map_indices = pd.Series(movies_df.index, index=movies_df.title).drop_duplicates()

    try:
        # Getting the index of the movie that matches the title
        idx = map_indices[movie_title]
    except Exception as ex:
        print(ex)
        idx = -1

    if idx >= 0:
        # Getting the pairwise similarity scores of all movies with that movies
        similarity_scores = list(enumerate(vrs_model[idx]))

        # Sorting the movie based on similarity score
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        similarity_scores = similarity_scores[1:10]

        # Get the movie indices
        movie_indices = [i[0] for i in similarity_scores]

        return movies_df.iloc[movie_indices]
    else:
        return pd.DataFrame()


if __name__ == '__main__':
    print('vrs_recommendation :: test')
    customer_id_test = 'movies_db'
    print(get_recommendation(customer_id_test, 'Avatar'))
