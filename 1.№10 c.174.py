# вариант 1
a = 0
print('введи деньгу: 5к 10к 50к')
b = int(input('нук: '))
c = a + b
while c != 100:
    if c < 100:
        print('маловата')
    elif c > 100:
        print('братух перегнул палку много взял')
        exit()
    b = int(input('плюсуй еще: '))
    c += b
print('красава точно сделал ')

# вариант 2(рубоики)

print('\nдарова!!')
print('короче надо тебе из 5,10 и 50 копеек сделать 1 руболь!!')
kop5 = int(input('\nскико 5 копеек: '))
kop10 = int(input('скико 10 копеек: '))
kop50 = int(input('скико 50 копеек: '))

bank = 0
bank += kop5*5+kop10*10+kop50*50
while bank != 100:
    if bank < 100:
        print(f'\nмоловато, не добрал {100-bank}')
        bank = 0
    else:
        print(f'\nперебрал ты на {bank-100}')
        bank = 0
    print('\nеще разок')
    kop5 = int(input('\nскико 5 копеек: '))
    kop10 = int(input('скико 10 копеек: '))
    kop50 = int(input('скико 50 копеек: '))
    bank += kop5 * 5 + kop10 * 10 + kop50 * 50
print('\nкрасава нормально дал')


# (омереконские долары)

print('\nдарова!!')
print('короче надо тебе из 5,10, 25 и 50 фунтов сделать 1 омереканский долар!!')
funt5 = int(input('\nскико 5 копеек: '))
funt10 = int(input('скико 10 копеек: '))
funt25 = int(input('скико 25 фунтов: '))
funt50 = int(input('скико 50 копеек: '))

bankfunt = 0
bankfunt += funt5*5+funt10*10+funt50*50+funt25*25
while bankfunt != 100:
    if bankfunt < 100:
        print(f'\nмоловато, не добрал {100-bankfunt}')
        bankfunt = 0
    else:
        print(f'\nперебрал ты на {bankfunt-100}')
        bankfunt = 0
    print('\nеще разок')
    funt5 = int(input('\nскико 5 копеек: '))
    funt10 = int(input('скико 10 копеек: '))
    funt25 = int(input('скико 25 фунтов: '))
    funt50 = int(input('скико 50 копеек: '))
    bankfunt += funt5*5+funt10*10+funt50*50+funt25*25
print('\nкрасава нормально дал')


