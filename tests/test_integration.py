import unittest
from unittest.mock import MagicMock

from src.controller import RegistrationController
from src.database import DatabaseManager
from src.external_service import EmailNotificationService
from src.registration_validator import RegistrationValidator
from src.user_interface import UserInterface


class TestRegistrationIntegration(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.validator = RegistrationValidator()
        self.external_service = EmailNotificationService()

    def tearDown(self):
        self.db.close()

    def test_integration_successful_registration_saves_to_db_and_notifies_external_service(self):
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

        self.assertTrue(success)
        self.assertEqual(error_message, "")

        saved_record = self.db.get_record("+7-999-123-4567", "Пароль1!", "Пароль1!")
        self.assertIsNotNone(saved_record)
        self.assertEqual(saved_record["login"], "+7-999-123-4567")
        self.assertTrue(saved_record["auth_result"])
        self.assertEqual(saved_record["error_message"], "")

        self.assertEqual(len(self.external_service.sent_payloads), 1)
        payload = self.external_service.sent_payloads[0]
        self.assertIn("USER:+7-999-123-4567", payload)
        self.assertIn("RESULT:SUCCESS", payload)
        self.assertIn("SOURCE:CALCULATION", payload)

    def test_integration_cached_database_record_bypasses_validator_calculation(self):
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

        spy_validator = MagicMock(spec=RegistrationValidator)

        controller = RegistrationController(
            ui=mock_ui,
            db=self.db,
            validator=spy_validator,
            external_service=self.external_service
        )

        success, error_message = controller.run_registration()

        self.assertTrue(success)
        self.assertEqual(error_message, "")

        spy_validator.validate.assert_not_called()

        self.assertEqual(len(self.external_service.sent_payloads), 1)
        payload = self.external_service.sent_payloads[0]
        self.assertIn("USER:student@vki.nsu.ru", payload)
        self.assertIn("RESULT:SUCCESS", payload)
        self.assertIn("SOURCE:DATABASE", payload)

    def test_integration_failed_registration_persists_error_to_database(self):
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

        self.assertFalse(success)
        self.assertIn("прописную букву кириллицы", error_message)

        saved_record = self.db.get_record("valid_user_99", "weak123", "weak123")
        self.assertIsNotNone(saved_record)
        self.assertFalse(saved_record["auth_result"])
        self.assertIn("прописную букву кириллицы", saved_record["error_message"])

        self.assertEqual(len(self.external_service.sent_payloads), 1)
        payload = self.external_service.sent_payloads[0]
        self.assertIn("USER:valid_user_99", payload)
        self.assertIn("RESULT:FAILED", payload)

    def test_integration_database_crud_lifecycle(self):
        login = "user_crud_test"
        pwd = "Пароль123!"
        confirm = "Пароль123!"

        self.assertIsNone(self.db.get_record(login, pwd, confirm))

        self.db.add_record(login, pwd, confirm, auth_result=True, error_message="")
        record = self.db.get_record(login, pwd, confirm)
        self.assertIsNotNone(record)
        self.assertEqual(record["login"], login)
        self.assertTrue(record["auth_result"])

        self.assertIsNone(self.db.get_record(login, pwd, "ДругойПароль!"))

        deleted = self.db.delete_record(login, pwd, confirm)
        self.assertTrue(deleted)

        self.assertIsNone(self.db.get_record(login, pwd, confirm))

        self.assertFalse(self.db.delete_record(login, pwd, confirm))


if __name__ == "__main__":
    unittest.main()
