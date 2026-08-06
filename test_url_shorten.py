import importlib
import os
import re
import sys
import tempfile
import unittest


class URLShortenerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_url_shortener.db")
        os.environ["URL_SHORTENER_DB_PATH"] = self.db_path
        sys.modules.pop("url_shorten", None)
        self.module = importlib.import_module("url_shorten")
        self.client = self.module.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()
        os.environ.pop("URL_SHORTENER_DB_PATH", None)
        sys.modules.pop("url_shorten", None)

    def test_shorten_and_redirect(self):
        response = self.client.post("/shorten", data={"long_url": "https://example.com"})
        self.assertEqual(response.status_code, 200)

        body = response.get_data(as_text=True)
        self.assertIn("shortened url", body)

        match = re.search(r"http://localhost/([A-Za-z0-9_\-]+)", body)
        self.assertIsNotNone(match)
        short_code = match.group(1)

        redirect_response = self.client.get(f"/{short_code}", follow_redirects=False)
        self.assertEqual(redirect_response.status_code, 302)
        self.assertEqual(redirect_response.headers["Location"], "https://example.com")


if __name__ == "__main__":
    unittest.main()
