import os
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.database import DatabaseRepository
from src.parser import ForumParser


def run_demo():
    print("=" * 70)
    print("Лабораторная работа №5: Автоматизированный сбор данных и тестирование")
    print("=" * 70)

    db_path = "comments.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    fixture_path = Path(__file__).resolve().parent / "tests" / "fixtures" / "forum_mock.html"
    if not fixture_path.exists():
        print(f"Ошибка: файл фикстуры {fixture_path} не найден.")
        return

    with open(fixture_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = ForumParser()
    print("\n[1] Парсинг HTML-содержимого страницы...")
    parsed_posts = parser.parse_html(html_content)
    print(f"  Успешно извлечено постов: {len(parsed_posts)}")

    for post in parsed_posts:
        print(f"    - ID: {post['id']}, Автор: {post['name']}")

    print(f"\n[2] Сохранение данных в базу данных SQLite ({db_path})...")
    with DatabaseRepository(db_path) as repo:
        saved_count = parser.save_to_db(parsed_posts, repo)
        print(f"  Успешно сохранено записей в БД: {saved_count}")

        print("\n[3] Демонстрация метода get_by_id(101):")
        record = repo.get_by_id(101)
        print(f"  Запись 101: {record}")

        print("\n[4] Демонстрация метода get_by_name('alex_dev'):")
        alex_records = repo.get_by_name("alex_dev")
        print(f"  Найдено сообщений: {len(alex_records)}")
        for r in alex_records:
            print(f"    - ID {r['id']}: {r['message'][:60]}...")

        print("\n[5] Демонстрация метода update(101, ...):")
        repo.update(101, "<p>Обновленное сообщение: BeautifulSoup выбран основным инструментом.</p>")
        updated_record = repo.get_by_id(101)
        print(f"  Новый текст ID 101: {updated_record['message']}")

        print("\n[6] Демонстрация метода delete(104):")
        deleted = repo.delete(104)
        print(f"  Удаление ID 104 успешно: {deleted}")
        remaining = repo.get_by_id(104)
        print(f"  Попытка найти ID 104: {remaining}")

    print("\n" + "=" * 70)
    print("Демонстрация работы модулей успешно завершена.")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
