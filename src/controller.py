from typing import Tuple

from src.database import DatabaseManager
from src.external_service import ExternalService
from src.registration_validator import RegistrationValidator
from src.user_interface import UserInterface


class RegistrationController:

    def __init__(
        self,
        ui: UserInterface,
        db: DatabaseManager,
        validator: RegistrationValidator,
        external_service: ExternalService
    ):
        self.ui = ui
        self.db = db
        self.validator = validator
        self.external_service = external_service

    def run_registration(self) -> Tuple[bool, str]:
        login, password, password_confirm = self.ui.get_user_input()

        existing_record = self.db.get_record(login, password, password_confirm)

        if existing_record is not None:
            auth_result = bool(existing_record["auth_result"])
            error_message = existing_record.get("error_message", "") or ""
            data_source = "DATABASE"
        else:
            auth_result, error_message = self.validator.validate(
                login, password, password_confirm
            )
            self.db.add_record(
                login=login,
                password=password,
                password_confirm=password_confirm,
                auth_result=auth_result,
                error_message=error_message
            )
            data_source = "CALCULATION"

        status_text = "SUCCESS" if auth_result else f"FAILED ({error_message})"
        result_payload = (
            f"EVENT:REGISTRATION | USER:{login} | RESULT:{status_text} | SOURCE:{data_source}"
        )
        self.external_service.send_notification(result_payload)

        return auth_result, error_message
