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

To use it:

```python
import pylitex

# run full code
result = pylitex.run("code...")

# run full codes with multi-threads/multi-process
results = pylitex.run_batch(["code1...", "code2..."], 2)

# run continuous codes in same litex env
litex_runner = pylitex.Runner()
result1 = litex_runner.run("code1...")
result2 = litex_runner.run("code2...")
litex_runner.close()
```
