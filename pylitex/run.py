import subprocess
import requests

from .base_info import litex_path


def run(code: str) -> dict:
    """
    Run a code snippet in the Litex environment.

    :param code: The code snippet to run.
    :return: The output of the code execution.
    """
    try:
        result = subprocess.run(
            [litex_path, "-e", code], capture_output=True, text=True, check=True
        )
        return {
            "success": True if ":)" in result.stdout else False,
            "payload": code,
            "message": result.stdout,
        }
    except subprocess.CalledProcessError as e:
        return {"success": False, "payload": code, "message": e.stderr}
    except FileNotFoundError:
        return {
            "success": False,
            "payload": code,
            "message": "Litex command not found. Please ensure Litex is installed and in your PATH.",
        }


def convert_to_latex(code: str) -> dict:
    """
    Convert a code snippet to LaTeX format.

    :param code: The code snippet to convert.
    :return: The LaTeX formatted output.
    """
    try:
        result = subprocess.run(
            [litex_path, "-latex", "-e", code],
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            "success": True,
            "payload": code,
            "message": result.stdout,
        }
    except subprocess.CalledProcessError as e:
        return {"success": False, "payload": code, "message": e.stderr}
    except FileNotFoundError:
        return {
            "success": False,
            "payload": code,
            "message": "Litex command not found. Please ensure Litex is installed and in your PATH.",
        }


def run_online(code: str) -> dict:
    """
    Run a code snippet in the online Litex environment.

    :param code: The code snippet to run.
    :return: The output of the code execution.
    """
    url = "https://litexlang.com/api/litex"
    try:
        response = requests.post(
            url, json={"targetFormat": "Run Litex", "litexString": code}
        )
        return {
            "success": True if ":)" in response.json()["data"] else False,
            "payload": code,
            "message": response.json()["data"],
        }
    except requests.RequestException as e:
        return {"success": False, "payload": code, "message": str(e)}
