import threading
import multiprocessing as mp
import subprocess
import re

from pexpect import replwrap, EOF

from .enum import RunBatchModel

__version__ = "0.1.6"
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


def _run_batch_multithread(codes: list[str]) -> list[str]:
    """Run a batch of code snippets in parallel using threads."""
    threads = []
    for code in codes:
        thread = threading.Thread(target=run, args=(code,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return [thread.result for thread in threads]


def _run_batch_multiprocess(codes: list[str], max_workers: int = 1) -> list[str]:
    """Run a batch of code snippets in parallel using processes."""
    with mp.Pool(processes=max_workers) as pool:
        results = pool.map(run, codes)
    return results


# TODO Implement a function to determine the best model to use for running batches
def _auto_model_determination() -> RunBatchModel:
    """Determine the best model to use for running batches."""
    return RunBatchModel.MULTIPROCESS  # Placeholder for actual logic


def run_batch(
    codes: list[str], max_workers: int = 1, model: RunBatchModel = RunBatchModel.AUTO
) -> list[str]:
    """Run a batch of code snippets in parallel."""
    if model == RunBatchModel.MULTIPROCESS:
        return _run_batch_multiprocess(codes, max_workers)
    elif model == RunBatchModel.MULTITHREAD:
        return _run_batch_multithread(codes)
    elif model == RunBatchModel.AUTO:
        target_model = _auto_model_determination()
        if target_model == RunBatchModel.MULTIPROCESS:
            return _run_batch_multiprocess(codes, max_workers)
        elif target_model == RunBatchModel.MULTITHREAD:
            return _run_batch_multithread(codes)
        else:
            raise ValueError(f"Unsupported auto-determined model: {target_model}")
    else:
        raise ValueError(f"Unsupported RunBatchModel: {model}")


class Runner:
    """A class to run code snippets in the Litex environment."""

    def __init__(self):
        self.litex_path = litex_path
        self._start_litex()

    def _start_litex(self):
        """Start the Litex REPL."""
        prompt = ">>> "
        continuation_prompt = "... "
        self.litexwrapper = replwrap.REPLWrapper(
            self.litex_path, prompt, None, continuation_prompt=continuation_prompt
        )
        self.litexwrapper.child.delaybeforesend = 0.1

    def _code_formatter(self, code: str) -> str:
        """Format the code to ensure proper indentation and line breaks."""
        litex_indentation = " " * 4
        code_lines = code.splitlines()
        formatted_lines = []

        for index, line in enumerate(code_lines):
            is_last_line = index >= len(code_lines) - 1
            if line.strip() == "":
                continue
            elif line.startswith(litex_indentation) and (
                is_last_line
                or not code_lines[index + 1].rstrip().startswith(litex_indentation)
            ):
                formatted_lines.append(line.rstrip())
                formatted_lines.append("")
            else:
                formatted_lines.append(line.rstrip())
        return "\n".join(formatted_lines)

    def run(self, code: str) -> str:
        """Run a code snippet in the Litex environment."""
        formatted_code = self._code_formatter(code)
        try:
            output = self.litexwrapper.run_command(formatted_code, timeout=None)
            return output
        except EOF:
            self._start_litex()
            return "Litex REPL closed unexpectedly. REPL restarted. Environment reset."
        except Exception as e:
            return f"Error running code: {str(e)}"

    def close(self):
        """Close the Litex REPL."""
        try:
            self.litexwrapper.child.close()
        except EOF:
            pass
        except Exception as e:
            print(f"Error closing Litex REPL: {str(e)}")