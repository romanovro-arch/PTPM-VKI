"""
Точка входа в программу (Лабораторная работа № 3).
Инициализирует все классы и запускает контроллер сквозного сценария.
"""

import sys
from pathlib import Path

# Добавляем пути для корректного импорта при любом способе запуска
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
for p in (str(SRC_DIR), str(BASE_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from controller import RegistrationController
    from database import DatabaseManager
    from external_service import EmailNotificationService
    from registration_validator import RegistrationValidator
    from user_interface import ConsoleUserInterface
except ImportError:
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

    # Инициализация конкретных реализаций компонентов
    ui = ConsoleUserInterface()
    db = DatabaseManager("registration.db")
    validator = RegistrationValidator()
    external_service = EmailNotificationService()

    # Инициализация контроллера (Dependency Injection)
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
