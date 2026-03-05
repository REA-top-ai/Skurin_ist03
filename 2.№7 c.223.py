bank = 0
day1 = 1
a = 0
day = int(input('скико дней: '))
for i in range(1,day + 1):
    print(f'день {i} - заработано: {day1} копеек')
    bank += day1
    day1 *= 2
    a += bank
print('-'*len(f"всего заработано: {bank/100} руб"))
print(f'всего заработано: {bank/100} руб')


