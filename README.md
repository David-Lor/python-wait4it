# python-wait4it

![Test](https://github.com/David-Lor/python-wait4it/workflows/Test/badge.svg)
[![PyPi](https://img.shields.io/badge/PyPi-wait4it-blue)](https://pypi.org/project/wait4it/)
[![License](https://img.shields.io/github/license/David-Lor/python-wait4it)](https://github.com/David-Lor/python-wait4it/blob/master/LICENSE.md)

Wait-For-It Python module, that waits until a certain TCP port is available.

Based on the idea behind the well-known [wait-for-it](https://github.com/vishnubob/wait-for-it) script, but created mainly as a Python package to be used on other Python applications, services or modules, instead of being mainly a CLI tool.

## Installing

Package is available at [PyPi](https://pypi.org/project/wait4it), so you can install it with `pip install wait4it` - or from sources with `python setup.py install`.

## Usage

```python
from wait4it import wait_for, WaitForTimeoutError

# This should return instantly (if you have connection)
wait_for(host="google.com", port=80)

# This should fail in 5 seconds
try:
    wait_for(host="google.com", port=12345, timeout=5)
except TimeoutError:
    # Actually will raise custom WaitForTimeoutError exception, but inherits from TimeoutError (except on Python2)
    print("Failed! (as expected)")

# This should return False in 15 seconds
wait_for(host="google.com", port=12345, raise_error=False)

# Normally you will want to check for a port in localhost (e.g. a MySQL/MariaDB database).
# This can be done directly like:
wait_for(3306)

# The exceptions include the failing host/port
try:
    wait_for(host="google.com", port=12345)
except WaitForTimeoutError as ex:
    assert ex.host == "google.com"
    assert ex.port == 12345
```

## Dependencies & Compatibility

Not external dependencies are required. Compatible (tested with) Python 2.7, 3.4, 3.5, 3.6, 3.7, 3.8 - under Linux.

## Changelog

- 0.0.1 - Initial release

## TODO

- Parameter to set retries limit
