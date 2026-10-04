import sqlite3
from typing import Optional, Dict, Any


class UserDatabase:

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS registrations (
                    login TEXT NOT NULL,
                    password TEXT NOT NULL,
                    password_confirm TEXT NOT NULL,
                    is_success INTEGER NOT NULL,
                    error_message TEXT,
                    PRIMARY KEY (login, password, password_confirm)
                )
                """
            )

    def add_record(
        self,
        login: str,
        password: str,
        password_confirm: str,
        is_success: bool,
        error_message: str = ""
    ) -> bool:
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO registrations (login, password, password_confirm, is_success, error_message)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(login, password, password_confirm) DO UPDATE SET
                        is_success = excluded.is_success,
                        error_message = excluded.error_message
                    """,
                    (login, password, password_confirm, int(is_success), error_message)
                )
            return True
        except sqlite3.Error:
            return False

    def get_record(
        self,
        login: str,
        password: str,
        password_confirm: str
    ) -> Optional[Dict[str, Any]]:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT login, password, password_confirm, is_success, error_message
            FROM registrations
            WHERE login = ? AND password = ? AND password_confirm = ?
            """,
            (login, password, password_confirm)
        )
        row = cursor.fetchone()
        if row:
            return {
                "login": row["login"],
                "password": row["password"],
                "password_confirm": row["password_confirm"],
                "is_success": bool(row["is_success"]),
                "error_message": row["error_message"] or ""
            }
        return None

    def delete_record(
        self,
        login: str,
        password: str,
        password_confirm: str
    ) -> bool:
        try:
            with self.connection:
                cursor = self.connection.execute(
                    """
                    DELETE FROM registrations
                    WHERE login = ? AND password = ? AND password_confirm = ?
                    """,
                    (login, password, password_confirm)
                )
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def close(self) -> None:
        self.connection.close()
