test = input('введите ответы капсом без пробелов: ')

with open('3.txt', 'r', encoding='utf-8') as file:
    num = 0
    count = 0
    while True:
        line = file.readline()
        if not line:
            break
        num += 1
        line_clean = line.strip()
        for i in range(len(test)):
            if i < len(line_clean):
                if test[i] == line_clean[i]:
                    count += 1

print(f'верных ответов {count} из 20!')