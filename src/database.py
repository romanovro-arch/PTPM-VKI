"""
Модуль работы с базой данных SQLite (Лабораторная работа № 3).
Класс работы с базой данных (п. 'b' ТЗ).
"""

import sqlite3
from typing import Any, Dict, Optional


class DatabaseManager:
    """
    Класс работы с базой данных в соответствии с п. 'b' ТЗ.
    Реализует методы добавления, получения и удаления данных.
    Каждая запись содержит:
        (логин, пароль, подтверждение_пароля, результат_авторизации, сообщение_об_ошибке)
    и идентифицируется по тройке (логин, пароль, подтверждение_пароля).
    """

    def __init__(self, db_path: str = "registration.db"):
        """
        Инициализирует подключение к SQLite БД.
        Для тестов может использоваться ':memory:'.
        """
        self.db_path = db_path
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        """Создает структуру таблицы registrations, если она отсутствует."""
        query = """
        CREATE TABLE IF NOT EXISTS registrations (
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            password_confirm TEXT NOT NULL,
            auth_result INTEGER NOT NULL,
            error_message TEXT,
            PRIMARY KEY (login, password, password_confirm)
        );
        """
        with self._connection:
            self._connection.execute(query)

    def add_record(
        self,
        login: str,
        password: str,
        password_confirm: str,
        auth_result: bool,
        error_message: str = ""
    ) -> None:
        """
        Метод добавления данных в базу данных.
        При повторном добавлении той же связки обновляет данные (INSERT OR REPLACE).
        """
        query = """
        INSERT OR REPLACE INTO registrations (
            login, password, password_confirm, auth_result, error_message
        ) VALUES (?, ?, ?, ?, ?);
        """
        with self._connection:
            self._connection.execute(
                query,
                (
                    login,
                    password,
                    password_confirm,
                    1 if auth_result else 0,
                    error_message or ""
                )
            )

    def get_record(
        self,
        login: str,
        password: str,
        password_confirm: str
    ) -> Optional[Dict[str, Any]]:
        """
        Метод получения данных из базы данных по идентификатору
        (логин, пароль, подтверждение_пароля).
        Возвращает словарь с полями записи либо None, если запись не найдена.
        """
        query = """
        SELECT login, password, password_confirm, auth_result, error_message
        FROM registrations
        WHERE login = ? AND password = ? AND password_confirm = ?;
        """
        cursor = self._connection.cursor()
        cursor.execute(query, (login, password, password_confirm))
        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "login": row["login"],
            "password": row["password"],
            "password_confirm": row["password_confirm"],
            "auth_result": bool(row["auth_result"]),
            "error_message": row["error_message"] or ""
        }

    def delete_record(
        self,
        login: str,
        password: str,
        password_confirm: str
    ) -> bool:
        """
        Метод удаления данных из базы данных по идентификатору
        (логин, пароль, подтверждение_пароля).
        Возвращает True, если запись была удалена, иначе False.
        """
        query = """
        DELETE FROM registrations
        WHERE login = ? AND password = ? AND password_confirm = ?;
        """
        with self._connection:
            cursor = self._connection.execute(query, (login, password, password_confirm))
            return cursor.rowcount > 0

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        if self._connection:
            self._connection.close()
