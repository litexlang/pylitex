import unittest
from unittest.mock import patch, MagicMock
import subprocess

from pylitex.run_file import run


class TestRunFunction(unittest.TestCase):
    """Test cases for the run function."""

    @patch("pylitex.run_file.subprocess.run")
    def test_run_success(self, mock_subprocess_run):
        """Test successful code execution without errors."""
        # Mock successful subprocess execution
        mock_result = MagicMock()
        mock_result.stdout = "Output: 42"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        code = "1 + 1"
        result = run(code)

        # Verify subprocess was called correctly
        mock_subprocess_run.assert_called_once_with(
            ["litex", "-e", code], capture_output=True, text=True, check=True
        )

        # Verify return value
        self.assertTrue(result["success"])
        self.assertEqual(result["payload"], code)
        self.assertEqual(result["message"], "Output: 42")

    @patch("pylitex.run_file.subprocess.run")
    def test_run_with_error_in_output(self, mock_subprocess_run):
        """Test code execution that returns output containing 'Error'."""
        # Mock subprocess execution with "Error" in output
        mock_result = MagicMock()
        mock_result.stdout = "Error: something went wrong"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        code = "invalid code"
        result = run(code)

        # Verify return value - success should be False when "Error" is in output
        self.assertFalse(result["success"])
        self.assertEqual(result["payload"], code)
        self.assertEqual(result["message"], "Error: something went wrong")

    @patch("pylitex.run_file.subprocess.run")
    def test_run_called_process_error(self, mock_subprocess_run):
        """Test handling of CalledProcessError exception."""
        # Mock subprocess raising CalledProcessError
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["litex", "-e", "code"], stderr="Process error occurred"
        )

        code = "failing code"
        result = run(code)

        # Verify return value
        self.assertFalse(result["success"])
        self.assertEqual(result["payload"], code)
        self.assertEqual(result["message"], "Process error occurred")

    @patch("pylitex.run_file.subprocess.run")
    def test_run_file_not_found_error(self, mock_subprocess_run):
        """Test handling of FileNotFoundError exception."""
        # Mock subprocess raising FileNotFoundError
        mock_subprocess_run.side_effect = FileNotFoundError()

        code = "some code"
        result = run(code)

        # Verify return value
        self.assertFalse(result["success"])
        self.assertEqual(result["payload"], code)
        self.assertEqual(
            result["message"],
            "Litex command not found. Please ensure Litex is installed and in your PATH.",
        )

    @patch("pylitex.run_file.subprocess.run")
    def test_run_empty_code(self, mock_subprocess_run):
        """Test running empty code string."""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        code = ""
        result = run(code)

        self.assertTrue(result["success"])
        self.assertEqual(result["payload"], code)
        self.assertEqual(result["message"], "")

    @patch("pylitex.run_file.subprocess.run")
    def test_run_multiline_code(self, mock_subprocess_run):
        """Test running multiline code."""
        mock_result = MagicMock()
        mock_result.stdout = "Result: 10"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        code = "x = 5\ny = 5\nx + y"
        result = run(code)

        self.assertTrue(result["success"])
        self.assertEqual(result["payload"], code)
        self.assertEqual(result["message"], "Result: 10")


if __name__ == "__main__":
    unittest.main()


