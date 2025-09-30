import re
import subprocess

__VERSION__ = "0.2.1"
LITEX_PATH = "litex"
VERSION_PAT = re.compile(r"Litex Kernel: golitex (.*)")


def get_version():
    """
    Get the version of this package.
    """
    return __VERSION__


def get_litex_version():
    """
    Get the version of the Litex core.
    """
    try:
        result = subprocess.run(
            [LITEX_PATH, "--version"], capture_output=True, text=True, check=True
        )
        match = VERSION_PAT.search(result.stdout)
        if match:
            return match.group(1)
    except subprocess.CalledProcessError as e:
        return f"Error getting version: {e.stderr}"
    except FileNotFoundError:
        return "Litex command not found. Please ensure Litex is installed and in your PATH."
