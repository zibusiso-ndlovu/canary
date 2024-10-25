import unittest
import requests

class TestCanaryApp(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8082"  # Using the Ingress controller port

    def test_homepage_main(self):
        response = requests.get(self.base_url, headers={"Host": "canary-demo.local"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello from version v1", response.text)
        self.assertIn("background-color: white", response.text)

    def test_homepage_canary(self):
        # We'll make multiple requests to increase the chance of hitting the canary
        for _ in range(10):
            response = requests.get(self.base_url, headers={"Host": "canary-demo.local"})
            if "Hello from version v2" in response.text:
                self.assertIn("background-color: green", response.text)
                return  # Test passes if we hit the canary
        self.fail("Did not receive canary version after 10 attempts")

    def test_metrics(self):
        response = requests.get(f"{self.base_url}/metrics", headers={"Host": "canary-demo.local"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("http_requests_total", response.text)

if __name__ == '__main__':
    unittest.main()