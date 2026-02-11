# задание 1

import datetime
current_time = datetime.datetime.now()
print(current_time)
print()

# задание 2

import random
random_list = [random.randint(1, 100) for _ in range(101)]
random_number = random.choice(random_list)
print(random_number)
print()

# задание 3

import matplotlib.pyplot as plt
import random

numbers_a = range(1, 13)
numbers_b = random.sample(range(1000), 12)

plt.plot(numbers_a, numbers_b)
plt.show()

# задание 4

from datetime import datetime, date
employees = [
    {
        "ФИО": "Иванов Иван Иванович",
        "Должность": "Менеджер",
        "Дата найма": "22.10.2013",
        "Оклад": 250000
    },
    {
        "ФИО": "Сорокина Екатерина Матвеевна",
        "Должность": "Аналитик",
        "Дата найма": "12.03.2020",
        "Оклад": 75000
    },
    {
        "ФИО": "Струков Иван Сергеевич",
        "Должность": "Старший программист",
        "Дата найма": "23.04.2012",
        "Оклад": 150000
    },
    {
        "ФИО": "Корнеева Анна Игоревна",
        "Должность": "Ведущий программист",
        "Дата найма": "22.02.2015",
        "Оклад": 120000
    },
    {
        "ФИО": "Старчиков Сергей Анатольевич",
        "Должность": "Младший программист",
        "Дата найма": "12.11.2021",
        "Оклад": 50000
    },
    {
        "ФИО": "Бутенко Артем Андреевич",
        "Должность": "Архитектор",
        "Дата найма": "12.02.2010",
        "Оклад": 200000
    },
    {
        "ФИО": "Савченко Алина Сергеевна",
        "Должность": "Старший аналитик",
        "Дата найма": "13.04.2016",
        "Оклад": 100000
    }
]

def calculate_experience(hire_date_str):
    hire_date = datetime.strptime(hire_date_str, "%d.%m.%Y").date()
    today = date.today()
    experience_years = today.year - hire_date.year
    if today.month < hire_date.month or (today.month == hire_date.month and today.day < hire_date.day):
        experience_years -= 1
    return experience_years



def calculate_experience_months(hire_date_str):
    hire_date = datetime.strptime(hire_date_str, "%d.%m.%Y").date()
    today = date.today()
    months = (today.year - hire_date.year) * 12 + (today.month - hire_date.month)
    if today.day < hire_date.day:
        months -= 1
    return months


def programmer_day_bonus(employee):
    programmer_positions = ["Старший программист", "Ведущий программист", "Младший программист", "Архитектор"]
    if employee["Должность"] in programmer_positions:
        return employee["Оклад"] * 0.03
    return 0


def holiday_bonus(employee):
    bonus = 2000
    if "ич" in employee["ФИО"].split()[2]:
        return bonus
    else:
        return bonus

def salary_indexation(employee):
    experience_years = calculate_experience(employee["Дата найма"])

    if experience_years > 10:
        return employee["Оклад"] * 0.07
    else:
        return employee["Оклад"] * 0.05

def vacation_schedule(employees_list):
    eligible_employees = []
    for employee in employees_list:
        months_experience = calculate_experience_months(employee["Дата найма"])
        if months_experience > 6:
            eligible_employees.append(employee["ФИО"])
    return eligible_employees
print("Список сотрудников:")
print("-" * 80)
for emp in employees:
    print(f"{emp['ФИО']:30} | {emp['Должность']:25} | {emp['Дата найма']:12} | {emp['Оклад']:8} руб.")
print()

print("Премии ко Дню программиста (13 сентября):")
print("-" * 60)
for emp in employees:
    bonus = programmer_day_bonus(emp)
    if bonus > 0:
        print(f"{emp['ФИО']:30} | Премия: {bonus:.2f} руб.")
print()

print("Праздничные премии (8 марта / 23 февраля):")
print("-" * 60)
for emp in employees:
    bonus = holiday_bonus(emp)
    print(f"{emp['ФИО']:30} | Премия: {bonus:.2f} руб.")
print()

print("Индексация зарплат:")
print("-" * 60)
for emp in employees:
    indexation = salary_indexation(emp)
    experience = calculate_experience(emp["Дата найма"])
    print(
        f"{emp['ФИО']:30} | Стаж: {experience} лет | Индексация: {indexation:.2f} руб. | Новый оклад: {emp['Оклад'] + indexation:.2f} руб.")
print()

print("График отпусков (сотрудники со стажем более 6 месяцев):")
print("-" * 60)
vacation_list = vacation_schedule(employees)
for name in vacation_list:
    print(f"{name}")
print(f"\nВсего сотрудников с правом на отпуск: {len(vacation_list)}")

print("\n" + "=" * 80)
print("ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
print("=" * 80)

for emp in employees:
    exp_years = calculate_experience(emp["Дата найма"])
    exp_months = calculate_experience_months(emp["Дата найма"])
    programmer_bonus = programmer_day_bonus(emp)
    holiday_b = holiday_bonus(emp)
    index = salary_indexation(emp)

    print(f"\n{emp['ФИО']}:")
    print(f"  Должность: {emp['Должность']}")
    print(f"  Стаж: {exp_years} лет ({exp_months} месяцев)")
    print(f"  Текущий оклад: {emp['Оклад']} руб.")
    print(f"  Премия ко Дню программиста: {programmer_bonus:.2f} руб.")
    print(f"  Праздничная премия: {holiday_b:.2f} руб.")
    print(f"  Индексация: {index:.2f} руб.")
    print(
        f"  Итоговый доход с учетом премий и индексации: {emp['Оклад'] + programmer_bonus + holiday_b + index:.2f} руб.")

#