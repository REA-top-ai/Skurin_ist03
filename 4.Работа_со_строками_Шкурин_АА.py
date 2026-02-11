# Задание 1
first_name = input("Ваше имя: ")
last_name = input('Ваша фамилия: ')

new_account = last_name[:5]
temp_password = last_name[2:6]

print(f"Имя: {first_name}")
print(f"Фамилия: {last_name}")

print(f'Ваш логин:{new_account} Ваш пароль:{temp_password}')

print()

# Задание 2

def account_generator(first_name, last_name):
    first_part = first_name[:3]
    second_part = last_name[:3]
    return first_part + second_part

new_account = account_generator(first_name, last_name)
print(f"Новый логин: {new_account}")

print()

# Задание 3

def password_generator(first_name, last_name):
    first_part = first_name[-3:]
    second_part = last_name[-3:]
    return first_part + second_part

temp_password = password_generator(first_name, last_name)
print(f"Новый пароль: {temp_password}")

print()

# Задание 4

company_motto = "Мечты сбываются"

second_to_last = company_motto[-2]
print(f"Предпоследний символ: '{second_to_last}'")

final_word = company_motto[-4:]
print(f"Последние 4 символа: '{final_word}'")

print()

# Задание 5

first_name1 = "Доб"
fixed_first_name1 = "Р" + first_name1[1:]
print(f"Исправленное имя: {fixed_first_name1}")

print()

# Задание 6

poem_title = "spring storm"
poem_author = "William Carlos Williams"

poem_title_fixed = poem_title.title()

print(f"Исходное название: {poem_title}")
print(f"Исправленное название: {poem_title_fixed}")
