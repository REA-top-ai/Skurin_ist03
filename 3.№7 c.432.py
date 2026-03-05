with open('testtext.txt', 'r') as f:
    lines = [line.strip() for line in f]
corect = ['A', 'C', 'A', 'A', 'D',
               'B', 'C', 'A', 'C', 'B',
               'A', 'D', 'C', 'A', 'D',
               'C', 'B', 'B', 'D', 'A']
cor = 0
wrong = []
for i in range(20):
    if lines[i] == corect[i]:
        cor += 1
    else:
        wrong.append(i+1)

wrongnomb = 20 - cor
print('\n======== РЗУЛЬТАТЫ ========')
if cor >= 15:
    print('\nкрасаучик, ти сдал!')
else:
    print('\nанлаки, пересдача :(')

print(f'\nвсего верно: {cor}')
print(f'всего неверно: {wrongnomb}')

if wrongnomb > 0:
    print(f'\nномер с ошибочкой: {wrong}')
else:
    print('\nвсе верно братанчик!!')