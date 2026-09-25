def format_record(rec: tuple[str, str, float]) -> str:
    """Форматирует данные студента в строку вида 'Фамилия И.О., гр. ГРУППА, GPA X.XX'[cite: 2].

    Args:
        rec: Кортеж из трех элементов (ФИО, группа, средний балл)[cite: 2].

    Returns:
        Отформатированная строка по шаблону[cite: 2].

    Raises:
        TypeError: Если передан не кортеж или типы полей неверные (не str, str, float/int)[cite: 2].
        ValueError: Если в кортеже не 3 элемента, пустое ФИО, пустая группа или GPA вне диапазона от 0.0 до 5.0[cite: 2].
    """
    if not isinstance(rec, tuple):
        raise TypeError("Передан не кортеж")
    if len(rec) != 3:
        raise ValueError("Длина кортежа должна быть 3")
    fio, group, gpa = rec
    if not isinstance(fio, str) or not isinstance(group, str) or not isinstance(gpa, (int, float)):
        raise TypeError("Неверный тип данных в элементах кортежа")
    words = fio.split()
    if len(words) not in (2, 3):
        raise ValueError("ФИО должно содержать фамилию и 1-2 имени/отчества")
    clear_group = group.strip()
    if not clear_group:
        raise ValueError("Пустая группа")
    if not (0.0 <= gpa <= 5.0):
        raise ValueError("GPA вне диапазона от 0.0 до 5.0")
    surname = words[0].capitalize()
    initials = "".join(f"{w[0].upper()}." for w in words[1:])
    return f"{surname} {initials}, гр. {clear_group}, GPA {gpa:.2f}"


if __name__ == "__main__":
    print("format_record:")
    cases_format_record = [
        ("Иванов Иван Иванович", "BIVT-25", 4.6),
        ("Петров Пётр", "IKB0-12", 5.0),
        ("Петров Пётр Петрович", "IKB0-12", 5.0),
        ("  сидорова   анна   сергеевна  ", "ABB-01", 3.999),
        ("", "BIVT-25", 4.5),
        ("Иванов Иван", "   ", 4.5),
        ("Иванов Иван", "BIVT-25", "4.6"),
        ("Иванов Иван", "BIVT-25", 6.0),
        ["Иванов Иван", "BIVT-25", 4.5],
    ]

    for case in cases_format_record:
        try:
            print(f"  {str(case):<52} -> {format_record(case)}")
        except ValueError:
            print(f"  {str(case):<52} -> ValueError")
        except TypeError:
            print(f"  {str(case):<52} -> TypeError")