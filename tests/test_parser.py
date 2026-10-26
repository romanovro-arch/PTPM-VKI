import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests

from src.database import DatabaseRepository
from src.parser import ForumParser


class TestForumParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fixtures_dir = Path(__file__).resolve().parent / "fixtures"
        cls.fixture_path = fixtures_dir / "forum_mock.html"
        with open(cls.fixture_path, "r", encoding="utf-8") as f:
            cls.fixture_html = f.read()

    def setUp(self):
        self.parser = ForumParser()

    def test_init_default_and_custom_headers(self):
        default_parser = ForumParser()
        self.assertIn("User-Agent", default_parser.headers)
        self.assertIn("Mozilla", default_parser.headers["User-Agent"])

        custom_ua = "MyTestBot/1.0"
        custom_parser = ForumParser(user_agent=custom_ua)
        self.assertEqual(custom_parser.headers["User-Agent"], custom_ua)

    def test_parse_html_with_fixture(self):
        results = self.parser.parse_html(self.fixture_html)

        self.assertEqual(len(results), 4)

        first_post = results[0]
        self.assertEqual(first_post["id"], 101)
        self.assertEqual(first_post["name"], "alex_dev")
        self.assertIn("<strong>BeautifulSoup</strong>", first_post["message"])
        self.assertIn("<em>Scrapy</em>", first_post["message"])

        second_post = results[1]
        self.assertEqual(second_post["id"], 102)
        self.assertEqual(second_post["name"], "maria_qa")
        self.assertIn("<code>requests</code>", second_post["message"])

        third_post = results[2]
        self.assertEqual(third_post["id"], 103)
        self.assertEqual(third_post["name"], "alex_dev")

        fourth_post = results[3]
        self.assertEqual(fourth_post["id"], 104)
        self.assertEqual(fourth_post["name"], "senior_lead")
        self.assertIn("unittest.mock.patch", fourth_post["message"])

    def test_parse_html_empty_and_none(self):
        self.assertEqual(self.parser.parse_html(""), [])
        self.assertEqual(self.parser.parse_html(None), [])
        self.assertEqual(self.parser.parse_html(12345), [])

    def test_parse_html_no_matching_elements(self):
        sample_html = "<html><body><h1>Title</h1><p>No posts here</p></body></html>"
        self.assertEqual(self.parser.parse_html(sample_html), [])

    def test_parse_html_skips_malformed_posts(self):
        malformed_html = """
        <div class="post">
            <span class="author">no_id_user</span>
            <div class="post-message">Message without ID</div>
        </div>
        <div class="post" data-post-id="not-a-number">
            <span class="author">invalid_id_user</span>
            <div class="post-message">Message with invalid ID</div>
        </div>
        <div class="post" data-post-id="201">
            <div class="post-message">Message without author</div>
        </div>
        <div class="post" data-post-id="202">
            <span class="author">no_msg_user</span>
        </div>
        <div class="post" data-post-id="203">
            <span class="author">valid_user</span>
            <div class="post-message">Valid text</div>
        </div>
        """
        results = self.parser.parse_html(malformed_html)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], 203)
        self.assertEqual(results[0]["name"], "valid_user")
        self.assertEqual(results[0]["message"], "Valid text")

    def test_parse_html_extracts_id_from_element_id_attribute(self):
        html = """
        <div class="post" id="post-777">
            <span class="author">charlie</span>
            <div class="post-message">Parsed by id attr</div>
        </div>
        """
        results = self.parser.parse_html(html)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], 777)
        self.assertEqual(results[0]["name"], "charlie")
        self.assertEqual(results[0]["message"], "Parsed by id attr")

    @patch("src.parser.requests.get")
    def test_fetch_page_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Mocked page</h1></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = "https://example.com/forum/topic/1"
        result = self.parser.fetch_page(url)

        self.assertEqual(result, "<html><body><h1>Mocked page</h1></body></html>")
        mock_get.assert_called_once_with(url, headers=self.parser.headers, timeout=10)
        mock_response.raise_for_status.assert_called_once()

    def test_fetch_page_invalid_url_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.parser.fetch_page("")
        with self.assertRaises(ValueError):
            self.parser.fetch_page("   ")
        with self.assertRaises(ValueError):
            self.parser.fetch_page(None)

    @patch("src.parser.requests.get")
    def test_fetch_page_http_error_raises_exception(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.parser.fetch_page("https://example.com/not-found")

    @patch("src.parser.requests.get")
    def test_fetch_page_connection_error_raises_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.parser.fetch_page("https://offline-domain-test.local")

    @patch.object(ForumParser, "fetch_page")
    def test_parse_page(self, mock_fetch):
        mock_fetch.return_value = self.fixture_html
        results = self.parser.parse_page("https://mock-forum.org/topic/42")

        mock_fetch.assert_called_once_with("https://mock-forum.org/topic/42")
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["id"], 101)

    def test_save_to_db_success(self):
        with DatabaseRepository(":memory:") as repo:
            parsed = self.parser.parse_html(self.fixture_html)
            saved_count = self.parser.save_to_db(parsed, repo)

            self.assertEqual(saved_count, 4)
            post101 = repo.get_by_id(101)
            self.assertIsNotNone(post101)
            self.assertEqual(post101["name"], "alex_dev")

            alex_posts = repo.get_by_name("alex_dev")
            self.assertEqual(len(alex_posts), 2)

    def test_save_to_db_duplicate_behavior(self):
        with DatabaseRepository(":memory:") as repo:
            parsed = self.parser.parse_html(self.fixture_html)
            self.parser.save_to_db(parsed, repo)

            with self.assertRaises(ValueError):
                self.parser.save_to_db(parsed, repo, ignore_duplicates=False)

            ignored_count = self.parser.save_to_db(parsed, repo, ignore_duplicates=True)
            self.assertEqual(ignored_count, 0)

    def test_save_to_db_invalid_arguments_raise_type_error(self):
        parsed = self.parser.parse_html(self.fixture_html)
        with self.assertRaises(TypeError):
            self.parser.save_to_db(parsed, "not-a-repo")

        with DatabaseRepository(":memory:") as repo:
            with self.assertRaises(TypeError):
                self.parser.save_to_db("not-a-list", repo)


if __name__ == "__main__":
    unittest.main()
