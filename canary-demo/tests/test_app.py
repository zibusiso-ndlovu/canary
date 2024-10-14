import unittest
import requests

class TestCanaryApp(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://canary-demo.local"

    def test_homepage(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello from version", response.text)

    def test_metrics(self):
        response = requests.get(f"{self.base_url}/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn("http_requests_total", response.text)

if __name__ == '__main__':
    unittest.main()
