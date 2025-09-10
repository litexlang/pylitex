# Pylitex

This is a Python api library for Litex core, which aims to help Python users to interact with Litex core.

## Installation

> 💡 *Install Litex core before using `pylitex`, follow the [Installation](https://litexlang.org/doc/Installation) to install Litex core.*

After Litex core installation, you could install `pylitex` for your python environment:

```bash
# change your Python env to which your are using
# then run following commands
pip install pylitex
```

`pylitex` is under rapid development, so the version is not stable. Update `pylitex` using the following command:

```bash
pip install -U pylitex
```

## Usage

Import `pylitex` as you installed.

```python
import pylitex
```

### Run full code

```python
# run full code
result = pylitex.run("code...")

# run full codes with multi-process
results = pylitex.run_batch(["code1...", "code2..."], 2)
```

Example:

```python
import pylitex

a = 1
b = 1
pylitex.run(str(a) + " = " + str(b))
```

### Run continuous codes

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

Example:

```python
import pylitex

runner = pylitex.Runner()
runner.run("let a R: a = 1")
runner.run("let b R: b = 2")
runner.run("b = 2 * a")
runner.close()
```

The difference between `pylitex.run()` and `pylitex.Runner().run()` is that `pylitex.run()` will start a new Litex environment for each code, while `runner = pylitex.Runner()` and use `runner.run()` will use the same Litex environment for all codes. You can execute `runner.run("clear")` to clear the Litex environment of the runner.

### Return type

For `pylitex.run()` and `pylitex.Runner().run()`, the return type is a python `dict` like (Call it `pylitexResult`):

```json
{"truely": boolean, "msg": str}
```

For `pylitex.run_batch()`, the return type is a python `list[pylitexResult]` like:

```json
[
    {"truely": boolean, "msg": str},
    {"truely": boolean, "msg": str},
    ...
]
```

For `pylitex.RunnerPool().get_results()`, the return type is a python `dict[list[pylitexResult]]` like:

```json
{
    "id1": [
        {"truely": boolean, "msg": str},
        {"truely": boolean, "msg": str},
        {"truely": boolean, "msg": str},
        ...
    ],
    "id2": [
        {"truely": boolean, "msg": str},
        {"truely": boolean, "msg": str},
        ...
    ],
    ...
}
```
