def transpose(mat: list[list[float | int]]) -> list[list[float | int]]:
    '''
    Поменять строки и столбцы местами. Пустая матрица [] → [].
    Если матрица «рваная» (строки разной длины) — ValueError.
    '''
    if not mat:
        return []
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            raise ValueError("Рваная матрица")

    rows = len(mat)
    trans_mat: list[list[float | int]] = [[0] * rows for _ in range(cols)]
    for r in range(rows):
        for c in range(cols):
            trans_mat[c][r] = mat[r][c]
    return trans_mat


def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Сумма по каждой строке матрицы.

    Args:
        mat: Прямоугольная матрица чисел.

    Returns:
        Список сумм по строкам.

    Raises:
        ValueError: Если матрица «рваная» (строки разной длины).
    """
    if not mat:
        return []

    cols = len(mat[0])
    sum_mat = []

    for row in mat:
        if len(row) != cols:
            raise ValueError("Рваная матрица")
        sum_mat.append(sum(row))

    return sum_mat


def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Сумма по каждому столбцу матрицы.

    Args:
        mat: Прямоугольная матрица чисел.

    Returns:
        Список сумм по каждому столбцу.

    Raises:
        ValueError: Если матрица «рваная».
    """
    if not mat:
        return []
    cols = len(mat[0])
    for row in mat:
        if len(row) != cols:
            raise ValueError("Рваная матрица")
    sums = []
    for c in range(cols):
        col_total = 0
        for row in mat:
            col_total += row[c]
        sums.append(col_total)
    return sums


if __name__ == "__main__":
    print("transpose:")
    cases_transpose = [
        [[1, 2, 3]],
        [[1], [2], [3]],
        [[1, 2], [3, 4]],
        [],
        [[1, 2], [3]],
    ]
    for case in cases_transpose:
        try:
            print(f"  {case} -> {transpose(case)}")
        except ValueError:
            print(f"  {case} -> ValueError")

    print("\nrow_sums:")
    cases_row_sums = [
        [[1, 2, 3], [4, 5, 6]],
        [[-1, 1], [10, -10]],
        [[0, 0], [0, 0]],
        [[1, 2], [3]],
    ]
    for case in cases_row_sums:
        try:
            print(f"  {case} -> {row_sums(case)}")
        except ValueError:
            print(f"  {case} -> ValueError")

    print("\ncol_sums:")
    cases_col_sums = [
        [[1, 2, 3], [4, 5, 6]],
        [[-1, 1], [10, -10]],
        [[0, 0], [0, 0]],
        [[1, 2], [3]],
    ]
    for case in cases_col_sums:
        try:
            print(f"  {case} -> {col_sums(case)}")
        except ValueError:
            print(f"  {case} -> ValueError")