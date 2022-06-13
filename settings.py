# Валидные данные для авторизации
valid_email = '666cas@gmail.com'
valid_password = '2048256a'
# *****

# Не валидные данные для авторизации
invalid_email = '666cas@gmail.com'
invalid_password = '5789456123'
invalid_auth_key = {
  "key": "d157891f-34e1-4372-80e9-c376d5bcf123"
}
rotten_auth_key = {
  "key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae74"
}
# *****

# Данные для добавления питомца
add_name = 'Cat'
add_age = '13'
add_animal_type = 'Cat'
add_pet_photo = 'images/dog1.jpg'
# *****

# Данные для обновления информации о питомце
update_name = 'Серый'
update_age = '12'
update_animal_type = 'укуц'
update_pet_photo = 'images/dog.jpeg'
# ******

def generate_string(num):
    return "x" * num
def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'
def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'
