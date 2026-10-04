import unittest
from unittest.mock import Mock, patch

from external_service import EmailNotificationService, ExternalService
from registration_controller import RegistrationController
from registration_validator import RegistrationValidator
from user_database import UserDatabase
from user_interface import ConsoleUserInterface, UserInterface


class TestRegistrationIntegration(unittest.TestCase):

    def setUp(self):
        self.db = UserDatabase(":memory:")
        self.validator = RegistrationValidator()

    def tearDown(self):
        self.db.close()

    def test_integration_successful_registration_end_to_end(self):
        mock_ui = Mock(spec=UserInterface)
        mock_ui.get_user_input.return_value = ("alex_99", "Пароль123!", "Пароль123!")

        mock_external = Mock(spec=ExternalService)
        mock_external.send_result.return_value = True

        controller = RegistrationController(
            ui=mock_ui,
            validator=self.validator,
            db=self.db,
            external_service=mock_external
        )

        success, message = controller.process_registration()

        self.assertTrue(success)
        self.assertEqual(message, "")

        db_record = self.db.get_record("alex_99", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(db_record)
        self.assertTrue(db_record["is_success"])
        self.assertEqual(db_record["error_message"], "")

        mock_ui.get_user_input.assert_called_once()
        mock_external.send_result.assert_called_once_with("alex_99", True, "")

    def test_integration_failed_registration_saves_error_to_database(self):
        mock_ui = Mock(spec=UserInterface)
        mock_ui.get_user_input.return_value = ("alex_99", "Пар1!", "Пар1!")

        mock_external = Mock(spec=ExternalService)
        mock_external.send_result.return_value = True

        controller = RegistrationController(
            ui=mock_ui,
            validator=self.validator,
            db=self.db,
            external_service=mock_external
        )

        success, message = controller.process_registration()

        self.assertFalse(success)
        self.assertIn("не менее 7 символов", message)

        db_record = self.db.get_record("alex_99", "Пар1!", "Пар1!")
        self.assertIsNotNone(db_record)
        self.assertFalse(db_record["is_success"])
        self.assertEqual(db_record["error_message"], message)

        mock_external.send_result.assert_called_once_with("alex_99", False, message)

    def test_integration_cached_record_skips_validation(self):
        self.db.add_record("cached_user", "Пароль123!", "Пароль123!", True, "")

        mock_ui = Mock(spec=UserInterface)
        mock_ui.get_user_input.return_value = ("cached_user", "Пароль123!", "Пароль123!")

        mock_validator = Mock(spec=RegistrationValidator)
        mock_external = Mock(spec=ExternalService)
        mock_external.send_result.return_value = True

        controller = RegistrationController(
            ui=mock_ui,
            validator=mock_validator,
            db=self.db,
            external_service=mock_external
        )

        success, message = controller.process_registration()

        self.assertTrue(success)
        self.assertEqual(message, "")
        mock_validator.validate.assert_not_called()
        mock_external.send_result.assert_called_once_with("cached_user", True, "")

    def test_database_crud_lifecycle(self):
        added = self.db.add_record("+7-999-111-2233", "Секрет1!", "Секрет1!", True, "")
        self.assertTrue(added)

        record = self.db.get_record("+7-999-111-2233", "Секрет1!", "Секрет1!")
        self.assertIsNotNone(record)
        self.assertEqual(record["login"], "+7-999-111-2233")
        self.assertTrue(record["is_success"])

        deleted = self.db.delete_record("+7-999-111-2233", "Секрет1!", "Секрет1!")
        self.assertTrue(deleted)

        record_after_delete = self.db.get_record("+7-999-111-2233", "Секрет1!", "Секрет1!")
        self.assertIsNone(record_after_delete)

        delete_non_existent = self.db.delete_record("ghost_user", "1", "1")
        self.assertFalse(delete_non_existent)

    @patch("builtins.input", side_effect=["ivan_test", "Пароль123!", "Пароль123!"])
    def test_console_user_interface_input_mock(self, mock_input):
        ui = ConsoleUserInterface()
        login, password, confirm = ui.get_user_input()

        self.assertEqual(login, "ivan_test")
        self.assertEqual(password, "Пароль123!")
        self.assertEqual(confirm, "Пароль123!")
        self.assertEqual(mock_input.call_count, 3)

    def test_integration_external_service_exception_handling(self):
        mock_ui = Mock(spec=UserInterface)
        mock_ui.get_user_input.return_value = ("net_user", "Пароль123!", "Пароль123!")

        mock_external = Mock(spec=ExternalService)
        mock_external.send_result.side_effect = ConnectionError("SMTP server down")

        controller = RegistrationController(
            ui=mock_ui,
            validator=self.validator,
            db=self.db,
            external_service=mock_external
        )

        success, message = controller.process_registration()

        self.assertTrue(success)
        self.assertEqual(message, "")

        db_record = self.db.get_record("net_user", "Пароль123!", "Пароль123!")
        self.assertIsNotNone(db_record)
        self.assertTrue(db_record["is_success"])

    def test_email_notification_service_send(self):
        service = EmailNotificationService()
        result = service.send_result("test@example.com", True, "")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
