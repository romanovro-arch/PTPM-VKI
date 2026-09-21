import unittest

from class_main import (
    Operation,
    Addition,
    Multiplication,
    Division,
    Subtraction,
    Power,
    Calculator
)


class TestAddition(unittest.TestCase):
    def setUp(self):
        self.operation = Addition()

    def test_execute(self):
        self.assertEqual(self.operation.execute(2, 3), 5)
        self.assertEqual(self.operation.execute(-5, 5), 0)
        self.assertEqual(self.operation.execute(0, 0), 0)
        self.assertEqual(self.operation.execute(100, 200), 300)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "+")


class TestMultiplication(unittest.TestCase):
    def setUp(self):
        self.operation = Multiplication()

    def test_execute(self):
        self.assertEqual(self.operation.execute(2, 3), 6)
        self.assertEqual(self.operation.execute(-2, 3), -6)
        self.assertEqual(self.operation.execute(0, 5), 0)
        self.assertEqual(self.operation.execute(7, 1), 7)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "*")


class TestDivision(unittest.TestCase):
    def setUp(self):
        self.operation = Division()

    def test_execute(self):
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

    def test_execute(self):
        self.assertEqual(self.operation.execute(10, 3), 7)
        self.assertEqual(self.operation.execute(3, 10), -7)
        self.assertEqual(self.operation.execute(0, 0), 0)
        self.assertEqual(self.operation.execute(-5, -3), -2)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "-")


class TestPower(unittest.TestCase):
    def setUp(self):
        self.operation = Power()

    def test_execute(self):
        self.assertEqual(self.operation.execute(2, 3), 8)
        self.assertEqual(self.operation.execute(5, 0), 1)
        self.assertEqual(self.operation.execute(3, 2), 9)
        self.assertEqual(self.operation.execute(2, 10), 1024)

    def test_symbol(self):
        self.assertEqual(self.operation.symbol(), "^")


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_operations(self):
        self.assertIsInstance(self.calculator.operations["1"], Addition)
        self.assertIsInstance(self.calculator.operations["2"], Multiplication)
        self.assertIsInstance(self.calculator.operations["3"], Division)
        self.assertIsInstance(self.calculator.operations["4"], Subtraction)
        self.assertIsInstance(self.calculator.operations["5"], Power)

    def test_calculate_addition(self):
        self.assertTrue(self.calculator.calculate("1", 2, 3))

    def test_calculate_multiplication(self):
        self.assertTrue(self.calculator.calculate("2", 2, 3))

    def test_calculate_division(self):
        self.assertTrue(self.calculator.calculate("3", 6, 2))

    def test_calculate_subtraction(self):
        self.assertTrue(self.calculator.calculate("4", 5, 3))

    def test_calculate_power(self):
        self.assertTrue(self.calculator.calculate("5", 2, 3))

    def test_calculate_exit(self):
        self.assertFalse(self.calculator.calculate("0", 0, 0))

    def test_calculate_invalid_choice(self):
        self.assertTrue(self.calculator.calculate("9", 0, 0))

    def test_calculate_division_by_zero(self):
        self.assertTrue(self.calculator.calculate("3", 5, 0))


class TestInheritance(unittest.TestCase):
    def test_operations_inherit_from_operation(self):
        self.assertIsInstance(Addition(), Operation)
        self.assertIsInstance(Multiplication(), Operation)
        self.assertIsInstance(Division(), Operation)
        self.assertIsInstance(Subtraction(), Operation)
        self.assertIsInstance(Power(), Operation)


if __name__ == "__main__":
    unittest.main()