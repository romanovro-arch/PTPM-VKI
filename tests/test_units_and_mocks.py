import unittest
from unittest.mock import MagicMock, patch

from src.controller import RegistrationController
from src.database import DatabaseManager
from src.external_service import EmailNotificationService, ExternalService
from src.registration_validator import RegistrationValidator
from src.user_interface import ConsoleUserInterface, UserInterface


class TestUnitsAndMocks(unittest.TestCase):

    def test_controller_strict_execution_order_with_full_mocks(self):
        mock_ui = MagicMock(spec=UserInterface)
        mock_ui.get_user_input.return_value = ("mock_user", "Pwd123!", "Pwd123!")

        mock_db = MagicMock(spec=DatabaseManager)
        mock_db.get_record.return_value = None

        mock_validator = MagicMock(spec=RegistrationValidator)
        mock_validator.validate.return_value = (True, "")

        mock_external = MagicMock(spec=ExternalService)
        mock_external.send_notification.return_value = True

        controller = RegistrationController(
            ui=mock_ui,
            db=mock_db,
            validator=mock_validator,
            external_service=mock_external
        )

        success, err = controller.run_registration()

        self.assertTrue(success)
        self.assertEqual(err, "")

        mock_ui.get_user_input.assert_called_once()
        mock_db.get_record.assert_called_once_with("mock_user", "Pwd123!", "Pwd123!")
        mock_validator.validate.assert_called_once_with("mock_user", "Pwd123!", "Pwd123!")
        mock_db.add_record.assert_called_once_with(
            login="mock_user",
            password="Pwd123!",
            password_confirm="Pwd123!",
            auth_result=True,
            error_message=""
        )
        mock_external.send_notification.assert_called_once()
        payload = mock_external.send_notification.call_args[0][0]
        self.assertIn("USER:mock_user", payload)
        self.assertIn("RESULT:SUCCESS", payload)

    @patch("builtins.input", side_effect=["+7-999-111-2233", "Тестовый1!", "Тестовый1!"])
    def test_console_user_interface_input_mocking(self, mock_input):
        ui = ConsoleUserInterface()
        login, password, password_confirm = ui.get_user_input()

        self.assertEqual(login, "+7-999-111-2233")
        self.assertEqual(password, "Тестовый1!")
        self.assertEqual(password_confirm, "Тестовый1!")
        self.assertEqual(mock_input.call_count, 3)

    def test_email_notification_service_payload_simulation(self):
        service = EmailNotificationService(smtp_server="smtp.test.local", port=25)
        result = service.send_notification("TEST_PAYLOAD_STRING")

        self.assertTrue(result)
        self.assertEqual(service.sent_payloads, ["TEST_PAYLOAD_STRING"])

        with self.assertRaises(TypeError):
            service.send_notification(12345)

    def test_validator_contract_and_non_string_types(self):
        validator = RegistrationValidator()

        ok, msg = validator.validate(None, "Пароль1!", "Пароль1!")
        self.assertFalse(ok)
        self.assertIn("строковыми значениями", msg)

        ok, msg = validator.validate("   ", "Пароль1!", "Пароль1!")
        self.assertFalse(ok)
        self.assertIn("не может быть пустым", msg)

        ok, msg = validator.validate("user1", "Пароль1!", "Пароль2!")
        self.assertFalse(ok)
        self.assertIn("не совпадают", msg)


if __name__ == "__main__":
    unittest.main()
