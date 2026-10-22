"""
Интеграционные тесты для Лабораторной работы № 3.
Проверяют совместную работу компонентов с реальной базой данных SQLite
и имитацией пользовательского ввода / сторонней зависимости.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
for p in (str(SRC_DIR), str(BASE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import unittest

try:
    from controller import RegistrationController
    from database import DatabaseManager
    from external_service import EmailNotificationService
    from registration_validator import RegistrationValidator
    from user_interface import UserInterface
except ImportError:
    from src.controller import RegistrationController
    from src.database import DatabaseManager
    from src.external_service import EmailNotificationService
    from src.registration_validator import RegistrationValidator
    from src.user_interface import UserInterface


class TestRegistrationIntegration(unittest.TestCase):
    """
    Комплекс интеграционных тестов (не менее 3 по ТЗ), проверяющий
    сквозные сценарии взаимодействия Controller, DatabaseManager,
    RegistrationValidator, UserInterface и ExternalService.
    """

    def setUp(self):
        """Подготовка изолированной базы данных SQLite в памяти для каждого теста."""
        self.db = DatabaseManager(":memory:")
        self.validator = RegistrationValidator()
        self.external_service = EmailNotificationService()

    def tearDown(self):
        """Очистка ресурсов после выполнения каждого теста."""
        self.db.close()

    def test_integration_successful_registration_saves_to_db_and_notifies_external_service(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ 1:
        Сквозной сценарий успешной регистрации нового пользователя:
        1. Пользователь вводит валидные данные (+7-999-123-4567, Пароль1!).
        2. Контроллер проверяет БД: записи нет.
        3. Контроллер вызывает валидатор: валидация успешна.
        4. Запись физически сохраняется в реальную базу данных SQLite.
        5. Внешний сервис получает уведомление со статусом SUCCESS и источником CALCULATION.
        6. Контроллер возвращает (True, "").
        """
        # Заглушка пользовательского интерфейса (эмуляция ввода)
        mock_ui = MagicMock(spec=UserInterface)
        mock_ui.get_user_input.return_value = (
            "+7-999-123-4567",
            "Пароль1!",
            "Пароль1!"
        )

        controller = RegistrationController(
            ui=mock_ui,
            db=self.db,
            validator=self.validator,
            external_service=self.external_service
        )

        success, error_message = controller.run_registration()

        # 1. Проверка возвращаемого значения
        self.assertTrue(success)
        self.assertEqual(error_message, "")

        # 2. Проверка, что запись физически появилась в реальной SQLite БД
        saved_record = self.db.get_record("+7-999-123-4567", "Пароль1!", "Пароль1!")
        self.assertIsNotNone(saved_record)
        self.assertEqual(saved_record["login"], "+7-999-123-4567")
        self.assertTrue(saved_record["auth_result"])
        self.assertEqual(saved_record["error_message"], "")

        # 3. Проверка передачи данных сторонней зависимости
        self.assertEqual(len(self.external_service.sent_payloads), 1)
        payload = self.external_service.sent_payloads[0]
        self.assertIn("USER:+7-999-123-4567", payload)
        self.assertIn("RESULT:SUCCESS", payload)
        self.assertIn("SOURCE:CALCULATION", payload)

    def test_integration_cached_database_record_bypasses_validator_calculation(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ 2:
        Сценарий повторного обращения (кэширование в БД):
        1. В БД уже присутствует предварительно сохраненная запись.
        2. Пользователь повторно запрашивает операцию с теми же данными.
        3. Контроллер находит запись в БД и берет результат из БД.
        4. Валидатор НЕ вызывается повторно (проверяется вызовом mock-шпиона).
        5. Внешний сервис получает уведомление с источником SOURCE:DATABASE.
        """
        # Предварительно добавляем запись в БД
        self.db.add_record(
            login="student@vki.nsu.ru",
            password="Учеба2026%",
            password_confirm="Учеба2026%",
            auth_result=True,
            error_message=""
        )

        mock_ui = MagicMock(spec=UserInterface)
        mock_ui.get_user_input.return_value = (
            "student@vki.nsu.ru",
            "Учеба2026%",
            "Учеба2026%"
        )

        # Подменяем валидатор шпионом для проверки факта вызова
        spy_validator = MagicMock(spec=RegistrationValidator)

        controller = RegistrationController(
            ui=mock_ui,
            db=self.db,
            validator=spy_validator,
            external_service=self.external_service
        )

        success, error_message = controller.run_registration()

        # 1. Результат успешно получен из базы данных
        self.assertTrue(success)
        self.assertEqual(error_message, "")

        # 2. Валидатор НЕ должен был вызываться, так как данные взяты из БД
        spy_validator.validate.assert_not_called()

        # 3. Внешний сервис получил уведомление о том, что источник - БД
        self.assertEqual(len(self.external_service.sent_payloads), 1)
        payload = self.external_service.sent_payloads[0]
        self.assertIn("USER:student@vki.nsu.ru", payload)
        self.assertIn("RESULT:SUCCESS", payload)
        self.assertIn("SOURCE:DATABASE", payload)

    def test_integration_failed_registration_persists_error_to_database(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ 3:
        Сценарий некорректных учетных данных:
        1. Пользователь передает невалидный пароль (без кириллицы и спецсимволов).
        2. Валидатор вычисляет ошибку.
        3. В базе данных создается запись с auth_result=False и текстом ошибки.
        4. Внешний сервис уведомляется о сбое операции (FAILED).
        5. Контроллер возвращает (False, текст_ошибки).
        """
        mock_ui = MagicMock(spec=UserInterface)
        mock_ui.get_user_input.return_value = (
            "valid_user_99",
            "weak123",
            "weak123"
        )

        controller = RegistrationController(
            ui=mock_ui,
            db=self.db,
            validator=self.validator,
            external_service=self.external_service
        )

        success, error_message = controller.run_registration()

        # 1. Контроллер вернул ошибку
        self.assertFalse(success)
        self.assertIn("прописную букву кириллицы", error_message)

        # 2. Неуспешная запись зафиксирована в SQLite БД
        saved_record = self.db.get_record("valid_user_99", "weak123", "weak123")
        self.assertIsNotNone(saved_record)
        self.assertFalse(saved_record["auth_result"])
        self.assertIn("прописную букву кириллицы", saved_record["error_message"])

        # 3. Внешний сервис получил уведомление о сбое регистрации
        self.assertEqual(len(self.external_service.sent_payloads), 1)
        payload = self.external_service.sent_payloads[0]
        self.assertIn("USER:valid_user_99", payload)
        self.assertIn("RESULT:FAILED", payload)

    def test_integration_database_crud_lifecycle(self):
        """
        ИНТЕГРАЦИОННЫЙ ТЕСТ 4:
        Проверка полного жизненного цикла (CRUD) в DatabaseManager:
        добавление, точный поиск по составному ключу (логин, пароль, подтверждение)
        и удаление записи.
        """
        login = "user_crud_test"
        pwd = "Пароль123!"
        confirm = "Пароль123!"

        # 1. Записи нет
        self.assertIsNone(self.db.get_record(login, pwd, confirm))

        # 2. Добавление записи
        self.db.add_record(login, pwd, confirm, auth_result=True, error_message="")
        record = self.db.get_record(login, pwd, confirm)
        self.assertIsNotNone(record)
        self.assertEqual(record["login"], login)
        self.assertTrue(record["auth_result"])

        # 3. Поиск с несовпадающим подтверждением пароля возвращает None
        self.assertIsNone(self.db.get_record(login, pwd, "ДругойПароль!"))

        # 4. Удаление записи
        deleted = self.db.delete_record(login, pwd, confirm)
        self.assertTrue(deleted)

        # 5. Повторная выборка подтверждает отсутствие
        self.assertIsNone(self.db.get_record(login, pwd, confirm))

        # 6. Повторное удаление возвращает False
        self.assertFalse(self.db.delete_record(login, pwd, confirm))


if __name__ == "__main__":
    unittest.main()
