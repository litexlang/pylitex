import multiprocessing as mp
import subprocess

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


def run_batch(codes: list[str], max_workers: int = 1) -> list[dict]:
    """
    Run a batch of code snippets in parallel.

    :param codes: A list of code snippets to run.
    :param max_workers: The maximum number of worker processes to use if model is MULTIPROCESS.
    :return: A list of outputs from each code snippet.
    """
    with mp.Pool(processes=max_workers) as pool:
        results = pool.map(run, codes)
    return results
