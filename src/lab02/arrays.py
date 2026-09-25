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


if __name__ == "__main__":
    print("min_max:")
    cases_min_max = [
        [3, -1, 5, 5, 0],
        [42],
        [-5, -2, -9],
        [],
        [1.5, 2, 2.0, -3.1],
    ]
    for case in cases_min_max:
        try:
            print(f"  {case} -> {min_max(case)}")
        except ValueError:
            print(f"  {case} -> ValueError")

    print("\nunique_sorted:")
    cases_unique = [
        [3, 1, 2, 1, 3],
        [],
        [-1, -1, 0, 2, 2],
        [1.0, 1, 2.5, 2.5, 0],
    ]
    for case in cases_unique:
        print(f"  {case} -> {unique_sorted(case)}")

    print("\nflatten:")
    cases_flatten = [
        [[1, 2], [3, 4]],
        [[1, 2], (3, 4, 5)],
        [[1], [], [2, 3]],
        [[1, 2], "ab"],
    ]
    for case in cases_flatten:
        try:
            print(f"  {case} -> {flatten(case)}")
        except TypeError:
            print(f"  {case} -> TypeError")



