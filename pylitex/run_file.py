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
            "success": is_success(result),
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
    except Exception as e:
        return {
            "success": False,
            "payload": code,
            "message": str(e),
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


def is_success(result):
    """
    Check if the result indicates a successful execution.
    
    :param result: A subprocess.CompletedProcess object with stdout attribute.
    :return: True if result.stdout (after stripping trailing whitespace) ends with ':)'.
    """
    # result.stdout在排除了末尾的空字符后，是以:)结尾的
    if not result.stdout:
        return False
    return result.stdout.rstrip().endswith(":)")
    