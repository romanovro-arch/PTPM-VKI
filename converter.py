"""
Корневой модуль экспорта Converter.
Позволяет импортировать Converter как напрямую (from converter import Converter),
так и через пакет (from src.converter import Converter).
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
for p in (str(SRC_DIR), str(BASE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from src.converter import Converter

__all__ = ["Converter"]
