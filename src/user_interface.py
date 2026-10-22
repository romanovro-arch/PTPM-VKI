"""
Модуль взаимодействия с пользователем (Лабораторная работа № 3).
Класс взаимодействия с пользователем (п. 'c' ТЗ).
"""

from abc import ABC, abstractmethod
from typing import Tuple


class UserInterface(ABC):
    """
    Абстрактный базовый класс интерфейса взаимодействия с пользователем (п. 'c' ТЗ).
    Выступает в роли строгого интерфейса.
    """

    @abstractmethod
    def get_user_input(self) -> Tuple[str, str, str]:
        """
        Метод получения информации от пользователя.

        Возвращает:
            Tuple[str, str, str]: (логин, пароль, подтверждение_пароля).
        """
        pass


class ConsoleUserInterface(UserInterface):
    """
    Консольная реализация взаимодействия с пользователем через функции ввода input().
    """

    def get_user_input(self) -> Tuple[str, str, str]:
        """
        Запрашивает у пользователя логин, пароль и подтверждение пароля через консоль.
        """
        print("\n--- Регистрация нового пользователя ---")
        login = input("Введите логин (телефон +x-xxx-xxx-xxxx, email или имя от 3 символов): ")
        password = input("Введите пароль: ")
        password_confirm = input("Подтвердите пароль: ")
        return login, password, password_confirm
