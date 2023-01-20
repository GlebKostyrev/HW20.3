from unittest.mock import MagicMock
from dao.director import DirectorDAO
import pytest
from service.director import DirectorService, DirectorNotFound


@pytest.fixture
def director_dao():
    dao = DirectorDAO(None)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()

    return dao


@pytest.fixture
def director_service(director_dao):
    return DirectorService(dao=director_dao)


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
def test_get_one(director_service, data):
    director_service.dao.get_one.return_value = data

    assert director_service.get_one(data['id']) == data


def test_get_one_with_error(director_service):
    # director_service.dao.get_one.side_effect = DirectorNotFound

    with pytest.raises(DirectorNotFound):
        director_service.get_one(0)


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
def test_get_all(director_service, length, data):
    director_service.dao.get_all.return_value = data

    test_result = director_service.get_all()
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
def test_partially_update(director_service, original_data, modified_data):
    director_service.dao.get_one.return_value = original_data
    director_service.partially_update(modified_data)

    director_service.dao.get_one.assert_called_once_with(original_data['id'])
    director_service.dao.update.assert_called_once_with(modified_data)


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
def test_partially_update_with_wrong_fields(director_service, original_data, modified_data):
    director_service.dao.get_one.return_value = original_data
    director_service.partially_update(modified_data)
    director_service.dao.update.assert_called_once_with(original_data)


@pytest.mark.parametrize(
    'director_id',
    (
        1,
    )
)
def test_delete(director_service, director_id):
    director_service.delete(director_id)
    director_service.dao.delete.assert_called_once_with(director_id)


@pytest.mark.parametrize(
    'director_data',
    (
            (

                {
                    'id': 1,
                    'name': "test_name",
                }
            ),
    )
)
def test_update(director_service, director_data):
    director_service.update(director_data)
    director_service.dao.update.assert_called_once_with(director_data)
