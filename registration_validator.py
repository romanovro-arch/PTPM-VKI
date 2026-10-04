import re
import string
from typing import Tuple

PHONE_REGEX = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$")
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
)
STRING_LOGIN_ALLOWED_CHARS = re.compile(r"^[a-zA-Z0-9_]+$")

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


class RegistrationValidator:

    def validate(self, login: str, password: str, password_confirm: str) -> Tuple[bool, str]:
        if not isinstance(login, str) or not isinstance(password, str) or not isinstance(password_confirm, str):
            return False, "Все входные параметры должны быть строками."

        if not login.strip():
            return False, "Логин не может быть пустым."

        clean_login = login.strip()

        if clean_login.lower() in BLACKLISTED_LOGINS:
            return False, f"Логин '{clean_login}' находится в списке запрещенных имен."

        if clean_login.startswith("+"):
            if not PHONE_REGEX.match(clean_login):
                return False, "Некорректный формат телефона. Ожидается маска: +x-xxx-xxx-xxxx."
        elif "@" in clean_login:
            if not EMAIL_REGEX.match(clean_login):
                return False, "Некорректный формат email."
        else:
            if not STRING_LOGIN_ALLOWED_CHARS.match(clean_login):
                return False, "Недопустимые символы в логине. Разрешены только латиница, цифры и _."
            if len(clean_login) < 5:
                return False, "Длина строкового логина должна составлять не менее 5 символов."

        if len(password) < 7:
            return False, "Длина пароля должна составлять не менее 7 символов."

        if not CYRILLIC_PASSWORD_ALLOWED_CHARS.match(password):
            return False, "Пароль содержит запрещенные символы. Разрешены только кириллица, цифры и спецсимволы."

        if not CYRILLIC_UPPERCASE_REGEX.search(password):
            return False, "Пароль должен содержать как минимум одну заглавную букву кириллицы."

        if not CYRILLIC_LOWERCASE_REGEX.search(password):
            return False, "Пароль должен содержать как минимум одну строчную букву кириллицы."

        if not DIGIT_REGEX.search(password):
            return False, "Пароль должен содержать как минимум одну цифру."

        if not SPECIAL_CHAR_REGEX.search(password):
            return False, "Пароль должен содержать как минимум один специальный символ."

        if password != password_confirm:
            return False, "Пароль и подтверждение пароля не совпадают."

        return True, ""
