from abc import ABC, abstractmethod
from typing import List


class ExternalService(ABC):

    @abstractmethod
    def send_notification(self, payload: str) -> bool:
        pass


class EmailNotificationService(ExternalService):

    def __init__(self, smtp_server: str = "smtp.vki.nsu.ru", port: int = 587):
        self.smtp_server = smtp_server
        self.port = port
        self.sent_payloads: List[str] = []

    def send_notification(self, payload: str) -> bool:
        if not isinstance(payload, str):
            raise TypeError("Данные для отправки сторонней зависимости должны быть строкой")

        self.sent_payloads.append(payload)
        return True
