# Задание 1
b = input()
contains_a = lambda a: 'a' in b
print(contains_a('a'))
print()

# Задани 2
c = input()
long_string = lambda s: len(s) > 12
print(long_string(c))
print()

# Задание 3
d = input()
end_in_a = lambda e: 'a' in d[-1]
print(end_in_a(d))
print()

# Задание 4
num = int(input())
even_or_odd = lambda num: "четное" if num % 2 == 0 else "нечетное"
print(even_or_odd(num))
print()

# Задание 5

num1 = int(input())
even_or_odd = lambda num1: "кратно 3" if num1 % 3 == 0 else "не кратно 3"
print(even_or_odd(num1))
print()

# Задание 6

reit = int(input('поставь оценку от 1 до 10: '))
rate_movie = lambda reit: 'мне понравился этот фильм' if reit >= 8.5 else 'этот фильм был не оч'
print(rate_movie(reit))