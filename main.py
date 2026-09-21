import logging
import os
import sys
from typing import Tuple

from auth_validator import mask_password, validate_registration


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")


def register_user(login: str, password: str, password_confirm: str) -> Tuple[bool, str]:
    masked_pw = mask_password(password)
    masked_confirm = mask_password(password_confirm)

    logging.debug(
        f"Получен запрос на регистрацию | login='{login}' | password={masked_pw} | password_confirm={masked_confirm}"
    )

    try:
        is_success, message = validate_registration(login, password, password_confirm)

        if is_success:
            logging.info(
                f"Успешная регистрация | login='{login}' | password={masked_pw} | результат: УСПЕХ"
            )
            return True, ""
        else:
            logging.warning(
                f"Неуспешная регистрация | login='{login}' | password={masked_pw} | "
                f"password_confirm={masked_confirm} | причина='{message}'"
            )
            return False, message

    except Exception as ex:
        logging.error(
            f"Критический сбой при регистрации пользователя login='{login}' | password={masked_pw}"
        )
        logging.exception("Заход в блок обработки исключения:")
        return False, f"Внутренний сбой системы: {ex}"


def run_demo_scenarios() -> None:
    print("\n" + "=" * 70)
    print("ЗАПУСК ДЕМОНСТРАЦИОННЫХ СЦЕНАРИЕВ ВАЛИДАЦИИ И ЛОГИРОВАНИЯ")
    print("=" * 70 + "\n")

    demo_cases = [
        ("alex_99", "Пароль1!", "Пароль1!", "1. Успешная регистрация (строковый логин)"),
        ("+7-999-123-4567", "Секрет№7", "Секрет№7", "2. Успешная регистрация (телефон)"),
        ("student@vki.nsu.ru", "Учеба2026%", "Учеба2026%", "3. Успешная регистрация (email)"),
        ("admin", "Пароль1!", "Пароль1!", "4. Логин из черного списка"),
        ("+7-999-00", "Пароль1!", "Пароль1!", "5. Неверная маска телефона"),
        ("bad_email@", "Пароль1!", "Пароль1!", "6. Неверный формат email"),
        ("cat", "Пароль1!", "Пароль1!", "7. Слишком короткий строковый логин (<5 симв.)"),
        ("user!name", "Пароль1!", "Пароль1!", "8. Запрещенные знаки в строковом логине"),
        ("valid_user", "Пар1!", "Пар1!", "9. Пароль короче 7 символов"),
        ("valid_user", "Password1!", "Password1!", "10. Пароль содержит латиницу (запрещено)"),
        ("valid_user", "парольбеззаглавной1!", "парольбеззаглавной1!", "11. Нет заглавной кириллицы"),
        ("valid_user", "ПАРОЛЬБЕЗСТРОЧНОЙ1!", "ПАРОЛЬБЕЗСТРОЧНОЙ1!", "12. Нет строчной кириллицы"),
        ("valid_user", "ПарольБезЦифр!", "ПарольБезЦифр!", "13. Нет цифры"),
        ("valid_user", "ПарольБезСпецСимвола1", "ПарольБезСпецСимвола1", "14. Нет спецсимвола"),
        ("valid_user", "Пароль1!", "Пароль2!", "15. Несовпадение пароля и подтверждения (разные маски в логах)"),
    ]

    for login, pwd, confirm, description in demo_cases:
        print(f"--- Тест: {description} ---")
        success, reason = register_user(login, pwd, confirm)
        status_text = "УСПЕХ" if success else f"ОШИБКА ({reason})"
        print(f"Итог: {status_text}\n")


def interactive_menu() -> None:
    while True:
        print("\n--- МЕНЮ РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЯ ---")
        print("1. Зарегистрировать нового пользователя")
        print("2. Запустить демонстрационные сценарии (проверка всех правил и логов)")
        print("3. Просмотреть последние строки файла logs/file_txt.log")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            login = input("Введите логин (телефон +x-xxx-xxx-xxxx, email или строка): ")
            pwd = input("Введите пароль (кириллица, цифры, спецсимвол, >=7 симв.): ")
            confirm = input("Подтвердите пароль: ")
            success, reason = register_user(login, pwd, confirm)
            if success:
                print("\n[+] Регистрация успешно завершена!")
            else:
                print(f"\n[-] Ошибка регистрации: {reason}")
        elif choice == "2":
            run_demo_scenarios()
        elif choice == "3":
            log_path = "logs/file_txt.log"
            if os.path.exists(log_path):
                print("\n--- Содержимое logs/file_txt.log (последние 20 строк) ---")
                with open(log_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines[-20:]:
                        print(line, end="")
            else:
                print("\n[-] Файл логов пока не создан.")
        elif choice == "0":
            logging.info("Пользователь завершил работу программы.")
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите пункт из меню.")


def main() -> None:
    setup_logging()

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo_scenarios()
    else:
        interactive_menu()


Main = main


if __name__ == "__main__":
    main()
