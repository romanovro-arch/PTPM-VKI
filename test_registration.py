import os
import unittest
from auth_validator import mask_password, validate_registration
from main import register_user, setup_logging


class TestAuthValidator(unittest.TestCase):

    def test_valid_registration_phone(self):
        success, message = validate_registration("+7-999-123-4567", "Привет1!", "Привет1!")
        self.assertTrue(success)
        self.assertEqual(message, "")

    def test_valid_registration_email(self):
        success, message = validate_registration("student@vki.nsu.ru", "Учеба2026%", "Учеба2026%")
        self.assertTrue(success)
        self.assertEqual(message, "")

    def test_valid_registration_string(self):
        success, message = validate_registration("ivan_ivanov_99", "Секрет№7?", "Секрет№7?")
        self.assertTrue(success)
        self.assertEqual(message, "")

    def test_empty_login(self):
        success, message = validate_registration("   ", "Привет1!", "Привет1!")
        self.assertFalse(success)
        self.assertIn("не может быть пустым", message)

    def test_blacklisted_login(self):
        for bad_login in ["admin", "ADMIN", "root", "SuperUser", "moderator"]:
            success, message = validate_registration(bad_login, "Привет1!", "Привет1!")
            self.assertFalse(success)
            self.assertIn("списке запрещенных имен", message)

    def test_invalid_phone_mask(self):
        invalid_phones = [
            "+7-999-123-456",
            "+79991234567",
            "+77-999-123-4567",
            "+7-999-12a-4567",
            "+-999-123-4567",
        ]
        for phone in invalid_phones:
            success, message = validate_registration(phone, "Привет1!", "Привет1!")
            self.assertFalse(success, f"Телефон '{phone}' должен быть признан невалидным")
            self.assertIn("формат телефона", message.lower())

    def test_invalid_email(self):
        invalid_emails = [
            "missing_domain@",
            "@missing_username.com",
            "user@domain",
            "user@.com",
            "user@@doubleat.com",
            "user@domain..com",
        ]
        for email in invalid_emails:
            success, message = validate_registration(email, "Привет1!", "Привет1!")
            self.assertFalse(success, f"Email '{email}' должен быть признан невалидным")
            self.assertIn("формат email", message.lower())

    def test_short_string_login(self):
        for short_login in ["a", "ab", "abc", "abcd"]:
            success, message = validate_registration(short_login, "Привет1!", "Привет1!")
            self.assertFalse(success)
            self.assertIn("не менее 5 символов", message)

    def test_string_login_forbidden_characters(self):
        forbidden_logins = ["user!name", "ivan ivan", "пользователь1", "user-name", "user$"]
        for login in forbidden_logins:
            success, message = validate_registration(login, "Привет1!", "Привет1!")
            self.assertFalse(success)
            self.assertIn("недопустимые символы", message.lower())

    def test_password_too_short(self):
        success, message = validate_registration("valid_user", "Пар1!", "Пар1!")
        self.assertFalse(success)
        self.assertIn("не менее 7 символов", message)

    def test_password_forbidden_characters_latin(self):
        success, message = validate_registration("valid_user", "Password1!", "Password1!")
        self.assertFalse(success)
        self.assertIn("запрещенные символы", message.lower())

    def test_password_missing_uppercase_cyrillic(self):
        success, message = validate_registration("valid_user", "пароль123!", "пароль123!")
        self.assertFalse(success)
        self.assertIn("заглавную букву кириллицы", message)

    def test_password_missing_lowercase_cyrillic(self):
        success, message = validate_registration("valid_user", "ПАРОЛЬ123!", "ПАРОЛЬ123!")
        self.assertFalse(success)
        self.assertIn("строчную букву кириллицы", message)

    def test_password_missing_digit(self):
        success, message = validate_registration("valid_user", "Парольчик!", "Парольчик!")
        self.assertFalse(success)
        self.assertIn("одну цифру", message)

    def test_password_missing_special_character(self):
        success, message = validate_registration("valid_user", "Парольчик123", "Парольчик123")
        self.assertFalse(success)
        self.assertIn("специальный символ", message)

    def test_passwords_mismatch(self):
        success, message = validate_registration("valid_user", "Пароль1!", "Пароль2!")
        self.assertFalse(success)
        self.assertIn("не совпадают", message)

    def test_non_string_types(self):
        success, message = validate_registration(12345, "Пароль1!", "Пароль1!")
        self.assertFalse(success)
        self.assertIn("должны быть строками", message)


class TestPasswordMasking(unittest.TestCase):

    def test_mask_identical_for_same_passwords(self):
        pwd1 = "Пароль1!"
        pwd2 = "Пароль1!"
        self.assertEqual(mask_password(pwd1), mask_password(pwd2))

    def test_mask_different_for_different_passwords(self):
        pwd1 = "Пароль1!"
        pwd2 = "Пароль2!"
        self.assertNotEqual(mask_password(pwd1), mask_password(pwd2))

    def test_plain_password_not_leaked(self):
        pwd = "СекретныйПароль123!"
        mask = mask_password(pwd)
        self.assertNotIn(pwd, mask)
        self.assertTrue(mask.startswith("***"))
        self.assertTrue(mask.endswith("***"))

    def test_empty_and_non_string_mask(self):
        self.assertEqual(mask_password(""), "***[empty]***")
        self.assertEqual(mask_password(None), "***[non-string]***")


class TestLoggingIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup_logging()

    def test_logging_file_created_and_written(self):
        log_file = "logs/file_txt.log"
        secret_pwd = "СекретныйКод1#"

        register_user("test_logger_user", secret_pwd, secret_pwd)
        register_user("test_logger_user", secret_pwd, "ДругойКод2$")

        self.assertTrue(os.path.exists(log_file), "Файл логов logs/file_txt.log должен существовать")

        with open(log_file, "r", encoding="utf-8") as f:
            log_content = f.read()

        self.assertNotIn(secret_pwd, log_content, "Открытый пароль не должен присутствовать в логах!")
        self.assertNotIn("ДругойКод2$", log_content, "Открытый пароль подтверждения не должен присутствовать в логах!")
        self.assertIn("Успешная регистрация", log_content)
        self.assertIn("Неуспешная регистрация", log_content)
        self.assertIn("test_logger_user", log_content)


if __name__ == "__main__":
    unittest.main()
