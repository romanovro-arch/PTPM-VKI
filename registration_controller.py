from typing import Tuple

from user_interface import UserInterface
from registration_validator import RegistrationValidator
from user_database import UserDatabase
from external_service import ExternalService


class RegistrationController:

    def __init__(
        self,
        ui: UserInterface,
        validator: RegistrationValidator,
        db: UserDatabase,
        external_service: ExternalService
    ):
        self.ui = ui
        self.validator = validator
        self.db = db
        self.external_service = external_service

    def process_registration(self) -> Tuple[bool, str]:
        login, password, password_confirm = self.ui.get_user_input()

        cached_record = self.db.get_record(login, password, password_confirm)

        if cached_record is not None:
            is_success = cached_record["is_success"]
            error_message = cached_record["error_message"]
        else:
            is_success, error_message = self.validator.validate(login, password, password_confirm)
            self.db.add_record(login, password, password_confirm, is_success, error_message)

        try:
            self.external_service.send_result(login, is_success, error_message)
        except Exception as e:
            print(f"[RegistrationController] Ошибка отправки уведомления: {e}")

        return is_success, error_message
