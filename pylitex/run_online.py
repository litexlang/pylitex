import multiprocessing as mp
import requests


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


def run_batch_online(codes: list[str], max_workers: int = 1) -> list[dict]:
    """
    Run a batch of code snippets in parallel online.

    :param codes: A list of code snippets to run.
    :param max_workers: The maximum number of worker processes to use if model is MULTIPROCESS.
    :return: A list of outputs from each code snippet.
    """
    with mp.Pool(processes=max_workers) as pool:
        results = pool.map(run_online, codes)
    return results
