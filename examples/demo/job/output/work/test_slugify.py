import unittest
from slugify import slugify


class T(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_runs_and_edges(self):
        self.assertEqual(slugify("  a -- b  "), "a-b")


if __name__ == "__main__":
    unittest.main()
