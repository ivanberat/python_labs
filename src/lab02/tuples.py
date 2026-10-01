StudentRecord = tuple[str, str, float]


def format_record(rec: StudentRecord) -> str:
    """Форматирует запись студента в строку вида «Фамилия И.О., гр. ГРУППА, GPA X.XX»."""
    if not isinstance(rec, tuple) or len(rec) != 3:
        raise TypeError("Запись должна быть кортежем из 3 элементов")

    fio, group, gpa = rec

    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError("ФИО и группа должны быть строками")
    if not isinstance(gpa, (int, float)):
        raise TypeError("GPA должен быть числом")

    words = fio.strip().split()
    if len(words) < 2:
        raise ValueError("ФИО должно содержать фамилию и хотя бы одно имя")

    clean_group = group.strip()
    if not clean_group:
        raise ValueError("Группа не может быть пустой")

    if not (0.0 <= gpa <= 5.0):
        raise ValueError("GPA должен быть от 0.0 до 5.0")

    surname = words[0].capitalize()
    initials = "".join(f"{w[0].upper()}." for w in words[1:3])

    return f"{surname} {initials}, гр. {clean_group}, GPA {gpa:.2f}"


if __name__ == "__main__":
    print("Тест кейсы:")

    print(f"""
format_record

('Иванов Иван Иванович', 'BIVT-25', 4.6) -> {format_record(('Иванов Иван Иванович', 'BIVT-25', 4.6))}
('Петров Пётр', 'IKBO-12', 5.0) -> {format_record(('Петров Пётр', 'IKBO-12', 5.0))}
('Петров Пётр Петрович', 'IKBO-12', 5.0) -> {format_record(('Петров Пётр Петрович', 'IKBO-12', 5.0))}
('  сидорова  анна   сергеевна ', 'ABB-01', 3.999) -> {format_record(('  сидорова  анна   сергеевна ', 'ABB-01', 3.999))}
""")
    # Ошибка ValueError:
    print(f'("", "ABB-01", 4.0) -> {format_record(("", "ABB-01", 4.0))}')