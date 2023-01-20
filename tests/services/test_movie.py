from unittest.mock import MagicMock
from dao.movie import MovieDAO
import pytest
from service.movie import MovieService, MovieNotFound


@pytest.fixture
def movie_dao():
    dao = MovieDAO(None)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()

    return dao


@pytest.fixture
def movie_service(movie_dao):
    return MovieService(dao=movie_dao)


@pytest.mark.parametrize(
    'data',
    (
            {
                'id': 1,
                'name': 'test',
            },
            {
                'id': 2,
                'name': 'test_name',
            },
    )
)
def test_get_one(movie_service, data):
    movie_service.dao.get_one.return_value = data

    assert movie_service.get_one(data['id']) == data


def test_get_one_with_error(movie_service):
    # movie_service.dao.get_one.side_effect = movieNotFound

    with pytest.raises(MovieNotFound):
        movie_service.get_one(0)


@pytest.mark.parametrize(
    'length, data',
    (
            (
                2,
                [
                        {
                            'id': 1,
                            'name': 'test',
                        },
                        {
                            'id': 2,
                            'name': 'test_name',
                        },
                    ],
            ),
            (
                0,
                [],
            ),

    ),
)
def test_get_all(movie_service, length, data):
    movie_service.dao.get_all.return_value = data

    test_result = movie_service.get_all()
    assert isinstance(test_result, list)
    assert len(test_result) == length
    assert test_result == data


@pytest.mark.parametrize(
    'original_data, modified_data',
    (
            (
                {
                    'id': 1,
                    'title': 'test',
                },
                {
                    'id': 1,
                    'description': 'test',
                },
                {
                    'id': 1,
                    'trailer': 'test',
                },
                {
                    'id': 1,
                    'year': 'test',
                },
                {
                    'id': 1,
                    'rating': 'test',
                },
                {
                    'id': 1,
                    'genre_id': 'test',
                },
                {
                    'id': 1,
                    'director_id': 'test',
                },
            ),
    )
)
def test_partially_update(movie_service, original_data, modified_data):
    movie_service.dao.get_one.return_value = original_data
    movie_service.partially_update(modified_data)

    movie_service.dao.get_one.assert_called_once_with(original_data['id'])
    movie_service.dao.update.assert_called_once_with(modified_data)


@pytest.mark.parametrize(
    'original_data, modified_data',
    (
            (
                {
                    'id': 1,
                    'name': 'test',
                },
                {
                    'id': 1,
                    'wrong_field': 'wrong_data',
                },
            ),
    )
)
def test_partially_update_with_wrong_fields(movie_service, original_data, modified_data):
    movie_service.dao.get_one.return_value = original_data
    movie_service.partially_update(modified_data)
    movie_service.dao.update.assert_called_once_with(original_data)


@pytest.mark.parametrize(
    'movie_id',
    (
        1,
    )
)
def test_delete(movie_service, movie_id):
    movie_service.delete(movie_id)
    movie_service.dao.delete.assert_called_once_with(movie_id)


@pytest.mark.parametrize(
    'movie_data',
    (
            (

                {
                    'id': 1,
                    'name': "test_name",
                }
            ),
    )
)
def test_update(movie_service, movie_data):
    movie_service.update(movie_data)
    movie_service.dao.update.assert_called_once_with(movie_data)
