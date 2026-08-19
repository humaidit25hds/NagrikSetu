import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class HealthCheckTests(unittest.TestCase):
    def test_health_reports_database_disconnects(self):
        with patch("app.main.check_mongo_connection", return_value={"configured": False, "status": "not_configured"}), patch(
            "app.main.check_database_connection", return_value="disconnected"
        ):
            client = TestClient(app)
            response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "degraded")
        self.assertEqual(response.json()["database"], "disconnected")


if __name__ == "__main__":
    unittest.main()
