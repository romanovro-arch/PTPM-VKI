"""
Корневая точка входа для Лабораторной работы № 3.
Делегирует запуск функции main() из src/main.py.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
for p in (str(SRC_DIR), str(BASE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from src.main import main

if __name__ == "__main__":
    main()
