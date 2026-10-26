import re
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup

from src.database import DatabaseRepository


class ForumParser:

    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    def __init__(self, user_agent: Optional[str] = None):
        self.headers = {
            "User-Agent": user_agent or self.DEFAULT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def fetch_page(self, url: str, timeout: int = 10) -> str:
        if not isinstance(url, str) or not url.strip():
            raise ValueError("URL должен быть непустой строкой")

        response = requests.get(url, headers=self.headers, timeout=timeout)
        response.raise_for_status()
        return response.text

    def parse_html(self, html_content: str) -> List[Dict[str, Any]]:
        if not html_content or not isinstance(html_content, str):
            return []

        try:
            soup = BeautifulSoup(html_content, "lxml")
        except Exception:
            soup = BeautifulSoup(html_content, "html.parser")

        posts = soup.select(".post, .forum-post, article.post")
        results: List[Dict[str, Any]] = []

        for post in posts:
            post_id_val = post.get("data-post-id")
            if not post_id_val:
                raw_id = post.get("id", "")
                match = re.search(r"\d+", raw_id)
                if match:
                    post_id_val = match.group(0)

            if not post_id_val:
                continue

            try:
                comment_id = int(post_id_val)
            except (ValueError, TypeError):
                continue

            author_elem = post.select_one(".author, .username, .user-name")
            if not author_elem:
                continue
            username = author_elem.get_text(strip=True)
            if not username:
                continue

            message_elem = post.select_one(".post-message, .message, .message-text, .post-text")
            if not message_elem:
                continue

            inner_html = message_elem.decode_contents().strip()
            if not inner_html:
                continue

            results.append({
                "id": comment_id,
                "name": username,
                "message": inner_html
            })

        return results

    def parse_page(self, url: str) -> List[Dict[str, Any]]:
        html = self.fetch_page(url)
        return self.parse_html(html)

    def save_to_db(
        self,
        parsed_data: List[Dict[str, Any]],
        repository: DatabaseRepository,
        ignore_duplicates: bool = False
    ) -> int:
        if not isinstance(repository, DatabaseRepository):
            raise TypeError("repository должен быть экземпляром DatabaseRepository")
        if not isinstance(parsed_data, list):
            raise TypeError("parsed_data должен быть списком словарей")

        saved_count = 0
        for item in parsed_data:
            if not isinstance(item, dict):
                continue
            comment_id = item.get("id")
            name = item.get("name")
            message = item.get("message")

            try:
                repository.add(comment_id=comment_id, username=name, message=message)
                saved_count += 1
            except ValueError as e:
                if ignore_duplicates and "уже существует" in str(e):
                    continue
                raise

        return saved_count
