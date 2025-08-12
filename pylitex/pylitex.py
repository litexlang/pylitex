import threading
import multiprocessing as mp
import subprocess
import re

from .enum import RunBatchModel

__version__ = "0.1.3"
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


def run_batch_multithread(codes: list[str]) -> list[str]:
    """Run a batch of code snippets in parallel using threads."""
    threads = []
    for code in codes:
        thread = threading.Thread(target=run, args=(code,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return [thread.result for thread in threads]


def run_batch_multiprocess(codes: list[str], max_workers: int = 1) -> list[str]:
    """Run a batch of code snippets in parallel using processes."""
    with mp.Pool(processes=max_workers) as pool:
        results = pool.map(run, codes)
    return results


# TODO Implement a function to determine the best model to use for running batches
def auto_model_determination() -> RunBatchModel:
    """Determine the best model to use for running batches."""
    return RunBatchModel.MULTIPROCESS  # Placeholder for actual logic


def run_batch(
    codes: list[str], max_workers: int = 1, model: RunBatchModel = RunBatchModel.AUTO
) -> list[str]:
    """Run a batch of code snippets in parallel."""
    if model == RunBatchModel.MULTIPROCESS:
        return run_batch_multiprocess(codes, max_workers)
    elif model == RunBatchModel.MULTITHREAD:
        return run_batch_multithread(codes)
    elif model == RunBatchModel.AUTO:
        target_model = auto_model_determination()
        if target_model == RunBatchModel.MULTIPROCESS:
            return run_batch_multiprocess(codes, max_workers)
        elif target_model == RunBatchModel.MULTITHREAD:
            return run_batch_multithread(codes)
        else:
            raise ValueError(f"Unsupported auto-determined model: {target_model}")
    else:
        raise ValueError(f"Unsupported RunBatchModel: {model}")
