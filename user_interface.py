from abc import ABC, abstractmethod
from typing import Tuple


class UserInterface(ABC):

    @abstractmethod
    def get_user_input(self) -> Tuple[str, str, str]:
        pass


class ConsoleUserInterface(UserInterface):

    def get_user_input(self) -> Tuple[str, str, str]:
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        password_confirm = input("Подтвердите пароль: ")
        return login, password, password_confirm
