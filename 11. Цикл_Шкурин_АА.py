# задание 1

board_games = ['Settlers of Catan', 'Carcassone', 'Power Grid', 'Agricola', 'Scrabble']
sport_games = ['football', 'football - American', 'hockey', 'baseball', 'cricket']
for game in board_games:
    print(game)
print()
board_games = ['Settlers of Catan', 'Carcassone', 'Power Grid', 'Agricola', 'Scrabble']
sport_games = ['football', 'football - American', 'hockey', 'baseball', 'cricket']
for game in sport_games:
    print(game)

print()

# задание 2

promise = "I will not chew gum in class"
for i in range(5):
    print(promise)
print()
# задание 3

students_period_A = ["Alex", "Briana", "Cheri", "Daniele"]
students_period_B = ["Dora", "Minerva", "Alexa", "Obie"]

for y in students_period_A:
    students_period_B.append(y)

print(students_period_B)

print()

# задание 4

dog_breeds_available_for_adoption = ['french_bulldog', 'dalmatian', 'shihtzu', 'poodle', 'collie']
dog_breed_I_want = 'dalmatian'

for n in dog_breeds_available_for_adoption:
    if n == dog_breed_I_want:
        print("У них есть собака, которую я хочу!")
        break
print()

# задание 5

sales_data = [[12, 17, 22], [2, 10, 3], [5, 12, 13]]
scoops_sold = 0

for l in sales_data:
    for j in l:
        scoops_sold += j
print(scoops_sold)
print()

# задание 6
single_digits = list(range(10))
squares = []

for d in single_digits:
    print(d)
    squares.append(d ** 2)
print(squares)

cubes = [d ** 3 for d in single_digits]

print(cubes)