"""
Модуль валидации учетных данных пользователя (Лабораторная работа № 3).
Класс вычислений / валидации (п. 'a' ТЗ).
"""

import re
from typing import Tuple


class RegistrationValidator:
    """
    Класс вычислений / валидации в соответствии с п. 'a' ТЗ:
    «Класс с одним методом, который был реализован в задании 'Лабораторная работа №1'».
    """

    def validate(self, login: str, password: str, password_confirm: str) -> Tuple[bool, str]:
        """
        Единственный метод бизнес-логики класса: выполняет валидацию учетных данных.

        Параметры:
            login (str): Логин пользователя (телефон, email или строка).
            password (str): Пароль.
            password_confirm (str): Подтверждение пароля.

        Возвращает:
            Tuple[bool, str]: (Успех: bool, Сообщение об ошибке: str).
                              При успехе возвращает (True, "").
        """
        # 1. Проверка типов входных параметров
        if not isinstance(login, str) or not isinstance(password, str) or not isinstance(password_confirm, str):
            return False, "Логин и пароли должны быть строковыми значениями"

        # 2. Проверка пустого логина
        clean_login = login.strip()
        if not clean_login:
            return False, "Логин не может быть пустым"

        # 3. Фильтрация по черному списку системных имен
        blacklist = {"admin", "administrator", "root", "superuser", "moderator", "guest", "system"}
        if clean_login.lower() in blacklist:
            return False, f"Логин '{clean_login}' находится в списке запрещенных имен"

        # 4. Проверка формата логина (телефон, email или строковый идентификатор)
        phone_pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        string_pattern = r"^[a-zA-Z0-9_]{3,}$"

        is_phone = bool(re.match(phone_pattern, clean_login))
        is_email = bool(re.match(email_pattern, clean_login))
        is_string = bool(re.match(string_pattern, clean_login))

        if not (is_phone or is_email or is_string):
            return False, "Логин должен быть телефоном (+x-xxx-xxx-xxxx), email или строкой от 3 символов"

        # 5. Проверка совпадения пароля и подтверждения
        if password != password_confirm:
            return False, "Пароли не совпадают"

        # 6. Проверка требований к сложности пароля (ЛР1):
        # - не менее 6 символов;
        # - хотя бы одна заглавная буква кириллицы;
        # - хотя бы одна строчная буква кириллицы;
        # - хотя бы одна цифра;
        # - хотя бы один специальный символ.
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
