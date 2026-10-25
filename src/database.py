import sqlite3
from typing import Any, Dict, Optional


class DatabaseManager:

    def __init__(self, db_path: str = "registration.db"):
        self.db_path = db_path
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
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
        query = """
        DELETE FROM registrations
        WHERE login = ? AND password = ? AND password_confirm = ?;
        """
        with self._connection:
            cursor = self._connection.execute(query, (login, password, password_confirm))
            return cursor.rowcount > 0

    def close(self) -> None:
        if self._connection:
            self._connection.close()
