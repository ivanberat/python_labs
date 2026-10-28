"""ЛР6, задание B: CLI-подкоманды json2csv, csv2json, csv2xlsx поверх функций ЛР5.

Запуск из корня репозитория:
    python3 -m src.lab06.cli_convert json2csv --in data/samples/people.json --out data/out/people.csv
"""
import argparse
import sys
from pathlib import Path

from src.lab05.csv_xlsx import csv_to_xlsx
from src.lab05.json_csv import csv_to_json, json_to_csv

# команда: (функция из ЛР5, расширение входа, расширение выхода)
COMMANDS = {
    "json2csv": (json_to_csv, ".json", ".csv"),
    "csv2json": (csv_to_json, ".csv", ".json"),
    "csv2xlsx": (csv_to_xlsx, ".csv", ".xlsx"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="CLI-утилиты лабораторной №6: конвертеры данных")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, (_, source_ext, target_ext) in COMMANDS.items():
        sub = subparsers.add_parser(name, help=f"Преобразует {source_ext} в {target_ext}")
        sub.add_argument("--in", dest="input", required=True, help=f"Входной {source_ext} файл")
        sub.add_argument("--out", dest="output", required=True, help=f"Выходной {target_ext} файл")

    args = parser.parse_args()
    convert, source_ext, target_ext = COMMANDS[args.command]

    if Path(args.input).suffix.lower() != source_ext:
        parser.error(f"входной файл должен быть {source_ext}, получен: {Path(args.input).name}")
    if Path(args.output).suffix.lower() != target_ext:
        parser.error(f"выходной файл должен быть {target_ext}, получен: {Path(args.output).name}")

    try:
        if not Path(args.input).is_file():
            raise FileNotFoundError(f"файл не найден: {args.input}")
        convert(args.input, args.output)
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print(f"Готово: {args.input} → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
