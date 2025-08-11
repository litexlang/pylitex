import multiprocessing as mp
import subprocess
import re

__version__ = "0.1.0"
version_pat = re.compile(r"Litex Kernel: golitex (.*)")
litex_path = "litex"


def get_version():
    """Get the version of this package."""
    return __version__


def get_litex_version():
    """Get the version of the Litex core."""
    try:
        result = subprocess.run(
            [litex_path, "--version"], capture_output=True, text=True, check=True
        )
        match = version_pat.search(result.stdout)
        if match:
            return match.group(1)
    except subprocess.CalledProcessError as e:
        return f"Error getting version: {e.stderr}"
    except FileNotFoundError:
        return "Litex command not found. Please ensure Litex is installed and in your PATH."


def run(code: str) -> str:
    """Run a code snippet in the Litex environment."""
    try:
        result = subprocess.run(
            [litex_path, "-e", code], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except FileNotFoundError:
        return "Litex command not found. Please ensure Litex is installed and in your PATH."


def run_batch(codes: list[str], max_workers: int = 1) -> list[str]:
    """Run a batch of code snippets in parallel."""
    with mp.Pool(processes=max_workers) as pool:
        results = pool.map(run, codes)
    return results
