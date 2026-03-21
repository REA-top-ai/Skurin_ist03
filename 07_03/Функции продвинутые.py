# Задание 1

# table = {
#     1: ['Jiho', False],
#     2:[],
#     3:[],
#     4:[],
#     5:[],
#     6:[],
#     7:[],
# }

# Задание 2

# def assign_table(table_number: int, name: str, vip_status: bool = False) -> None:
#     table[table_number] = [name, vip_status]

# assign_table(6, "Yoni", False)
# assign_table(name="Klara", table_number=4)
# print(table)

# Задание 3

# def print_order(*order_items):
#     print(*order_items)

# print_order('Orange Juice', 'Apple Juice', 'Scrambled Eggs', 'Pancakes')

# Задание 4

# table = {
#     1: {'name': 'Jiho',
#         'vip_status': False,
#         'order':'Orange Juice, Apple Juice'},
#     2:{},
#     3:{},
#     4:{},
#     5:{},
#     6:{},
#     7:{},
# }

# def assign_table(table_number: int, name: str, vip_status: bool = False) -> None:
#     table[table_number]['name'] = name
#     table[table_number]['vip_status'] = vip_status

# def assign_and_print_order(table_number: int, *order_items:str) -> None:
#     table[table_number]['order'] = order_items
#     for item in order_items:
#         print(item)

# assign_table(name="Arwa", table_number=2, vip_status=True)
# assign_and_print_order(2,'Стейк','Морской окунь','Бутылка Вина')


# Задание 5
# table = {
#     1: {'name': 'Jiho',
#         'vip_status': False,
#         'order': {
#             'drinks':'Orange Juice, Apple Juice',
#             'food_items':'Pancakes'
#                  }
#         },
#     2:{},
#     3:{},
#     4:{},
#     5:{},
#     6:{},
#     7:{},
# }


# def assign_food_items(**order_items):
#     food = order_items.get('food')
#     drinks = order_items.get('drinks')

# assign_food_items(food='Pancakes, Poached Egg', drinks='Water')


# Задание 6

def calculate_price_per_person(total, tip, split):
    total_tip = total * (tip / 100)
    split_price = (total + total_tip) / split
    print(split_price)


table_7_total = [534.50, 20.0, 5]
calculate_price_per_person(*table_7_total)