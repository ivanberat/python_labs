"""Статистика по тексту из stdin."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from text import count_freq, normalize, tokenize, top_n

TOP_SIZE = 5
TABLE_MODE = True


def print_table(top: list[tuple[str, int]]) -> None:
    """Печатает топ слов в виде таблицы."""
    width = 5
    for word, _ in top:
        if len(word) > width:
            width = len(word)

    print(f"{'слово':<{width}} | частота")
    print("-" * (width + 10))
    for word, count in top:
        print(f"{word:<{width}} | {count}")


if __name__ == "__main__":
    text = sys.stdin.read()
    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, TOP_SIZE)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(set(tokens))}")
    print(f"Топ-{TOP_SIZE}:")
    if TABLE_MODE:
        print_table(top)
    else:
        for word, count in top:
            print(f"{word}:{count}")
