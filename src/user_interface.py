from abc import ABC, abstractmethod
from typing import Tuple


class UserInterface(ABC):

    @abstractmethod
    def get_user_input(self) -> Tuple[str, str, str]:
        pass


class ConsoleUserInterface(UserInterface):

    def get_user_input(self) -> Tuple[str, str, str]:
        print("\n--- Регистрация нового пользователя ---")
        login = input("Введите логин (телефон +x-xxx-xxx-xxxx, email или имя от 3 символов): ")
        password = input("Введите пароль: ")
        password_confirm = input("Подтвердите пароль: ")
        return login, password, password_confirm
