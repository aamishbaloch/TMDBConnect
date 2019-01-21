import http.client
import json

from urllib.parse import quote
from tmbd.exceptions import ErrorConnectingTMDB


class TMDBConnect:
    """
    TMDBConnect is used to get more customized results from tmdb. All you need to give is the API key.
    """

    def __init__(self, api_key, session_id=None):
        self.conn = http.client.HTTPSConnection("api.themoviedb.org")
        self.version = "3"
        self.api_key = api_key
        self.session_id = session_id

    def request_get(self, url, params='', page=None, payload='{}'):
        params += f'&' if params else ''
        params += f'api_key={self.api_key}'
        params += f'&page={page}' if page else ''

        self.conn.request(
            'GET',
            f'/{self.version}/{url}?{params}',
            payload,
        )
        response = self.conn.getresponse()
        if not response.status == 200:
            raise ErrorConnectingTMDB()
        data = response.read()
        return json.loads(data.decode("utf-8"))

    def get_person_id_by_name(self, name):
        """
        :param name: name of the person you want an id for
        :return: person id of the searched person
        """
        response = self.request_get('search/person', f'include_adult=false&query={quote(name)}&language=en-US')
        if 'results' in response and len(response['results']) > 0:
            return response['results'][0]['id']

    def get_movies_by_director_id(self, director_id, sort='release_date.desc'):
        """
        Get all the movie titles directed by a given director.
        :param director_id: person_id
        :param sort: sort can have multiple values like
                    popularity.asc, popularity.desc, release_date.asc, release_date.desc,
                    revenue.asc, revenue.desc, primary_release_date.asc, primary_release_date.desc,
                    original_title.asc, original_title.desc, vote_average.asc, vote_average.desc,
                    vote_count.asc, vote_count.desc
                    default: release_date.desc
        :return: list of movie titles
        """
        movies_id_by_director = []
        movies_sorted = []

        response = self.request_get(f'person/{director_id}/movie_credits')
        if 'crew' in response:
            for item in response['crew']:
                if item['job'] == 'Director':
                    movies_id_by_director.append(item['id'])

        page = 1
        while True:
            response = self.request_get(
                'discover/movie', f'with_crew={director_id}&sort_by={sort}&include_video=false', page
            )
            if 'results' in response:
                for item in response['results']:
                    if item['id'] in movies_id_by_director:
                        movies_sorted.append(item)

                if page >= response['total_pages']:
                    break
                else:
                    page = page + 1

        return movies_sorted



