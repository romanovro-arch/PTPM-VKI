import hashlib
import logging
import os
import re
import string
import sys
from typing import Tuple

PHONE_REGEX = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
)
STRING_LOGIN_ALLOWED_CHARS = re.compile(r"^[a-zA-Z0-9_]+$")
STRING_LOGIN_REGEX = re.compile(r"^[a-zA-Z0-9_]{5,}$")

BLACKLISTED_LOGINS = {
    "admin",
    "administrator",
    "root",
    "superuser",
    "moderator",
    "guest",
    "null",
    "undefined",
    "test",
    "support",
    "owner",
}

SPECIAL_CHARS = string.punctuation + "№"
CYRILLIC_PASSWORD_ALLOWED_CHARS = re.compile(
    r"^[а-яА-ЯёЁ0-9" + re.escape(SPECIAL_CHARS) + r"]+$"
)
CYRILLIC_UPPERCASE_REGEX = re.compile(r"[А-ЯЁ]")
CYRILLIC_LOWERCASE_REGEX = re.compile(r"[а-яё]")
DIGIT_REGEX = re.compile(r"\d")
SPECIAL_CHAR_REGEX = re.compile(r"[" + re.escape(SPECIAL_CHARS) + r"]")


def mask_password(password: str) -> str:
    """Маскирование пароля для безопасного логирования."""
    if not isinstance(password, str):
        return "***[non-string]***"
    if not password:
        return "***[empty]***"
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()[:8]
    return f"***[len={len(password)}:hash={pw_hash}]***"


def validate_registration(login: str, password: str, password_confirm: str) -> Tuple[bool, str]:
    """
    Валидация учетных данных при регистрации пользователя.
    Возвращает: (успех_проверки, сообщение_об_ошибке)
    """
    if not isinstance(login, str) or not isinstance(password, str) or not isinstance(password_confirm, str):
        return False, "Все входные параметры (логин, пароль, подтверждение) должны быть строками."

    if not login.strip():
        return False, "Логин не может быть пустым."

    clean_login = login.strip()

    if clean_login.lower() in BLACKLISTED_LOGINS:
        return False, f"Логин '{clean_login}' находится в списке запрещенных имен."

    if clean_login.startswith("+"):
        if not PHONE_REGEX.match(clean_login):
            return False, "Некорректный формат телефона. Ожидается маска: +x-xxx-xxx-xxxx (например, +7-999-123-4567)."
    elif "@" in clean_login:
        if not EMAIL_REGEX.match(clean_login):
            return False, "Некорректный формат email. Введенный адрес не соответствует стандартному формату электронной почты."
    else:
        if not STRING_LOGIN_ALLOWED_CHARS.match(clean_login):
            return False, "Недопустимые символы в логине. Разрешены только латинские буквы (a-z, A-Z), цифры (0-9) и символ подчеркивания (_)."
        if len(clean_login) < 5:
            return False, "Длина строкового логина должна составлять не менее 5 символов."

    if len(password) < 7:
        return False, "Длина пароля должна составлять не менее 7 символов."

    if not CYRILLIC_PASSWORD_ALLOWED_CHARS.match(password):
        return False, "Пароль содержит запрещенные символы. Разрешены только буквы кириллицы, цифры и спецсимволы (латиница и пробелы запрещены)."

    if not CYRILLIC_UPPERCASE_REGEX.search(password):
        return False, "Пароль должен содержать как минимум одну заглавную букву кириллицы (А-Я, Ё)."

    if not CYRILLIC_LOWERCASE_REGEX.search(password):
        return False, "Пароль должен содержать как минимум одну строчную букву кириллицы (а-я, ё)."

    if not DIGIT_REGEX.search(password):
        return False, "Пароль должен содержать как минимум одну цифру (0-9)."

    if not SPECIAL_CHAR_REGEX.search(password):
        return False, "Пароль должен содержать как минимум один специальный символ (например: ! @ # $ % ^ & * _ -)."

    if password != password_confirm:
        return False, "Пароль и подтверждение пароля не совпадают."

    return True, ""


# =====================================================================
# СЕРВИС ЛОГИРОВАНИЯ И ИНТЕРФЕЙС (ИЗ MAIN.PY)
# =====================================================================

def setup_logging(console: bool = True) -> None:
    """Конфигурация сквозного логирования."""
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handlers = [
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]

    if console:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )

    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")


def register_user(login: str, password: str, password_confirm: str) -> Tuple[bool, str]:
    """Регистрация пользователя с логированием попыток и маскированием паролей."""
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
    """Запуск демонстрационных сценариев валидации и логирования."""
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
    """Интерактивное консольное меню пользователя."""
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
