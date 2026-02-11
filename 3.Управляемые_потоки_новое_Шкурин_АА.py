# Задания №1
from operator import truediv

print((6*6)-1==8+1) #False
print(13-7 != (3*2)+1) #True
print(3*(2-1)==4-1) #True
print()

# Задания №2

print((6*6)-1>=8+1) #True
print(13-7 <= (3*2)+1) #True
print(3*(2-1)>4-1) #False
print()

# Задания №3
 # bool_variable = true Ошибка : name 'true' is not defined
 # print(bool_variable)
bool_variable = "true"
print(type(bool_variable)) # строка
print(bool_variable)

bool_variable2 = True
print(type(bool_variable2))
print(bool_variable2)
print()
# Задания №4
usr_name = input("Введите свое имя: ")
Dmima_Check = "Дмитрий"
if usr_name == Dmima_Check:
    print('Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!')
else:
    print('Добро пожаловать', usr_name)

# Задания №5

statement_1 = (2+2+2>=6) and (-1*-1<0)
statement_2 = (4*2<=8) and (7 - 1 == 6)

Dmima_Check = "Дмитрий"
Angel_check = 'Ангелина'
Vasea_check = 'Василий'
Katea_chek = 'Екатерина'
APM1 = "1234"
APM2 = "2345"
APM3 = "3456"
APM4 = "5678"

DA = Dmima_Check + APM1
AA = Angel_check + APM2
VA = Vasea_check + APM3
KA = Katea_chek + APM4

usr_name = input("Введите свое имя: ")
pasw = input('Ведите свой APM: ')

if usr_name + pasw == DA:
    print('Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!')
elif usr_name + pasw != AA and usr_name + pasw != VA and usr_name + pasw != KA and usr_name + pasw != DA:
    print('Логин или пароль не верный')
else:
    print("Добро пожаловать!")


# Задания №6
print((2-1>3) or (-5*2==-10))
print((9+5 <= 15) or (7 != 4+3))