import unittest

from tmbd.exceptions import ErrorConnectingTMDB
from tmbd.helper import TMDBConnect
from tmbd.settings import tmdb_api_key


class TestMoviesByDirector(unittest.TestCase):

    def setUp(self):
        self.valid_director = 'Quentin Tarantino'
        self.invalid_director = 'Aamish Baloch'

        self.tmdb_client = TMDBConnect(tmdb_api_key)

    def test_get_director_id(self):
        director_id = self.tmdb_client.get_person_id_by_name(self.valid_director)
        self.assertEqual(director_id, 138)

    def test_get_invalid_director_id(self):
        director_id = self.tmdb_client.get_person_id_by_name(self.invalid_director)
        self.assertEqual(director_id, None)

    def test_get_movies_by_director_id(self):
        director_id = self.tmdb_client.get_person_id_by_name(self.valid_director)
        movies = self.tmdb_client.get_movies_by_director_id(director_id)
        self.assertEqual(len(movies), 17)

    def test_get_movies_by_invalid_director_id(self):
        director_id = self.tmdb_client.get_person_id_by_name(self.invalid_director)
        with self.assertRaises(ErrorConnectingTMDB):
            self.tmdb_client.get_movies_by_director_id(director_id)
