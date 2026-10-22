"""
Модуль класса-контроллера (Лабораторная работа № 3).
Класс-контроллер (Controller) (п. 'e' ТЗ).
"""

from typing import Tuple

try:
    from database import DatabaseManager
    from external_service import ExternalService
    from registration_validator import RegistrationValidator
    from user_interface import UserInterface
except ImportError:
    from src.database import DatabaseManager
    from src.external_service import ExternalService
    from src.registration_validator import RegistrationValidator
    from src.user_interface import UserInterface


class RegistrationController:
    """
    Класс-контроллер (Controller) сквозного сценария бизнес-логики (п. 'e' ТЗ).
    Объединяет все компоненты и управляет их взаимодействием.
    """

    def __init__(
        self,
        ui: UserInterface,
        db: DatabaseManager,
        validator: RegistrationValidator,
        external_service: ExternalService
    ):
        """
        Внедрение зависимостей (Dependency Injection) через конструктор контроллера.
        """
        self.ui = ui
        self.db = db
        self.validator = validator
        self.external_service = external_service

    def run_registration(self) -> Tuple[bool, str]:
        """
        Метод реализует сквозной сценарий бизнес-логики:
        1. У пользователя запрашиваются входные данные (через класс взаимодействия).
        2. Осуществляется проверка:
           - если для данных нет записи в БД -> вычисляется результат (через класс вычислений)
             и добавляется запись в БД;
           - если для данных есть запись в БД -> результат берется из БД.
        3. Осуществляется отправка строки-результата сторонней зависимости
           (через класс сторонней зависимости).
        4. Метод возвращает результат выполнения операции.
        """
        # 1. Запрос входных данных у пользователя
        login, password, password_confirm = self.ui.get_user_input()

        # 2. Проверка наличия записи в БД
        existing_record = self.db.get_record(login, password, password_confirm)

        if existing_record is not None:
            # Результат берется из БД
            auth_result = bool(existing_record["auth_result"])
            error_message = existing_record.get("error_message", "") or ""
            data_source = "DATABASE"
        else:
            # Вычисляется результат через класс вычислений (валидации)
            auth_result, error_message = self.validator.validate(
                login, password, password_confirm
            )
            # Добавляется запись в БД
            self.db.add_record(
                login=login,
                password=password,
                password_confirm=password_confirm,
                auth_result=auth_result,
                error_message=error_message
            )
            data_source = "CALCULATION"

        # 3. Отправка строки-результата сторонней зависимости
        status_text = "SUCCESS" if auth_result else f"FAILED ({error_message})"
        result_payload = (
            f"EVENT:REGISTRATION | USER:{login} | RESULT:{status_text} | SOURCE:{data_source}"
        )
        self.external_service.send_notification(result_payload)

        # 4. Возврат результата выполнения операции
        return auth_result, error_message
