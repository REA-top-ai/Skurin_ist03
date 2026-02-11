# Задача 1

def f_to_c(f_temp):
    c_temp = (f_temp - 32) * 5/9
    return c_temp
f = int(input())
f100_in_c = f_to_c(100)
print(f"F = {f100_in_c} C")

def c_to_f(c_temp):
    f_temp = c_temp * (9/5) + 32
    return f_temp

c0_in_fahrenheit = c_to_f(0)
print(f"0 C = {c0_in_fahrenheit} F")

print(c0_in_fahrenheit)

print()

# Задача 2

def get_force(mass, acceleration):
    force = mass * acceleration
    return force

train_mass = 22680
train_acceleration = 10
train_force = get_force(train_mass, train_acceleration)
print(f"Поезд GE поставляет {train_force} ньютонов силы")

def get_energy(mass, c=3*10**8):
    energy = mass * c**2
    return energy

bomb_energy = get_energy(1)
print(f"1 кг бомбы составляет {bomb_energy} Джоулей")

def get_work(mass, acceleration, distance):
    force = get_force(mass, acceleration)
    work = force * distance
    return work

train_distance = 100
train_work = get_work(train_mass, train_acceleration, train_distance)
print(f"Поезд выполняет {train_work} Джоулей за {train_distance} метров.")

print()

# Задача 3

def print_wardrobe(clothes, time_of_day):
    print(f"У меня большой гардероб.")
    print(f"{time_of_day} лучше всего подходит {clothes}")

def print_meal_preferences(meal, time_of_day):
    print(f"Мои предпочтения в еде.")
    print(f"{time_of_day} лучше всего подходит {meal}")

clothes = "домашняя одежда"
for time in ["Утром", "Днём", "Вечером", "Ночью"]:
    print_wardrobe(clothes, time)

meal = "завтрак"
for time in ["Утром", "Днём", "Вечером"]:
    print_meal_preferences(meal, time)

print()

# Задача 4

def check_user_access(user_name,  APM):
    users_APM = {"Дмитрий": 1,"Ангелина": 2,"Василий": 3,"Екатерина": 4}

    if user_name in users_APM:
        if APM == users_APM[user_name]:
            return "Добро пожаловать!"
        elif user_name == "Дмитрий":
            return "Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!"
        else:
            return "Логин или пароль не верный, попробуйте еще раз"
    else:
        return "Пользователь не найден"
# проверим
print(check_user_access("Дмитрий", 1))
print(check_user_access("Дмитрий", 2))
print(check_user_access("Ангелина", 2))
print(check_user_access("Ангелина", 5))

print()

# Задача 5

def get_grade(average_score):
    if average_score >= 4.0:
        return "A"
    elif average_score >= 3.0:
        return "B"
    elif average_score >= 2.0:
        return "C"
    elif average_score >= 1.0:
        return "D"
    else:
        return "F"

grades_to_check = [4.5, 3.5, 2.5, 1.5, 0.5]
for grade in grades_to_check:
    print(f"Средний балл {grade} -> Грейд {get_grade(grade)}")
