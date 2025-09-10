import multiprocessing as mp
import time

from pexpect import replwrap, EOF

from .base_info import litex_path


class Runner:
    """
    A class to run code snippets in the Litex environment.
    """

    def __init__(self):
        self.litex_path = litex_path
        self._start_litex()

    def _start_litex(self):
        """
        Start the Litex REPL.
        """
        prompt = ">>> "
        continuation_prompt = "... "
        self.litexwrapper = replwrap.REPLWrapper(
            self.litex_path, prompt, None, continuation_prompt=continuation_prompt
        )

    def _code_formatter(self, code: str) -> str:
        """
        Format the code to ensure proper indentation and line breaks.

        :param code: The code snippet to format.
        :return: The formatted code snippet.
        """
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

    def run(self, code: str) -> dict:
        """
        Run a code snippet in the Litex environment.

        :param code: The code snippet to run.
        :return: The output of the code execution.
        """
        formatted_code = self._code_formatter(code)
        try:
            output = self.litexwrapper.run_command(formatted_code, timeout=None)
            return {
                "success": True if ":)" in output else False,
                "payload": code,
                "message": output,
            }
        except EOF:
            self._start_litex()
            return {
                "success": False,
                "payload": code,
                "message": "\n-- Litex Environment closed unexpectedly --\n-- Environment reset --\n",
            }
        except Exception as e:
            return {"success": False, "payload": code, "message": str(e)}

    def close(self):
        """
        Close the Litex REPL.
        """
        try:
            self.litexwrapper.child.close()
        except EOF:
            pass
        except Exception as e:
            print(f"Error closing Litex REPL: {str(e)}")


class RunnerPool:
    """
    A class to manage a pool of Litex runners.

    :param max_workers: The number of runners in the pool.
    :param timeout: The timeout for each runner operation in second.
    """

    def __init__(self, max_workers: int = 1, timeout: int = 10):
        self.pending_codes: dict = {}
        self.results: dict = {}
        self.runners = [
            mp.Process(target=self._run, args=(timeout,)) for _ in range(max_workers)
        ]

    def _run(self, timeout: int = 10) -> None:
        """
        Run a code snippet across all runners.

        :param timeout: The timeout for runner operation in second.
        """
        litex_runner = Runner()
        last_response = time.time()
        running_id = ""
        while True:
            if time.time() - last_response >= timeout:
                litex_runner.run("clear")
                running_id = ""
            else:
                if not running_id:
                    running_id = next(
                        (
                            pending_code
                            for pending_code in self.pending_codes
                            if not pending_code["running"]
                        ),
                        "",
                    )
                    last_response = time.time()
                else:
                    running_code = self.pending_codes[running_id]["codes"].pop(0)
                    self.results[running_id].append(litex_runner.run(running_code))
                    last_response = time.time()

    def inject_code(self, code_info: dict) -> None:
        """
        Inject code into the pool of runners.

        :param code_info: A dictionary containing the code and optional metadata.
        """
        id = code_info.get("id", None)
        if id is not None and not isinstance(id, str):
            raise TypeError("id must be a string")
        code = code_info.get("code", None)
        if not code and not isinstance(id, str):
            raise ValueError("code must be a string")
        self.pending_codes[id]["running"] = self.pending_codes[id]["running"] | False
        self.pending_codes[id]["codes"].append(code)

    def get_results(self) -> dict:
        """
        Get the results of the executed code snippets.

        :return: A list of results from the executed code snippets.
        """
        return self.results

    def close(self) -> None:
        """
        Close all runners.
        """
        try:
            for runner in self.runners:
                runner.close()
        except Exception as e:
            print(f"Error closing RunnerPool: {str(e)}")
