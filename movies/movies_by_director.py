from tmbd.helper import TMDBConnect
from tmbd.settings import tmdb_api_key


def movies_by_director(director_name):
    """
    method used to get list of movie titles directed by the given name
    :param director_name: name of the director
    :return: list of movie titles directed by the given name
    """
    tmdb_client = TMDBConnect(tmdb_api_key)
    director_id = tmdb_client.get_person_id_by_name(director_name)

    if director_id:
        movies = tmdb_client.get_movies_by_director_id(director_id)
        for movie in movies:
            print(movie['original_title'])


if __name__ == '__main__':
    movies_by_director("Quentin Tarantino")
