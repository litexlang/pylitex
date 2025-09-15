# Pylitex

This is a Python api library for Litex core, which aims to help Python users to interact with Litex core.

## Installation

> 💡 _Install Litex core before using `pylitex`, visit our [website](https://litexlang.org) and read the [Installation](https://litexlang.org/doc/Start) of Litex core._

**After installing Litex core on your machine**, install `pylitex` in the same way as installing other Python packages:

```bash
# remember to install Litex core before install pylitex
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

`1 + 1 = 2` and `2 + 2 = 4` are examples of Litex code. You can write your own Litex code.

```python
# run full code
result = pylitex.run("1 + 1 = 2")

# run full codes with multi-process
results = pylitex.run_batch(["1 + 1 = 2", "2 + 2 = 4"], 2)
```

Example:

```python
import pylitex

a = 1
b = 1
pylitex.run(str(a) + " = " + str(b))
```

### Run full code via internet

`1 + 1 = 2` and `2 + 2 = 4` are examples of Litex code. You can write your own Litex code.

```python
# run full code
result = pylitex.run_online("1 + 1 = 2")

# run full codes with multi-process
results = pylitex.run_batch_online(["1 + 1 = 2", "2 + 2 = 4"], 2)
```

Example:

```python
import pylitex

a = 1
b = 1
pylitex.run_online(str(a) + " = " + str(b))
```

### Run continuous codes

```python
# run continuous codes in one litex env
litex_runner = pylitex.Runner()
result1 = litex_runner.run("1 + 1 = 2")
result2 = litex_runner.run("2 + 2 = 4")
litex_runner.close()

# run continuous code in litex multi-process pool
litex_pool = pylitex.RunnerPool()
litex_pool.inject_code({id: "id1", code: "1 + 1 = 2"})
litex_pool.inject_code({id: "id2", code: "2 + 2 = 4"})
litex_pool.inject_code({id: "id1", code: "1 + 1 = 2"})
litex_pool.inject_code({id: "id1", code: "2 + 2 = 4"})
litex_pool.inject_code({id: "id2", code: "2 + 2 = 4"})
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

### Compare

| function                             | environment                                  | required local litex installation | multithread |
| :----------------------------------- | :------------------------------------------- | :-------------------------------- | :---------- |
| `pylitex.run()`                      | New environment for each code                | ✅                                | ❌          |
| `pylitex.run_batch()`                | New environment for each code                | ✅                                | ✅          |
| `pylitex.run_online()`               | New environment for each code                | ❌                                | ❌          |
| `pylitex.run_batch_online()`         | New environment for each code                | ❌                                | ✅          |
| `pylitex.Runner().run()`             | Continuous environment for all code          | ✅                                | ❌          |
| `pylitex.RunnerPool().inject_code()` | Distribute environment for each code by `id` | ✅                                | ✅          |

### Return type

For `pylitex.run()`, `pulitex.run_online()` and `pylitex.Runner().run()`, the return type is a python `dict` like (Call it `pylitexResult`):

```json
{"success": boolean, "payload": str, "message": str}
```

For `pylitex.run_batch()` and `pylitex.run_batch_online()` the return type is a python `list[pylitexResult]` like:

```json
[
    {"success": boolean, "payload": str, "message": str},
    {"success": boolean, "payload": str, "message": str},
    ...
]
```

For `pylitex.RunnerPool().get_results()`, the return type is a python `dict[list[pylitexResult]]` like:

```json
{
    "id1": [
        {"success": boolean, "payload": str, "message": str},
        {"success": boolean, "payload": str, "message": str},
        {"success": boolean, "payload": str, "message": str},
        ...
    ],
    "id2": [
        {"success": boolean, "payload": str, "message": str},
        {"success": boolean, "payload": str, "message": str},
        ...
    ],
    ...
}
```
