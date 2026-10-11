import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    """Приводит строку к единому виду: регистр, буква ё, лишние пробелы."""
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()

    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")

    return " ".join(text.split())


def tokenize(text: str) -> list[str]:
    """Разбивает текст на слова. Дефис внутри слова слово не разрывает."""
    return re.findall(r"\w+(?:-\w+)*", text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Считает, сколько раз каждое слово встречается в списке."""
    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Возвращает n самых частых слов, при равной частоте по алфавиту."""
    if n < 0:
        raise ValueError("n не может быть отрицательным")
    items = sorted(freq.items(), key=lambda pair: (-pair[1], pair[0]))
    return items[:n]


if __name__ == "__main__":
    print("Тест кейсы:")

    s1 = "ПрИвЕт\nМИр\t"
    s2 = "ёжик, Ёлка"
    s3 = "Hello\r\nWorld"
    s4 = "  двойные   пробелы  "
    print(f"""
normalize

{s1!r} -> {normalize(s1)!r}
{s2!r} -> {normalize(s2)!r}
{s3!r} -> {normalize(s3)!r}
{s4!r} -> {normalize(s4)!r}
""")

    t1 = "привет мир"
    t2 = "hello,world!!!"
    t3 = "по-настоящему круто"
    t4 = "2025 год"
    t5 = "emoji :) не слово"
    print(f"""
tokenize

{t1} -> {tokenize(t1)}
{t2} -> {tokenize(t2)}
{t3} -> {tokenize(t3)}
{t4} -> {tokenize(t4)}
{t5} -> {tokenize(t5)}
""")

    w1 = ["a", "b", "a", "c", "b", "a"]
    freq1 = count_freq(w1)
    print(f"""
count_freq

{w1} -> {freq1}

top_n

{freq1}, n=2 -> {top_n(freq1, 2)}
""")

    w2 = ["bb", "aa", "bb", "aa", "cc"]
    freq2 = count_freq(w2)
    print(f"""
count_freq

{w2} -> {freq2}

top_n

{freq2}, n=2 -> {top_n(freq2, 2)}
""")

    top_n(freq1, -1)
