import sqlite3
from typing import Any, Dict, List, Optional


class DatabaseRepository:

    def __init__(self, db_path: str = "comments.db"):
        self.db_path = db_path
        self._connection = sqlite3.connect(self.db_path)
        self._connection.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """
        with self._connection:
            self._connection.execute(query)

    def add(self, comment_id: int, username: str, message: str) -> bool:
        if isinstance(comment_id, bool) or not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом")
        if not isinstance(username, str):
            raise TypeError("username должен быть строкой")
        if not isinstance(message, str):
            raise TypeError("message должен быть строкой")

        if comment_id <= 0:
            raise ValueError("comment_id должен быть положительным числом")

        clean_username = username.strip()
        if not clean_username:
            raise ValueError("username не может быть пустым")
        if len(clean_username) > 256:
            raise ValueError("Длина username не может превышать 256 символов")

        clean_message = message.strip()
        if not clean_message:
            raise ValueError("message не может быть пустым")
        if len(clean_message) > 8096:
            raise ValueError("Длина message не может превышать 8096 символов")

        query = "INSERT INTO comments (id, name, message) VALUES (?, ?, ?);"
        try:
            with self._connection:
                self._connection.execute(query, (comment_id, clean_username, clean_message))
            return True
        except sqlite3.IntegrityError:
            raise ValueError(f"Запись с id={comment_id} уже существует")

    def get_by_id(self, comment_id: int) -> Optional[Dict[str, Any]]:
        if isinstance(comment_id, bool) or not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом")

        query = "SELECT id, name, message FROM comments WHERE id = ?;"
        cursor = self._connection.cursor()
        cursor.execute(query, (comment_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row["id"],
            "name": row["name"],
            "message": row["message"]
        }

    def get_by_name(self, username: str) -> List[Dict[str, Any]]:
        if not isinstance(username, str):
            raise TypeError("username должен быть строкой")

        query = "SELECT id, name, message FROM comments WHERE name = ? ORDER BY id ASC;"
        cursor = self._connection.cursor()
        cursor.execute(query, (username.strip(),))
        rows = cursor.fetchall()

        return [
            {
                "id": r["id"],
                "name": r["name"],
                "message": r["message"]
            }
            for r in rows
        ]

    def update(self, comment_id: int, new_message: str) -> bool:
        if isinstance(comment_id, bool) or not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом")
        if not isinstance(new_message, str):
            raise TypeError("new_message должен быть строкой")

        clean_message = new_message.strip()
        if not clean_message:
            raise ValueError("message не может быть пустым")
        if len(clean_message) > 8096:
            raise ValueError("Длина message не может превышать 8096 символов")

        if self.get_by_id(comment_id) is None:
            raise KeyError(f"Запись с id={comment_id} не найдена")

        query = "UPDATE comments SET message = ? WHERE id = ?;"
        with self._connection:
            cursor = self._connection.execute(query, (clean_message, comment_id))
            return cursor.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        if isinstance(comment_id, bool) or not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом")

        query = "DELETE FROM comments WHERE id = ?;"
        with self._connection:
            cursor = self._connection.execute(query, (comment_id,))
            return cursor.rowcount > 0

    def close(self) -> None:
        if self._connection:
            self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
