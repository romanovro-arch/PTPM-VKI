from src.password_validator import validate_password
import unittest

class TestPasswordValidator(unittest.TestCase):
    def test_valid_password_latin(self):
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_password_cyrillic(self):
        self.assertTrue(validate_password("ПарольТест9#"))

    # 2. Граничные значения длины (BVA)
    def test_boundary_length_7(self):
        self.assertFalse(validate_password("Pass1!a"))

    def test_boundary_length_8(self):
        self.assertTrue(validate_password("Pass1!aa"))

    def test_boundary_length_20(self):
        self.assertTrue(validate_password("A" * 16 + "a1!b"))

    def test_boundary_length_21(self):
        self.assertFalse(validate_password("A" * 17 + "a1!b"))

    def test_missing_uppercase(self):
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lowercase(self):
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special_char(self):
        self.assertFalse(validate_password("SecurePassword1"))

    def test_invalid_special_char(self):
        self.assertFalse(validate_password("SecurePass1_"))
        self.assertFalse(validate_password("SecurePass1?"))

    def test_empty_string(self):
        self.assertFalse(validate_password(""))

    def test_spaces_in_password(self):
        with self.assertRaises(ValueError):
            validate_password("Pass 1234!")
        with self.assertRaises(ValueError):
            validate_password(" Pass1234!")
        with self.assertRaises(ValueError):
            validate_password("Pass1234! ")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_password(12345678)
        with self.assertRaises(TypeError):
            validate_password(None)
        with self.assertRaises(TypeError):
            validate_password(["P", "a", "s", "s", "1", "!"])


if __name__ == '__main__':
    unittest.main()