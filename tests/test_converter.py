"""
Комплексный набор юнит-тестов для класса Converter (unittest).
Полностью покрывает положительные, отрицательные, граничные сценарии
и обработку исключительных ситуаций согласно ТЗ.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
for p in (str(SRC_DIR), str(BASE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import unittest

try:
    from converter import Converter
except ImportError:
    from src.converter import Converter


class TestConverter(unittest.TestCase):
    """
    Тестирование статического метода Converter.do(x: float) -> int.
    """

    # =========================================================================
    # 1. Диапазон x ∈ [100.7; +∞) -> возвращает 1000
    # =========================================================================

    def test_upper_boundary_exact_point(self):
        """Проверка точной нижней границы диапазона [100.7; +∞): x = 100.7."""
        self.assertEqual(Converter.do(100.7), 1000)

    def test_upper_boundary_just_above(self):
        """Проверка значения чуть выше границы: x = 100.8."""
        self.assertEqual(Converter.do(100.8), 1000)

    def test_upper_boundary_large_numbers(self):
        """Проверка больших положительных чисел в диапазоне: x = 200.0, 1000.5, 99999.9."""
        self.assertEqual(Converter.do(200.0), 1000)
        self.assertEqual(Converter.do(1000.5), 1000)
        self.assertEqual(Converter.do(99999.9), 1000)

    # =========================================================================
    # 2. Диапазон x ∈ (0; 100.7) -> возвращает целую часть int(x)
    # =========================================================================

    def test_positive_range_just_below_100_7(self):
        """Проверка значения чуть ниже верхней границы: x = 100.6 -> 100."""
        self.assertEqual(Converter.do(100.6), 100)

    def test_positive_range_spec_example(self):
        """Проверка примера из технического задания: x = 65.7 -> 65."""
        self.assertEqual(Converter.do(65.7), 65)

    def test_positive_range_integer_float(self):
        """Проверка вещественного числа с нулевой дробной частью: x = 50.0 -> 50."""
        self.assertEqual(Converter.do(50.0), 50)

    def test_positive_range_small_values(self):
        """Проверка малых положительных чисел: x = 1.9 -> 1, x = 1.0 -> 1."""
        self.assertEqual(Converter.do(1.9), 1)
        self.assertEqual(Converter.do(1.0), 1)

    def test_positive_range_near_zero(self):
        """Проверка значения чуть выше нуля: x = 0.1 -> 0."""
        self.assertEqual(Converter.do(0.1), 0)

    # =========================================================================
    # 3. Точка x == 0.0 -> генерируется исключение ValueError
    # =========================================================================

    def test_zero_raises_value_error(self):
        """Проверка генерации исключения ValueError при x = 0.0."""
        with self.assertRaises(ValueError) as context:
            Converter.do(0.0)
        self.assertIn("0.0", str(context.exception))

    def test_negative_zero_raises_value_error(self):
        """Проверка генерации исключения ValueError при x = -0.0."""
        with self.assertRaises(ValueError):
            Converter.do(-0.0)

    def test_integer_zero_raises_value_error(self):
        """Проверка генерации ValueError при передаче целочисленного 0."""
        with self.assertRaises(ValueError):
            Converter.do(0)

    # =========================================================================
    # 4. Диапазон x ∈ [-30.4; 0) -> возвращает int(x) - 5
    # =========================================================================

    def test_negative_range_near_zero(self):
        """Проверка значения чуть ниже нуля: x = -0.1 -> int(-0.1) - 5 = 0 - 5 = -5."""
        self.assertEqual(Converter.do(-0.1), -5)

    def test_negative_range_small_values(self):
        """Проверка отрицательных чисел: x = -1.5 -> -1 - 5 = -6, x = -1.0 -> -1 - 5 = -6."""
        self.assertEqual(Converter.do(-1.5), -6)
        self.assertEqual(Converter.do(-1.0), -6)

    def test_negative_range_medium_values(self):
        """Проверка значений в середине диапазона: x = -10.0 -> -15, x = -25.9 -> -30."""
        self.assertEqual(Converter.do(-10.0), -15)
        self.assertEqual(Converter.do(-25.9), -30)

    def test_negative_range_just_before_boundary(self):
        """Проверка точки перед нижней границей: x = -30.3 -> int(-30.3) - 5 = -35."""
        self.assertEqual(Converter.do(-30.3), -35)

    def test_negative_range_exact_boundary(self):
        """Проверка точной нижней границы [-30.4; 0): x = -30.4 -> int(-30.4) - 5 = -35."""
        self.assertEqual(Converter.do(-30.4), -35)

    # =========================================================================
    # 5. Диапазон x ∈ (-∞; -30.5] -> возвращает -2000
    # =========================================================================

    def test_lower_boundary_exact_point(self):
        """Проверка точной верхней границы диапазона (-∞; -30.5]: x = -30.5 -> -2000."""
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_lower_boundary_just_below(self):
        """Проверка значения чуть ниже границы: x = -30.6 -> -2000."""
        self.assertEqual(Converter.do(-30.6), -2000)

    def test_lower_boundary_spec_example(self):
        """Проверка примера из технического задания: x = -94.5 -> -2000."""
        self.assertEqual(Converter.do(-94.5), -2000)

    def test_lower_boundary_large_negative_numbers(self):
        """Проверка больших по модулю отрицательных чисел: x = -500.0, -99999.9 -> -2000."""
        self.assertEqual(Converter.do(-500.0), -2000)
        self.assertEqual(Converter.do(-99999.9), -2000)

    # =========================================================================
    # 6. Проверка типов входных данных (TypeError)
    # =========================================================================

    def test_invalid_type_string_raises_type_error(self):
        """Проверка передачи строки: Converter.do('100.7') -> TypeError."""
        with self.assertRaises(TypeError):
            Converter.do("100.7")

    def test_invalid_type_none_raises_type_error(self):
        """Проверка передачи None: Converter.do(None) -> TypeError."""
        with self.assertRaises(TypeError):
            Converter.do(None)

    def test_invalid_type_boolean_raises_type_error(self):
        """Проверка передачи булева значения: Converter.do(True) -> TypeError."""
        with self.assertRaises(TypeError):
            Converter.do(True)

    def test_invalid_type_list_raises_type_error(self):
        """Проверка передачи списка: Converter.do([10.5]) -> TypeError."""
        with self.assertRaises(TypeError):
            Converter.do([10.5])

    # =========================================================================
    # 7. Проверка контракта статического метода
    # =========================================================================

    def test_method_is_staticmethod(self):
        """Проверка, что метод Converter.do декорирован как @staticmethod."""
        self.assertIsInstance(Converter.__dict__["do"], staticmethod)

    def test_call_via_instance(self):
        """Проверка возможности вызова как через класс, так и через экземпляр."""
        instance = Converter()
        self.assertEqual(instance.do(100.7), 1000)
        self.assertEqual(instance.do(65.7), 65)


if __name__ == "__main__":
    unittest.main()
