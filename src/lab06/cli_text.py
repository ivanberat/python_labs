import argparse
import sys
from pathlib import Path

from src.lab03.text_stats import print_table
from src.lib.text import count_freq, normalize, tokenize, top_n

ENCODING = "utf-8"


def _read_text(input_path: str) -> str:
    """Читает файл в UTF-8. Нет файла — FileNotFoundError, не UTF-8 — ValueError."""
    path = Path(input_path)
    if not path.is_file():
        raise FileNotFoundError(f"файл не найден: {input_path}")
    try:
        return path.read_text(encoding=ENCODING)
    except UnicodeDecodeError as error:
        raise ValueError(f"не удалось прочитать файл в кодировке UTF-8: {input_path}") from error


def cat(input_path: str, number: bool) -> None:
    """Печатает файл построчно. При number строки нумеруются с 1."""
    lines = _read_text(input_path).splitlines(keepends=True)
    for index, line in enumerate(lines, start=1):
        if number:
            print(f"{index:>6}  {line}", end="")
        else:
            print(line, end="")


def stats(input_path: str, top: int) -> None:
    """Печатает число слов, число уникальных слов и top самых частых слов."""
    tokens = tokenize(normalize(_read_text(input_path)))
    freq = count_freq(tokens)
    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{top}:")
    print_table(top_n(freq, top))


def main() -> int:
    parser = argparse.ArgumentParser(description="CLI-утилиты лабораторной №6: cat и stats")
    subparsers = parser.add_subparsers(dest="command", required=True)

    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла построчно")
    cat_parser.add_argument("--input", required=True, help="Путь к текстовому файлу")
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats_parser = subparsers.add_parser("stats", help="Частоты слов в тексте")
    stats_parser.add_argument("--input", required=True, help="Путь к текстовому файлу")
    stats_parser.add_argument("--top", type=int, default=5, help="Сколько самых частых слов показать")

    args = parser.parse_args()
    if args.command == "stats" and args.top <= 0:
        parser.error("--top должен быть положительным числом")

    try:
        if args.command == "cat":
            cat(args.input, args.n)
        else:
            stats(args.input, args.top)
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
