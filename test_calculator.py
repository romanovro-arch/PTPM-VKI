import unittest
import io
import sys

from class_main import (
    Operation,
    Addition,
    Multiplication,
    Division,
    Subtraction,
    Power,
    Factorial,
    Calculator
)


class TestAddition(unittest.TestCase):
    def setUp(self):
        self.operation = Addition()

    def test_addition(self):
        self.assertEqual(self.operation.execute(2, 3), 5)
        self.assertEqual(self.operation.execute(-5, 5), 0)
        self.assertEqual(self.operation.execute(0, 0), 0)
        self.assertEqual(self.operation.execute(100, 200), 300)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "+")


class TestMultiplication(unittest.TestCase):
    def setUp(self):
        self.operation = Multiplication()

    def test_multiplication(self):
        self.assertEqual(self.operation.execute(2, 3), 6)
        self.assertEqual(self.operation.execute(-2, 3), -6)
        self.assertEqual(self.operation.execute(0, 5), 0)
        self.assertEqual(self.operation.execute(7, 1), 7)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "*")


class TestDivision(unittest.TestCase):
    def setUp(self):
        self.operation = Division()

    def test_division(self):
        self.assertEqual(self.operation.execute(10, 2), 5.0)
        self.assertEqual(self.operation.execute(7, 2), 3.5)
        self.assertEqual(self.operation.execute(0, 5), 0.0)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            self.operation.execute(5, 0)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "/")


class TestSubtraction(unittest.TestCase):
    def setUp(self):
        self.operation = Subtraction()

    def test_subtraction(self):
        self.assertEqual(self.operation.execute(10, 3), 7)
        self.assertEqual(self.operation.execute(3, 10), -7)
        self.assertEqual(self.operation.execute(0, 0), 0)
        self.assertEqual(self.operation.execute(-5, -3), -2)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "-")


class TestPower(unittest.TestCase):
    def setUp(self):
        self.operation = Power()

    def test_power(self):
        self.assertEqual(self.operation.execute(2, 3), 8)
        self.assertEqual(self.operation.execute(5, 0), 1)
        self.assertEqual(self.operation.execute(3, 2), 9)
        self.assertEqual(self.operation.execute(2, 10), 1024)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "^")


class TestFactorial(unittest.TestCase):
    def setUp(self):
        self.operation = Factorial()

    def test_factorial_zero(self):
        self.assertEqual(self.operation.execute(0), 1)

    def test_factorial_one(self):
        self.assertEqual(self.operation.execute(1), 1)

    def test_factorial_five(self):
        self.assertEqual(self.operation.execute(5), 120)

    def test_factorial_six(self):
        self.assertEqual(self.operation.execute(6), 720)

    def test_factorial_ten(self):
        self.assertEqual(self.operation.execute(10), 3628800)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            self.operation.execute(-1)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "!")


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_operations(self):
        self.assertIsInstance(self.calculator.operations["1"], Addition)
        self.assertIsInstance(self.calculator.operations["2"], Multiplication)
        self.assertIsInstance(self.calculator.operations["3"], Division)
        self.assertIsInstance(self.calculator.operations["4"], Subtraction)
        self.assertIsInstance(self.calculator.operations["5"], Power)
        self.assertIsInstance(self.calculator.operations["6"], Factorial)

    def test_calculate_addition(self):
        result = self.calculator.calculate("1", 2, 3)
        self.assertTrue(result)

    def test_calculate_multiplication(self):
        result = self.calculator.calculate("2", 2, 3)
        self.assertTrue(result)

    def test_calculate_division(self):
        result = self.calculator.calculate("3", 6, 2)
        self.assertTrue(result)

    def test_calculate_subtraction(self):
        result = self.calculator.calculate("4", 5, 3)
        self.assertTrue(result)

    def test_calculate_power(self):
        result = self.calculator.calculate("5", 2, 3)
        self.assertTrue(result)

    def test_calculate_factorial(self):
        result = self.calculator.calculate("6", 5, 0)
        self.assertTrue(result)

    def test_calculate_exit(self):
        result = self.calculator.calculate("0", 0, 0)
        self.assertFalse(result)

    def test_calculate_invalid_choice(self):
        result = self.calculator.calculate("9", 0, 0)
        self.assertTrue(result)

    def test_calculate_factorial_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("6", 5, 0)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "5! = 120"
            )
        finally:
            sys.stdout = original_stdout

    def test_calculate_addition_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("1", 2, 3)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "2 + 3 = 5"
            )
        finally:
            sys.stdout = original_stdout

    def test_calculate_multiplication_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("2", 2, 3)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "2 * 3 = 6"
            )
        finally:
            sys.stdout = original_stdout

    def test_calculate_division_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("3", 6, 2)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "6 / 2 = 3.0"
            )
        finally:
            sys.stdout = original_stdout

    def test_calculate_subtraction_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("4", 5, 3)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "5 - 3 = 2"
            )
        finally:
            sys.stdout = original_stdout

    def test_calculate_power_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("5", 2, 3)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "2 ^ 3 = 8"
            )
        finally:
            sys.stdout = original_stdout

    def test_division_by_zero_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("3", 5, 0)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "Ошибка: деление на ноль!"
            )
        finally:
            sys.stdout = original_stdout

    def test_negative_factorial_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("6", -5, 0)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "Ошибка: факториал отрицательного числа не существует!"
            )
        finally:
            sys.stdout = original_stdout

    def test_invalid_choice_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("9", 0, 0)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "Неверный выбор! Попробуйте снова."
            )
        finally:
            sys.stdout = original_stdout

    def test_exit_output(self):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.calculator.calculate("0", 0, 0)
            self.assertEqual(
                captured_output.getvalue().strip(),
                "До свидания!"
            )
        finally:
            sys.stdout = original_stdout


if __name__ == "__main__":
    unittest.main()
