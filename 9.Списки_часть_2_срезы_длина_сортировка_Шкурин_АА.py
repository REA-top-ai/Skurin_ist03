# задание 1

list1= range(2,20,3)
list_len = len(list1)
print(list_len)

print()

# задание 2

shopping_list = ['яйца', 'масло', 'молоко', 'огурцы', 'сок', 'хлопья']

print(len(shopping_list))

last_element = shopping_list[-1]
element5 = shopping_list[4]
print(last_element, element5)

print()

# задание 3

suitcase = ['рубашка', 'рубашка', 'брюки', 'брюки', 'пижамы', 'книги']
beginning = suitcase [0: 2]
print(len(beginning))
beginning4 = suitcase [0: 4]
print(beginning4)
beginning34 = suitcase [2: 4]
print(beginning34)
print()

# задание 4
suitcase1 = ['рубашка', 'футболка', 'носки', 'очки', 'пижама', 'книги']
start = suitcase1[0: 3]
print(start)
print()

# задание 5

votes = ['Jake', 'Jake', 'Laurie', 'Laurie', 'Laurie', 'Jake', 'Jake', 'Jake', 'Laurie', 'Cassie', 'Cassie', 'Jake', 'Jake', 'Cassie', 'Laurie', 'Cassie', 'Jake',
'Jake', 'Cassie', 'Laurie']

jake_vote = votes.count('Jake')
print(jake_vote)
print()

# задание 6

addresses = ['221 B Baker St.', '42 Wallaby Way', '12 Grimmauld Place',\
             '742 Evergreen Terrace' , '1600 Pennsylvania Ave', '10 Downing St.']
addresses.sort()
print(addresses)
print()

# задание 7

games = ['Portal', 'Minecraft', 'Pacman', 'Tetris', 'The Sims', 'Pokemon']
game_sort = sorted(games)
print(game_sort)

print()

# задание 8

inventory = ["двухспальная кровать", "двухспальная кровать", "изголовье", "двуспальная кровать",
             "двуспальная кровать", "комод", "комод", "стол", "стол", "тумбочка", "тумбочка",
             "королевский кровать", "двуспальная кровать", "две односпальные кровати",
             "две односпальные кровати", "простыни", "простыни", "подушка", "подушка"]

inventory_len = len(inventory)
print(f"1. Количество товаров на складе: {inventory_len}")

first = inventory[0]
print(f"2. Первый элемент: {first}")

last = inventory[-1]
print(f"3. Последний элемент: {last}")

inventory26 = inventory[2:6]
print(f"4. Элементы с индекса 2 до 6: {inventory26}")

first3 = inventory[:3]
print(f"5. Первые 3 элемента: {first3}")

twin_beds = inventory.count("две односпальные кровати")
print(f"6. Количество односпальных кроватей: {twin_beds}")

inventory.sort()
print(f"7. Отсортированный инвентарь: {inventory}")