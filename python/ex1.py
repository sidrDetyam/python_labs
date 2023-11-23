def generate_pascal_triangle(n: int) -> None:
    try:
        n = int(n)
        if n <= 0:
            raise ValueError("Введите положительное целое число.")
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    pascal_triangle = [[1] * (i + 1) for i in range(n)]

    for i in range(2, n):
        for j in range(1, i):
            pascal_triangle[i][j] = pascal_triangle[i - 1][j - 1] + pascal_triangle[i - 1][j]

    for row in pascal_triangle:
        print(' '.join(map(str, row)).center(n * 4))


n = input("Введите целое положительное число n: ")
try:
    n = int(n)
    if n <= 0:
        raise ValueError("Введите положительное целое число")

    generate_pascal_triangle(n)
except ValueError as e:
    print(f"Неккоректный ввод: {e}")
