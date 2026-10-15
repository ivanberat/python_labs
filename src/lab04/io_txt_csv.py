import csv
import tempfile
from pathlib import Path


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает файл и возвращает его содержимое одной строкой.

    По умолчанию файл читается в utf-8. Если файл в другой кодировке,
    передайте её явно, например: read_text(path, encoding="cp1251").
    Если файла нет, падает FileNotFoundError. Если кодировка не
    подходит, падает UnicodeDecodeError.
    """
    return Path(path).read_text(encoding=encoding)


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт родительские папки пути, если их нет."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_csv(rows: list[tuple | list], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    """Создаёт или перезаписывает CSV-файл с разделителем запятой.

    Если передан header, он записывается первой строкой. Все строки
    должны быть одной длины, иначе ValueError. Пустой rows без header
    даёт пустой файл.
    """
    rows = list(rows)
    lengths = {len(row) for row in rows}
    if header is not None:
        lengths.add(len(header))
    if len(lengths) > 1:
        raise ValueError("все строки должны быть одной длины")
    ensure_parent_dir(path)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)

        sample = tmp_dir / "sample.txt"
        sample.write_text("Привет, мир! Привет!!!", encoding="utf-8")
        print("read_text, utf-8:")
        print(repr(read_text(sample)))

        empty = tmp_dir / "empty.txt"
        empty.write_text("", encoding="utf-8")
        print("\nread_text, пустой файл:")
        print(repr(read_text(empty)))

        cp = tmp_dir / "cp.txt"
        cp.write_bytes("Привет".encode("cp1251"))
        print("\nread_text, cp1251:")
        print(repr(read_text(cp, encoding="cp1251")))

        print("\nread_text, файла нет:")
        missing = tmp_dir / "no_such_file.txt"
        try:
            read_text(missing)
        except FileNotFoundError:
            print(f"FileNotFoundError: нет файла {missing.name}")

        out = tmp_dir / "check.csv"
        write_csv([("test", 3)], out, header=("word", "count"))
        print("\nwrite_csv, с заголовком:")
        print(out.read_text(encoding="utf-8"), end="")

        write_csv([], out, header=("a", "b"))
        print("\nwrite_csv, пустые строки и заголовок:")
        print(out.read_text(encoding="utf-8"), end="")

        write_csv([], out)
        print("\nwrite_csv, пустые строки без заголовка:")
        print(repr(out.read_text(encoding="utf-8")))

        print("\nwrite_csv, строки разной длины:")
        try:
            write_csv([("a", 1), ("b",)], out)
        except ValueError as error:
            print(f"ValueError: {error}")
