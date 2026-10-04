from user_interface import ConsoleUserInterface
from registration_validator import RegistrationValidator
from user_database import UserDatabase
from external_service import EmailNotificationService
from registration_controller import RegistrationController


def main():
    ui = ConsoleUserInterface()
    validator = RegistrationValidator()
    db = UserDatabase("users.db")
    external_service = EmailNotificationService()

    controller = RegistrationController(ui, validator, db, external_service)

    print("=== Система регистрации пользователей (Лабораторная работа №3) ===")
    try:
        success, message = controller.process_registration()
        if success:
            print("\n[+] Регистрация успешно завершена!")
        else:
            print(f"\n[-] Ошибка регистрации: {message}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
