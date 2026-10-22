"""
Модуль взаимодействия со сторонней зависимостью (Лабораторная работа № 3).
Класс сторонней зависимости (п. 'd' ТЗ).
"""

from abc import ABC, abstractmethod
from typing import List


class ExternalService(ABC):
    """
    Абстрактный базовый класс интерфейса сторонней зависимости (п. 'd' ТЗ).
    Выступает в роли интерфейса передачи данных внешнему сервису.
    """

    @abstractmethod
    def send_notification(self, payload: str) -> bool:
        """
        Метод передачи строки-результата стороннему процессу.

        Параметры:
            payload (str): Передаваемые данные.

        Возвращает:
            bool: Признак успешной передачи данных.
        """
        pass


class EmailNotificationService(ExternalService):
    """
    Класс реализации взаимодействия со сторонней зависимостью (email-сервером).
    Внутри класса реализуется исключительно имитация передачи данных в соответствии с ТЗ.
    """

    def __init__(self, smtp_server: str = "smtp.vki.nsu.ru", port: int = 587):
        self.smtp_server = smtp_server
        self.port = port
        self.sent_payloads: List[str] = []

    def send_notification(self, payload: str) -> bool:
        """
        Имитирует отправку строки данных на внешний email-сервер.
        """
        if not isinstance(payload, str):
            raise TypeError("Данные для отправки сторонней зависимости должны быть строкой")

        # Имитация передачи данных: фиксируем в журнале отправленных сообщений
        self.sent_payloads.append(payload)
        return True
