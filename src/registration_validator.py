import re
from typing import Tuple


class RegistrationValidator:

    def validate(self, login: str, password: str, password_confirm: str) -> Tuple[bool, str]:
        if not isinstance(login, str) or not isinstance(password, str) or not isinstance(password_confirm, str):
            return False, "Логин и пароли должны быть строковыми значениями"

        clean_login = login.strip()
        if not clean_login:
            return False, "Логин не может быть пустым"

        blacklist = {"admin", "administrator", "root", "superuser", "moderator", "guest", "system"}
        if clean_login.lower() in blacklist:
            return False, f"Логин '{clean_login}' находится в списке запрещенных имен"

        phone_pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        string_pattern = r"^[a-zA-Z0-9_]{3,}$"

        is_phone = bool(re.match(phone_pattern, clean_login))
        is_email = bool(re.match(email_pattern, clean_login))
        is_string = bool(re.match(string_pattern, clean_login))

        if not (is_phone or is_email or is_string):
            return False, "Логин должен быть телефоном (+x-xxx-xxx-xxxx), email или строкой от 3 символов"

        if password != password_confirm:
            return False, "Пароли не совпадают"

        if len(password) < 6:
            return False, "Пароль должен содержать не менее 6 символов"

        if not re.search(r"[А-ЯЁ]", password):
            return False, "Пароль должен содержать хотя бы одну прописную букву кириллицы"

        if not re.search(r"[а-яё]", password):
            return False, "Пароль должен содержать хотя бы одну строчную букву кириллицы"

        if not re.search(r"\d", password):
            return False, "Пароль должен содержать хотя бы одну цифру"

        if not re.search(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]", password):
            return False, "Пароль должен содержать хотя бы один специальный символ"

        return True, ""
