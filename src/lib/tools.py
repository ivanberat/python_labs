def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Возвращает кортеж (минимум, максимум) без использования встроенных min() и max()."""
    if not nums:
        raise ValueError("Список не должен быть пустым")

    mn = mx = nums[0]
    for x in nums:
        if x < mn:
            mn = x
        if x > mx:
            mx = x
    return mn, mx


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный список уникальных элементов без sort() и sorted()."""
    # Собираем уникальные элементы
    unique = []
    for x in nums:
        if x not in unique:
            unique.append(x)
    for i in range(len(unique)):
        for j in range(len(unique) - 1):
            if unique[j] > unique[j + 1]:
                unique[j], unique[j + 1] = unique[j + 1], unique[j]
    return unique


def flatten(mat: list[list | tuple]) -> list:
    """«Расплющивает» список списков/кортежей в один одномерный список."""
    res = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError("«строка не строка строк матрицы»")
        for x in row:
            res.append(x)
    return res


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