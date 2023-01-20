from unittest.mock import MagicMock
from dao.genre import GenreDAO
import pytest
from service.genre import GenreService, GenreNotFound


@pytest.fixture
def genre_dao():
    dao = GenreDAO(None)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()

    return dao


@pytest.fixture
def genre_service(genre_dao):
    return GenreService(dao=genre_dao)


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
def test_get_one(genre_service, data):
    genre_service.dao.get_one.return_value = data

    assert genre_service.get_one(data['id']) == data


def test_get_one_with_error(genre_service):
    # genre_service.dao.get_one.side_effect = GenreNotFound

    with pytest.raises(GenreNotFound):
        genre_service.get_one(0)


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
def test_get_all(genre_service, length, data):
    genre_service.dao.get_all.return_value = data

    test_result = genre_service.get_all()
    assert isinstance(test_result, list)
    assert len(test_result) == length
    assert test_result == data


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
                    'name': 'changed_name',
                },
            ),
    )
)
def test_partially_update(genre_service, original_data, modified_data):
    genre_service.dao.get_one.return_value = original_data
    genre_service.partially_update(modified_data)

    genre_service.dao.get_one.assert_called_once_with(original_data['id'])
    genre_service.dao.update.assert_called_once_with(modified_data)


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
def test_partially_update_with_wrong_fields(genre_service, original_data, modified_data):
    genre_service.dao.get_one.return_value = original_data
    genre_service.partially_update(modified_data)
    genre_service.dao.update.assert_called_once_with(original_data)


@pytest.mark.parametrize(
    'genre_id',
    (
        1,
    )
)
def test_delete(genre_service, genre_id):
    genre_service.delete(genre_id)
    genre_service.dao.delete.assert_called_once_with(genre_id)


@pytest.mark.parametrize(
    'genre_data',
    (
            (

                {
                    'id': 1,
                    'name': "test_name",
                }
            ),
    )
)
def test_update(genre_service, genre_data):
    genre_service.update(genre_data)
    genre_service.dao.update.assert_called_once_with(genre_data)
