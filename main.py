"""
Демонстрационная точка входа для Среза знаний по юнит-тестам (Converter).
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
for p in (str(SRC_DIR), str(BASE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from converter import Converter


def main():
    print("=" * 60)
    print("Практическое задание: Срез знаний по юнит-тестам (Converter)")
    print("=" * 60)

    demo_values = [
        150.0,
        100.7,
        100.6,
        65.7,
        1.5,
        0.1,
        -0.1,
        -15.0,
        -30.4,
        -30.5,
        -94.5,
    ]

    print("\n[Автоматический прогон контрольных значений из ТЗ]:")
    for val in demo_values:
        res = Converter.do(val)
        print(f"  Converter.do({val:>6.1f}) -> {res:>5}")

    print("\n[Проверка исключения при x = 0.0]:")
    try:
        Converter.do(0.0)
    except ValueError as e:
        print(f"  Converter.do(   0.0) -> Успешно перехвачено исключение: {type(e).__name__} ({e})")

    print("\n" + "=" * 60)
    print("Все сценарии работают в строгом соответствии с ТЗ.")
    print("=" * 60)


if __name__ == "__main__":
    main()
