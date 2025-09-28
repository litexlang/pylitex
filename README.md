# Pylitex

[![PyPI version](https://badge.fury.io/py/pylitex.svg)](https://badge.fury.io/py/pylitex)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A Python API library for Litex core, designed to help Python users interact with Litex core seamlessly. This library provides both local and online execution capabilities, persistent environments, and multi-process support.

## Installation

> 💡 _Install Litex core before using `pylitex`, visit our [website](https://litexlang.org) and read the [Installation](https://litexlang.org/doc/Start) of Litex core._

**After installing Litex core on your machine**, install `pylitex` in the same way as installing other Python packages:

```bash
# remember to install Litex core before install pylitex
# change your Python env to which your are using
# then run following commands
pip install pylitex
```

## Usage

Import `pylitex` to get started:

```python
import pylitex
```

### Basic Functions

#### Local Execution

Execute Litex code using your local Litex installation:

```python
# Run a single code snippet
result = pylitex.run("1 + 1 = 2")
print(result)
# Output: {"success": True, "payload": "1 + 1 = 2", "message": "..."}
```

#### Online Execution

Execute Litex code using the online Litex service (no local installation required):

```python
# Run code online
result = pylitex.run_online("1 + 1 = 2")
print(result)
# Output: {"success": True, "payload": "1 + 1 = 2", "message": "..."}
```

#### LaTeX Conversion

Convert Litex code to LaTeX format:

```python
# Convert code to LaTeX
result = pylitex.convert_to_latex("1 + 1 = 2")
print(result)
# Output: {"success": True, "payload": "1 + 1 = 2", "message": "LaTeX output..."}
```

### Persistent Execution with Runner

For multiple code executions that need to maintain state:

```python
# Create a persistent runner
runner = pylitex.Runner()

try:
    # Variables persist between calls
    result1 = runner.run("let a R: a = 1")
    result2 = runner.run("let b R: b = 2")
    result3 = runner.run("let c R: c = a + b")
    print("Final result:", result3)
finally:
    runner.close()  # Always close the runner
```

### Multi-Process Execution with RunnerPool

For parallel execution with separate environments per session:

```python
# Create a runner pool with 2 workers and 30-second timeout
pool = pylitex.RunnerPool(max_workers=2, timeout=30)

try:
    # Each ID maintains its own environment
    pool.inject_code({"id": "session1", "code": "let x R: x = 5"})
    pool.inject_code({"id": "session2", "code": "let y R: y = 10"})
    pool.inject_code({"id": "session1", "code": "let result R: result = x * 2"})
    pool.inject_code({"id": "session2", "code": "let result R: result = y / 2"})
    
    # Get all results grouped by session ID
    results = pool.get_results()
    print("Session 1 results:", results["session1"])
    print("Session 2 results:", results["session2"])
finally:
    pool.close()  # Always close the pool
```

### Utility Functions

#### Version Information

Get version information for both pylitex and Litex core:

```python
# Get pylitex version
version = pylitex.get_version()
print(f"Pylitex version: {version}")

# Get Litex core version (requires local installation)
litex_version = pylitex.get_litex_version()
print(f"Litex core version: {litex_version}")
```

## API Reference

### Functions

- **`run(code: str) -> dict`**: Execute Litex code locally
- **`run_online(code: str) -> dict`**: Execute Litex code online
- **`convert_to_latex(code: str) -> dict`**: Convert Litex code to LaTeX
- **`get_version() -> str`**: Get pylitex version
- **`get_litex_version() -> str`**: Get Litex core version

### Classes

- **`Runner()`**: Persistent Litex execution environment
  - `run(code: str) -> dict`: Execute code in persistent environment
  - `close()`: Close the runner
  
- **`RunnerPool(max_workers: int = 1, timeout: int = 10)`**: Multi-process runner pool
  - `inject_code(code_info: dict)`: Add code to execution queue
  - `get_results() -> dict`: Get all execution results
  - `close()`: Close all runners

### Return Format

All execution functions return a dictionary with the following structure:

```python
{
    "success": bool,      # True if execution succeeded
    "payload": str,       # The original code that was executed
    "message": str        # Output message or error details
}
```

### Error Handling

The library handles common errors gracefully:

- **Local execution**: Returns error message if Litex core is not installed or not in PATH
- **Online execution**: Returns error message for network issues or API failures
- **Runner errors**: Automatically resets environment on unexpected failures

## Requirements

- Python 3.9+
- For local execution: Litex core must be installed and accessible via `litex` command
- For online execution: Internet connection required

## License

MIT License - see LICENSE file for details.