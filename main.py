import os
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import requests
from src.database import DatabaseRepository
from src.parser import ForumParser


def run_demo():
    print("=" * 75)
    print("Лабораторная работа №5: Автоматизированный сбор данных и тестирование")
    print("=" * 75)

    db_path = "comments.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    parser = ForumParser()

    print("\n[ЭТАП 1: Оффлайн-демонстрация на локальной фикстуре]")
    fixture_path = Path(__file__).resolve().parent / "tests" / "fixtures" / "forum_mock.html"
    if fixture_path.exists():
        with open(fixture_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        parsed_fixture = parser.parse_html(html_content)
        print(f"  Извлечено постов из фикстуры: {len(parsed_fixture)}")

        with DatabaseRepository(db_path) as repo:
            saved_count = parser.save_to_db(parsed_fixture, repo)
            print(f"  Сохранено в базу данных: {saved_count}")

            print("  Проверка get_by_id(101):", repo.get_by_id(101))
            alex_posts = repo.get_by_name("alex_dev")
            print(f"  Проверка get_by_name('alex_dev'): найдено {len(alex_posts)}")

            repo.update(101, "<p>Обновлено: парсер успешно поддерживает Habr и форумную верстку.</p>")
            print("  Проверка update(101):", repo.get_by_id(101)["message"])

            repo.delete(104)
            print("  Проверка delete(104): запись удалена, get_by_id(104) ->", repo.get_by_id(104))

    print("\n" + "-" * 75)
    print("[ЭТАП 2: Онлайн-сбор реальных данных с Habr]")
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://habr.com/ru/articles/1103460/comments/"
    print(f"  Целевой URL: {target_url}")

    try:
        print("  Отправка HTTP-запроса с заголовком User-Agent...")
        habr_posts = parser.parse_page(target_url)
        print(f"  Успешно извлечено живых комментариев с Habr: {len(habr_posts)}")

        if habr_posts:
            print("\n  Примеры собранных комментариев:")
            for p in habr_posts[:3]:
                clean_preview = p["message"].replace("\n", " ")[:70]
                print(f"    - ID: {p['id']:<10} | Автор: {p['name']:<18} | Текст: {clean_preview}...")

            with DatabaseRepository(db_path) as repo:
                saved_habr = parser.save_to_db(habr_posts, repo, ignore_duplicates=True)
                print(f"\n  Сохранено живых комментариев в SQLite ({db_path}): {saved_habr}")

                first_id = habr_posts[0]["id"]
                db_record = repo.get_by_id(first_id)
                print(f"  Проверка чтения из БД по первому ID ({first_id}):")
                print(f"    Автор: {db_record['name']}")
                print(f"    Длина HTML-сообщения: {len(db_record['message'])} симв.")
    except requests.RequestException as e:
        print(f"  Внимание: Сетевой запрос к Habr не выполнен ({e}).")
        print("  Оффлайн-режим и база данных отработали штатно.")

    print("\n" + "=" * 75)
    print("Демонстрация работы завершена.")
    print("=" * 75)


if __name__ == "__main__":
    run_demo()
