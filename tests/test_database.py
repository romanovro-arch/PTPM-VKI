import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    def test_add_success(self):
        result = self.repo.add(1, "alex", "Hello, world!")
        self.assertTrue(result)
        record = self.repo.get_by_id(1)
        self.assertIsNotNone(record)
        self.assertEqual(record["id"], 1)
        self.assertEqual(record["name"], "alex")
        self.assertEqual(record["message"], "Hello, world!")

    def test_add_duplicate_id_raises_value_error(self):
        self.repo.add(1, "alex", "First message")
        with self.assertRaises(ValueError):
            self.repo.add(1, "maria", "Second message with same ID")

    def test_add_invalid_types_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.repo.add("not-an-int", "alex", "Message")

        with self.assertRaises(TypeError):
            self.repo.add(True, "alex", "Message")

        with self.assertRaises(TypeError):
            self.repo.add(2, 12345, "Message")

        with self.assertRaises(TypeError):
            self.repo.add(3, "alex", ["invalid", "message"])

    def test_add_non_positive_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.repo.add(0, "alex", "Zero ID")
        with self.assertRaises(ValueError):
            self.repo.add(-5, "alex", "Negative ID")

    def test_add_empty_name_or_message_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.repo.add(1, "", "Message")
        with self.assertRaises(ValueError):
            self.repo.add(2, "   ", "Message")
        with self.assertRaises(ValueError):
            self.repo.add(3, "alex", "")
        with self.assertRaises(ValueError):
            self.repo.add(4, "alex", "   \n\t  ")

    def test_add_exceeding_length_limits_raises_value_error(self):
        too_long_name = "a" * 257
        with self.assertRaises(ValueError):
            self.repo.add(1, too_long_name, "Message")

        too_long_message = "m" * 8097
        with self.assertRaises(ValueError):
            self.repo.add(2, "alex", too_long_message)

    def test_get_by_id_existing(self):
        self.repo.add(10, "tester", "Content")
        record = self.repo.get_by_id(10)
        self.assertEqual(record, {"id": 10, "name": "tester", "message": "Content"})

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.repo.get_by_id(999))

    def test_get_by_id_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.repo.get_by_id("10")
        with self.assertRaises(TypeError):
            self.repo.get_by_id(False)

    def test_get_by_name_multiple_records(self):
        self.repo.add(1, "alex", "Post 1")
        self.repo.add(2, "maria", "Post 2")
        self.repo.add(3, "alex", "Post 3")

        alex_posts = self.repo.get_by_name("alex")
        self.assertEqual(len(alex_posts), 2)
        self.assertEqual([p["id"] for p in alex_posts], [1, 3])
        self.assertEqual(alex_posts[0]["message"], "Post 1")
        self.assertEqual(alex_posts[1]["message"], "Post 3")

    def test_get_by_name_not_found(self):
        self.repo.add(1, "alex", "Post 1")
        result = self.repo.get_by_name("unknown_user")
        self.assertEqual(result, [])

    def test_get_by_name_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.repo.get_by_name(123)

    def test_update_success(self):
        self.repo.add(1, "alex", "Original message")
        updated = self.repo.update(1, "Edited message")
        self.assertTrue(updated)
        record = self.repo.get_by_id(1)
        self.assertEqual(record["message"], "Edited message")
        self.assertEqual(record["name"], "alex")

    def test_update_non_existent_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.repo.update(999, "New message")

    def test_update_invalid_types_raise_type_error(self):
        self.repo.add(1, "alex", "Original")
        with self.assertRaises(TypeError):
            self.repo.update("1", "Updated")
        with self.assertRaises(TypeError):
            self.repo.update(1, 12345)

    def test_update_invalid_message_length_raises_value_error(self):
        self.repo.add(1, "alex", "Original")
        with self.assertRaises(ValueError):
            self.repo.update(1, "")
        with self.assertRaises(ValueError):
            self.repo.update(1, "   ")
        with self.assertRaises(ValueError):
            self.repo.update(1, "m" * 8097)

    def test_delete_existing_returns_true(self):
        self.repo.add(1, "alex", "To be deleted")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_non_existent_returns_false(self):
        self.assertFalse(self.repo.delete(999))

    def test_delete_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.repo.delete("1")
        with self.assertRaises(TypeError):
            self.repo.delete(True)

    def test_context_manager_support(self):
        with DatabaseRepository(":memory:") as repo:
            repo.add(1, "ctx_user", "Context manager test")
            self.assertIsNotNone(repo.get_by_id(1))


if __name__ == "__main__":
    unittest.main()
