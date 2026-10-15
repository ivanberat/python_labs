import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from io_txt_csv import read_text, write_csv
from text import count_freq, normalize, tokenize, top_n

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "lab04"
DEFAULT_IN = DATA_DIR / "input.txt"
DEFAULT_OUT = DATA_DIR / "report.csv"
DEFAULT_PER_FILE = DATA_DIR / "report_per_file.csv"
DEFAULT_TOTAL = DATA_DIR / "report_total.csv"
TOP_SIZE = 5


def words_of(text: str) -> list[str]:
    """Нормализует текст и возвращает список слов."""
    return tokenize(normalize(text))


def print_table(top: list[tuple[str, int]]) -> None:
    """Печатает топ слов в виде таблицы."""
    width = 5
    for word, _ in top:
        width = max(width, len(word))

    print(f"{'слово':<{width}} | частота")
    print("-" * (width + 10))
    for word, count in top:
        print(f"{word:<{width}} | {count}")


def print_summary(tokens: list[str], freq: dict[str, int],
                  table: bool) -> None:
    """Печатает краткое резюме по словам."""
    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    top = top_n(freq, TOP_SIZE)
    print(f"Топ-{TOP_SIZE}:")
    if table:
        print_table(top)
    else:
        for word, count in top:
            print(f"{word}:{count}")


def run_single(text: str, out: Path, table: bool) -> None:
    """Считает слова в одном тексте и пишет report с колонками word,count."""
    tokens = words_of(text)
    freq = count_freq(tokens)
    write_csv(top_n(freq, len(freq)), out, header=("word", "count"))
    print_summary(tokens, freq, table)


def run_many(texts: dict[Path, str], per_file: Path, total: Path,
             table: bool) -> None:
    """Пишет отчёт по каждому файлу и сводный отчёт по всем файлам."""
    labels: dict[Path, str] = {path: path.name for path in texts}
    if len(set(labels.values())) < len(labels):
        labels = {path: str(path) for path in texts}
    per_file_rows: list[tuple[str, str, int]] = []
    all_tokens: list[str] = []
    for path in sorted(texts, key=lambda p: labels[p]):
        tokens = words_of(texts[path])
        all_tokens.extend(tokens)
        freq = count_freq(tokens)
        for word, count in top_n(freq, len(freq)):
            per_file_rows.append((labels[path], word, count))

    write_csv(per_file_rows, per_file, header=("file", "word", "count"))
    total_freq = count_freq(all_tokens)
    write_csv(top_n(total_freq, len(total_freq)), total,
              header=("word", "count"))
    print_summary(all_tokens, total_freq, table)


def parse_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Отчёт о частотах слов в текстовых файлах.")
    parser.add_argument("--in", dest="inputs", nargs="+", type=Path,
                        default=[DEFAULT_IN], metavar="FILE",
                        help="входной файл или несколько файлов")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="CSV для одного входного файла")
    parser.add_argument("--per-file", type=Path, default=DEFAULT_PER_FILE,
                        help="CSV по каждому файлу (при нескольких входах)")
    parser.add_argument("--total", type=Path, default=DEFAULT_TOTAL,
                        help="сводный CSV (при нескольких входах)")
    parser.add_argument("--encoding", default="utf-8",
                        help="кодировка входных файлов")
    parser.add_argument("--table", action="store_true",
                        help="печатать таблицу вместо списка")
    return parser.parse_args()


def main() -> None:
    """Читает файлы по аргументам и пишет отчёты."""
    args = parse_args()
    try:
        texts = {path: read_text(path, encoding=args.encoding)
                 for path in args.inputs}
        if len(args.inputs) == 1:
            run_single(texts[args.inputs[0]], args.out, args.table)
        else:
            run_many(texts, args.per_file, args.total, args.table)
    except (OSError, LookupError, UnicodeDecodeError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
