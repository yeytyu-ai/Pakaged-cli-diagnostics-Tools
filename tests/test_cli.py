import json
import unittest
from unittest.mock import patch

from diagnostics_cli.cli import collect_diagnostics


class TestDiagnostics(unittest.TestCase):

    def test_python_information_exists(self):
        report = collect_diagnostics()
        self.assertIn("python", report)
        self.assertIn("version", report["python"])

    def test_disk_information_exists(self):
        report = collect_diagnostics()
        self.assertIn("disk", report)
        self.assertGreaterEqual(report["disk"]["total_gb"], 0)

    def test_developer_tools_exist(self):
        report = collect_diagnostics()
        self.assertIn("developer_tools", report)
        self.assertIn("python", report["developer_tools"])

    def test_report_is_json_serializable(self):
        report = collect_diagnostics()
        encoded = json.dumps(report)
        decoded = json.loads(encoded)
        self.assertEqual(decoded["status"], report["status"])

    @patch("diagnostics_cli.cli.shutil.disk_usage")
    def test_low_disk_space_warning(self, mock_usage):
        mock_usage.return_value = type(
            "Usage",
            (),
            {
                "total": 10 * 1024**3,
                "used": 9.5 * 1024**3,
                "free": 0.5 * 1024**3,
            },
        )()

        report = collect_diagnostics(min_free_gb=1.0)
        self.assertEqual(report["status"], "WARN")


if __name__ == "__main__":
    unittest.main()
