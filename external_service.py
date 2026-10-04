from abc import ABC, abstractmethod


class ExternalService(ABC):

    @abstractmethod
    def send_result(self, recipient: str, status: bool, message: str) -> bool:
        pass


class EmailNotificationService(ExternalService):

    def send_result(self, recipient: str, status: bool, message: str) -> bool:
        print(f"[EmailService] Отправка на {recipient}: статус={status}, сообщение='{message}'")
        return True
