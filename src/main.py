from src.controller import RegistrationController
from src.database import DatabaseManager
from src.external_service import EmailNotificationService
from src.registration_validator import RegistrationValidator
from src.user_interface import ConsoleUserInterface


def main():
    print("=" * 65)
    print("Лабораторная работа № 3")
    print("Интеграционное тестирование проектов и работа с тестовыми заглушками")
    print("=" * 65)

    ui = ConsoleUserInterface()
    db = DatabaseManager("registration.db")
    validator = RegistrationValidator()
    external_service = EmailNotificationService()

    controller = RegistrationController(
        ui=ui,
        db=db,
        validator=validator,
        external_service=external_service
    )

    try:
        success, message = controller.run_registration()
        print("\n--- Результат выполнения операции ---")
        if success:
            print("УСПЕХ: Пользователь успешно зарегистрирован!")
        else:
            print(f"ОТКАЗ: Ошибка регистрации: {message}")

        if external_service.sent_payloads:
            print(f"Уведомление внешнему сервису: {external_service.sent_payloads[-1]}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
