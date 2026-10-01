def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Возвращает минимум и максимум списка без min() и max()."""
    if not len(nums):
        raise ValueError("список пуст")

    mn = mx = nums[0]
    for x in nums:
        if x < mn:
            mn = x
        if x > mx:
            mx = x
    return mn, mx


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Возвращает отсортированный список уникальных элементов без sort() и sorted()."""
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
    """Переводит матрицу в плоский список."""
    vector = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError("передана не матрица")
        vector.extend(row)
    return vector


if __name__ == "__main__":
    print("Тест кейсы:")

    print(f"""
min_max

[3, -1, 5, 5, 0] -> {min_max([3, -1, 5, 5, 0])}
[42] -> {min_max([42])}
[-5, -2, -9] -> {min_max([-5, -2, -9])}
[1.5, 2, 2.0, -3.1] -> {min_max([1.5, 2, 2.0, -3.1])}
""")
    # Ошибка ValueError:
    #print(f"[] -> {min_max([])}")

    print(f"""
unique_sorted

[3, 1, 2, 1, 3] -> {unique_sorted([3, 1, 2, 1, 3])}
[] -> {unique_sorted([])}
[-1, -1, 0, 2, 2] -> {unique_sorted([-1, -1, 0, 2, 2])}
[1.0, 1, 2.5, 2.5, 0] -> {unique_sorted([1.0, 1, 2.5, 2.5, 0])}
""")

    print(f"""
flatten

[[1, 2], [3, 4]] -> {flatten([[1, 2], [3, 4]])}
[[1, 2], (3, 4, 5)] -> {flatten([[1, 2], (3, 4, 5)])}
[[1], [], [2, 3]] -> {flatten([[1], [], [2, 3]])}
""")
    # Ошибка TypeError:
    print(f'[[1, 2], "ab"] -> {flatten([[1, 2], "ab"])}')
