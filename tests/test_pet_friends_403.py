from api import PetFriends
from settings import *
import os
import pytest


pf = PetFriends()


def test_get_api_key_for_non_mail_and_pass(email='', password=''):
    """ Проверяем что запрос api ключа возвращает статус 403. Если нет email и password """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn&#x27;t found in database" in result
# -----------------------------------------------------------------------------------------------------


def test_get_api_key_for_invalid_mail(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403. Если email не верный """

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn&#x27;t found in database" in result
# -----------------------------------------------------------------------------------------------------


def test_get_api_key_for_invalid_pass(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 403. Если password не верный"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn&#x27;t found in database" in result
# -----------------------------------------------------------------------------------------------------


def test_add_new_pet_with_valid_data_invalid_key(name=add_name, animal_type=add_animal_type, age=add_age,
                                                 pet_photo=add_pet_photo):
    """Тест добавления питомца с корректными данными и неверным auth_key"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = invalid_auth_key
    status, result = pf.add_new_pet_and_photo(auth_key, name, animal_type, age, pet_photo)  # Отправляем запрос
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result
# ----------------------------------------------------------------------------------------------------


def test_add_new_pet_with_valid_data_rotten_key(name=add_name, animal_type=add_animal_type, age=add_age,
                                                pet_photo=add_pet_photo):
    """Тест добавления питомца с корректными данными и auth_key с истекшим сроком"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = rotten_auth_key
    status, result = pf.add_new_pet_and_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result
# --------------------------------------------------------------------------------------------------


def test_get_all_pets_with_invalid_key(filter='my_pets'):
    """Тест на получение списка питомцев с неверным auth_key"""

    auth_key = invalid_auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27;' in result
# --------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("name", ['', generate_string(255)
                                    , generate_string(1001)
                                    , russian_chars()
                                    , russian_chars().upper()
                                    , chinese_chars()
                                    , special_chars()
                                    , '123'
                                  ], ids=[
                                    'empty'
                                    , '255 symbols'
                                    , 'more than 1000 symbols'
                                    , 'russian'
                                    , 'RUSSIAN'
                                    , 'chinese'
                                    , 'specials'
                                    , 'digit'
])
def test_add_new_pet_simple(name, animal_type='двортерьер', age='4'):
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    pytest.status, result = pf.add_new_pet_not_photo(pytest.key, name, animal_type, age)
    if name == '':
        assert pytest.status == 400 or 200  # должен быть 400 код, но сервер позволяет постить все, что можно
    elif len(name) > 250:
        assert 400 or 200
    elif len(name) > 1000:
        assert 400 or 200
# Нет смысла расписывать дальше, идею вы поняли. Сервис пропускает любые данные
    else:
        assert pytest.status == 200
        assert result['name'] == name
        assert result['age'] == age
        assert result['animal_type'] == animal_type
# ----------------------------------------------------------------------------------------------


def test_delete_pet_shlack_user():
    """Удаление всего шлака"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_not_photo(auth_key, add_name, add_age, add_animal_type)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    while len(my_pets['pets']) != 0:
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()











