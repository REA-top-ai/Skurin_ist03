def magic_square(square):
    numbers = []
    for row in square:
        for num in row:
            numbers.append(num)
    if sorted(numbers) != list(range(1, 10)):
        return False
    magic_sum = 15
    for row in square:
        if sum(row) != magic_sum:
            return False
    for col in range(3):
        col_sum = square[0][col] + square[1][col] + square[2][col]
        if col_sum != magic_sum:
            return False
    diag1 = square[0][0] + square[1][1] + square[2][2]
    diag2 = square[0][2] + square[1][1] + square[2][0]

    if diag1 != magic_sum or diag2 != magic_sum:
        return False

    return True

test_square = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
]

if magic_square(test_square):
    print("эт квадрат Лоу Шунина!")
else:
    print("эт обычнй квадрат.")