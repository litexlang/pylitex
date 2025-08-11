# Python api for Litex core

This is a Python api library for Litex core, which aims to help Python users to interact with Litex core.

## installation

This reuqires Litex core and Python3, you could install Litex core follow the [Installation](https://litexlang.org/doc/Installation). 

After Litex core installation, you could install litex for your python environment:

```bash
# change your Python env to which your are using
# then run following commands
pip install litex
```

To use it:

```python
import litex

# regular runner
result = litex.run("code...")

# multi-process runner
results = litex.run_batch(["code1...", "code2..."], 2)
```