import csv
import json
import sys
import tempfile
from pathlib import Path

ENCODING = "utf-8"
# корень репозитория: src/lab05/json_csv.py → на два уровня вверх от папки lab05
ROOT = Path(__file__).resolve().parents[2]


def _check_suffix(path: Path, suffix: str) -> None:
    """Проверяет расширение файла, иначе ValueError."""
    if path.suffix.lower() != suffix:
        raise ValueError(f"ожидался файл {suffix}, получен: {path.name}")


def _to_cell(value) -> str:
    """Превращает значение из JSON в текст для ячейки CSV.

    None становится пустой строкой, список и словарь — JSON-текстом,
    bool — true/false как в JSON. Остальное — через str().
    """
    if value is None:
        return ""
    if isinstance(value, (list, dict, bool)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON-файл (список словарей) в CSV.

    Колонки — объединение ключей всех объектов в порядке первого
    появления. Отсутствующие поля записываются пустыми строками.
    Кодировка UTF-8.
    """
    src = Path(json_path)
    _check_suffix(src, ".json")
    text = src.read_text(encoding=ENCODING)
    if not text.strip():
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"битый JSON: {error.msg}, строка {error.lineno}") from error

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Список с не-словарями: каждый элемент должен быть объектом")

    # dict.fromkeys убирает повторы и сохраняет порядок первого появления
    columns = list(dict.fromkeys(key for item in data for key in item))

    dst = Path(csv_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", newline="", encoding=ENCODING) as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for item in data:
            writer.writerow({key: _to_cell(item.get(key)) for key in columns})


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Преобразует CSV в JSON (список словарей).

    Первая строка — заголовок, он обязателен. Все значения остаются
    строками, потому что в CSV нет типов. Кодировка UTF-8.
    """
    src = Path(csv_path)
    _check_suffix(src, ".csv")
    with src.open(encoding=ENCODING, newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        if not header:
            raise ValueError("CSV пустой или без заголовка")
        if len(set(header)) != len(header):
            raise ValueError(f"повторяющиеся колонки в заголовке: {header}")

        records = []
        for row in reader:
            if None in row:
                raise ValueError(f"строка {reader.line_num}: значений больше, чем колонок")
            if None in row.values():
                raise ValueError(f"строка {reader.line_num}: значений меньше, чем колонок")
            records.append(row)

    if not records:
        raise ValueError("Пустой CSV: в файле нет строк данных")

    dst = Path(json_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding=ENCODING) as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def _check(condition: bool, message: str) -> None:
    """Проверка результата конвертации. Не прошла — ValueError."""
    if not condition:
        raise ValueError(f"проверка не прошла: {message}")


def _demo() -> None:
    """Сценарии 1 и 2 из README: конвертация и сравнение с источником."""
    samples = ROOT / "data" / "samples"
    out = ROOT / "data" / "out"

    # Сценарий 1: JSON → CSV. Заголовок = объединение ключей, строк = записей.
    json_to_csv(samples / "people.json", out / "people_from_json.csv")
    with (samples / "people.json").open(encoding=ENCODING) as f:
        source = json.load(f)
    with (out / "people_from_json.csv").open(encoding=ENCODING, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames
    all_keys = list(dict.fromkeys(key for item in source for key in item))
    _check(header == all_keys, "заголовок CSV совпадает с ключами JSON")
    _check(len(rows) == len(source), "число строк CSV равно числу записей JSON")
    print("Сценарий 1, JSON → CSV")
    print(f"  заголовок: {header}")
    print(f"  записей в JSON: {len(source)}, строк данных в CSV: {len(rows)}")

    # Сценарий 2: CSV → JSON. Ключи объектов = заголовок, объектов = строк.
    csv_to_json(samples / "people.csv", out / "people_from_csv.json")
    with (samples / "people.csv").open(encoding=ENCODING, newline="") as f:
        reader = csv.DictReader(f)
        source_rows = list(reader)
        header = reader.fieldnames
    with (out / "people_from_csv.json").open(encoding=ENCODING) as f:
        records = json.load(f)
    _check(len(records) == len(source_rows), "число объектов JSON равно числу строк CSV")
    _check(all(set(record) == set(header) for record in records),
           "ключи каждого объекта совпадают с заголовком CSV")
    print("Сценарий 2, CSV → JSON")
    print(f"  строк данных в CSV: {len(source_rows)}, записей в JSON: {len(records)}")
    print(f"  ключи объектов: {sorted(header)}")


def _self_check() -> None:
    """Проверки ошибок на временных файлах. Каждый случай печатает результат."""
    cases = [
        ("пустой JSON-файл", "people.json", "", json_to_csv),
        ("JSON: не список", "people.json", '{"a": 1}', json_to_csv),
        ("JSON: пустой список", "people.json", "[]", json_to_csv),
        ("JSON: элемент не словарь", "people.json", "[1, 2]", json_to_csv),
        ("битый JSON", "people.json", "[{]", json_to_csv),
        ("неверное расширение JSON-функции", "people.txt", "[]", json_to_csv),
        ("пустой CSV-файл", "people.csv", "", csv_to_json),
        ("CSV: только заголовок", "people.csv", "name,age\n", csv_to_json),
        ("CSV: повтор колонки", "people.csv", "a,a\n1,2\n", csv_to_json),
        ("CSV: лишнее значение", "people.csv", "a,b\n1,2,3\n", csv_to_json),
        ("CSV: не хватает значения", "people.csv", "a,b\n1\n", csv_to_json),
        ("неверное расширение CSV-функции", "people.txt", "a\n1\n", csv_to_json),
    ]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for title, name, content, func in cases:
            src = tmp_dir / name
            src.write_text(content, encoding=ENCODING)
            try:
                func(src, tmp_dir / "out.file")
                print(f"НЕТ ОШИБКИ: {title}")
            except ValueError as error:
                print(f"ок, {title}: {error}")

        try:
            json_to_csv(tmp_dir / "нет.json", tmp_dir / "x.csv")
        except FileNotFoundError:
            print("ок, файл отсутствует: FileNotFoundError")

        cp = tmp_dir / "cp.csv"
        cp.write_bytes("имя,город\nАлиса,Москва\n".encode("cp1251"))
        try:
            csv_to_json(cp, tmp_dir / "x.json")
        except ValueError as error:
            print(f"ок, не UTF-8: {type(error).__name__}")


def main() -> int:
    try:
        _demo()
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    _self_check()
    print()
    sys.exit(main())
