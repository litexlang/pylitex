# Pylitex

[![PyPI version](https://badge.fury.io/py/pylitex.svg)](https://badge.fury.io/py/pylitex)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A Python API library for Litex core, designed to help Python users interact with Litex core seamlessly. This library provides both local and online execution capabilities, persistent environments, and multi-process support.

**Features:**
- 🚀 Local and online Litex code execution
- 🔄 Persistent REPL environments for stateful operations  
- ⚡ Multi-process execution pools for parallel processing
- 📝 LaTeX conversion for mathematical expressions
- 🛡️ Robust error handling and timeout management

## Installation

> 💡 _Install Litex core before using `pylitex`, visit our [website](https://litexlang.org) and read the [Installation](https://litexlang.org/doc/Start) of Litex core._

**After installing Litex core on your machine**, install `pylitex` in the same way as installing other Python packages:

```bash
# remember to install Litex core before install pylitex
# change your Python env to which your are using
# then run following commands
pip install pylitex
```

`pylitex` is under active development. Update to the latest version:

```bash
pip install -U pylitex
```

## Usage

Import `pylitex` to get started:

```python
import pylitex
```

### Quick Start

Here's a simple example to get you started quickly:

```python
import pylitex

# Check if everything is working
print("Pylitex version:", pylitex.get_version())

# Try online execution (no local Litex installation required)
result = pylitex.run_online("1 + 1 = 2")
print("Online result:", result)

# If you have Litex installed locally, try:
try:
    local_result = pylitex.run("1 + 1 = 2") 
    print("Local result:", local_result)
except:
    print("Local Litex not available - install Litex core for local execution")
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

Convert Litex code to LaTeX format using the `-elatex` flag:

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

### Core Functions

#### `run(code: str) -> dict`
Execute Litex code locally using subprocess with the `-e` flag.
- **Parameters**: `code` - The Litex code string to execute
- **Returns**: Dictionary with `success`, `payload`, and `message` keys
- **Requires**: Local Litex installation

#### `run_online(code: str) -> dict`
Execute Litex code using the online Litex service at `https://litexlang.com/api/litex`.
- **Parameters**: `code` - The Litex code string to execute
- **Returns**: Dictionary with `success`, `payload`, and `message` keys
- **Requires**: Internet connection

#### `convert_to_latex(code: str) -> dict`
Convert Litex code to LaTeX format using the `-elatex` flag.
- **Parameters**: `code` - The Litex code string to convert
- **Returns**: Dictionary with `success`, `payload`, and `message` keys
- **Requires**: Local Litex installation

### Utility Functions

#### `get_version() -> str`
Get the current version of pylitex package.
- **Returns**: Version string (currently "0.2.1")

#### `get_litex_version() -> str`
Get the version of the installed Litex core.
- **Returns**: Litex version string or error message
- **Requires**: Local Litex installation with `--version` support

### Classes

#### `Runner()`
Persistent Litex execution environment using REPL wrapper.
- **Methods**:
  - `run(code: str) -> dict`: Execute code in persistent environment with automatic formatting
  - `close()`: Close the REPL wrapper and cleanup resources
- **Features**: Maintains state between executions, automatic environment reset on errors

#### `RunnerPool(max_workers: int = 1, timeout: int = 10)`
Multi-process runner pool for parallel execution (experimental).
- **Parameters**:
  - `max_workers`: Number of worker processes
  - `timeout`: Timeout in seconds for runner operations
- **Methods**:
  - `inject_code(code_info: dict)`: Add code to execution queue
    - `code_info` should contain `{"id": "session_id", "code": "litex_code"}`
  - `get_results() -> dict`: Get all execution results grouped by session ID
  - `close()`: Close all worker processes
- **Note**: This feature is experimental and may have limitations

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
- Dependencies: `pexpect >= 4.8.0`, `requests >= 2.22.0`
- For local execution: Litex core must be installed and accessible via `litex` command
- For online execution: Internet connection required

## Version

Current version: **0.2.1**

### Version History

- **0.2.1**: Enhanced stability, improved error handling, updated documentation
- **0.2.0**: Core functionality with local/online execution, REPL wrappers, and LaTeX conversion

Check version programmatically:
```python
import pylitex
print(f"Pylitex version: {pylitex.get_version()}")
print(f"Litex core version: {pylitex.get_litex_version()}")
```

## Important Notes

### RunnerPool Limitations
The current `RunnerPool` implementation has some limitations:
- The multiprocess execution is still under development
- Some methods may not work as expected in the current version
- For production use, consider using the `Runner` class for persistent execution

### LaTeX Conversion
The `convert_to_latex` function uses the `-elatex` flag internally to generate LaTeX output from Litex code.

## License

MIT License - see LICENSE file for details.