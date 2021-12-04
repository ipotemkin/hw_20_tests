from unittest.mock import MagicMock
import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db

OBJECTS = []


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    m1 = Movie(id=1,
               title='Harry Potter',
               description="Some description",
               rating=10,
               director_id=1,
               genre_id=1,
               trailer="#",
               year=2015,
               genre="qrq",
               director="qrqy")

    m2 = Movie(id=2, title='Titanic', description="Some description")
    m3 = Movie(id=3, title='Ocean', description="Some description", genre_id=0)
    movie_create = dict(id=3, title='Ocean', description="Some description", genre_id=0)

    objects_d = {1: m1, 2: m2, 3: m3}

    global OBJECTS
    OBJECTS = [m1, m2, m3]

    movie_dao.get_one = MagicMock(side_effect=objects_d.get)
    movie_dao.get_all = MagicMock(return_value=[m1, m2, m3])
    movie_dao.create = MagicMock(return_value=Movie(**movie_create))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    movie_dao.partially_update = MagicMock()
    # movie_dao.objects = objects_d

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(2)
        assert movie is not None
        assert movie.id == 2
        assert movie.title == 'Titanic'

    def test_get_one_100(self):
        movie = self.movie_service.get_one(100)
        assert movie is None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0
        assert isinstance(movies, list)
        assert movies == OBJECTS

    def test_create(self):
        movie_d = {
            'title': 'Superman',
            'description': "Some description"
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None
        assert movie.id == 3

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            'id': 3,
            'title': 'Superman'
        }
        self.movie_service.update(movie_d)

    def test_partially_update(self):
        movie_d = {
            'id': 3,
            'title': 'Superman',
            'description': "Some description",
            'rating': 10,
            'director_id': 1,
            'genre_id': 1,
            'trailer': "#",
            'year': 2015,
            'genre': "qrq",
            'director': "qrqy"
        }
        self.movie_service.partially_update(movie_d)

