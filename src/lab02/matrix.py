def transpose(mat: list[list[float | int]]) -> list[list]:
    """Транспонирует прямоугольную матрицу (меняет строки и столбцы местами)."""
    if not mat:
        return []

    row_len = len(mat[0])
    for row in mat:
        if len(row) != row_len:
            raise ValueError("Матрица должна быть прямоугольной")

    if row_len == 0:
        return []

    return [[mat[r][c] for r in range(len(mat))] for c in range(row_len)]


def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Вычисляет сумму элементов каждой строки прямоугольной матрицы."""
    if not mat:
        return []

    row_len = len(mat[0])
    for row in mat:
        if len(row) != row_len:
            raise ValueError("Матрица должна быть прямоугольной")

    return [sum(row) for row in mat]


def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Вычисляет сумму элементов каждого столбца прямоугольной матрицы."""
    if not mat:
        return []

    row_len = len(mat[0])
    for row in mat:
        if len(row) != row_len:
            raise ValueError("Матрица должна быть прямоугольной")

    if row_len == 0:
        return []

    sums = []
    for c in range(row_len):
        sums.append(sum(mat[r][c] for r in range(len(mat))))
    return sums


if __name__ == "__main__":
    print("Тест кейсы:")

    print(f"""
transpose

[[1, 2, 3]] -> {transpose([[1, 2, 3]])}
[[1], [2], [3]] -> {transpose([[1], [2], [3]])}
[[1, 2], [3, 4]] -> {transpose([[1, 2], [3, 4]])}
[] -> {transpose([])}
""")
    # Ошибка ValueError:
    #print(f"[[1, 2], [3]] -> {transpose([[1, 2], [3]])}")

    print(f"""
row_sums

[[1, 2, 3], [4, 5, 6]] -> {row_sums([[1, 2, 3], [4, 5, 6]])}
[[-1, 1], [10, -10]] -> {row_sums([[-1, 1], [10, -10]])}
[[0, 0], [0, 0]] -> {row_sums([[0, 0], [0, 0]])}
""")
    # Ошибка ValueError:
    #print(f"[[1, 2], [3]] -> {row_sums([[1, 2], [3]])}")

    print(f"""
col_sums

[[1, 2, 3], [4, 5, 6]] -> {col_sums([[1, 2, 3], [4, 5, 6]])}
[[-1, 1], [10, -10]] -> {col_sums([[-1, 1], [10, -10]])}
[[0, 0], [0, 0]] -> {col_sums([[0, 0], [0, 0]])}
""")
    # Ошибка ValueError:
    print(f"[[1, 2], [3]] -> {col_sums([[1, 2], [3]])}")