# Pylitex

This is a Python api library for Litex core, which aims to help Python users to interact with Litex core.

## installation

This reuqires Litex core and Python3, you could install Litex core follow the [Installation](https://litexlang.org/doc/Installation).

After Litex core installation, you could install litex for your python environment:

```bash
# change your Python env to which your are using
# then run following commands
pip install pylitex
```

## usage

Import `pylitex` as you installed.

```python
import pylitex
```

### run fill code

```python
# run full code
result = pylitex.run("code...")

# run full codes with multi-process
results = pylitex.run_batch(["code1...", "code2..."], 2)
```

### run continuous codes

```python
# run continuous codes in one litex env
litex_runner = pylitex.Runner()
result1 = litex_runner.run("code1...")
result2 = litex_runner.run("code2...")
litex_runner.close()

# run continuous code in litex multi-process pool
litex_pool = pylitex.RunnerPool()
litex_pool.inject_code({id: "id1", code: "code1..."})
litex_pool.inject_code({id: "id2", code: "code2..."})
litex_pool.inject_code({id: "id1", code: "code3..."})
litex_pool.inject_code({id: "id1", code: "code4..."})
litex_pool.inject_code({id: "id2", code: "code5..."})
results = litex_pool.get_results()
litex_pool.close()
```
