"""EXCEPTIONS
Custom exceptions
"""

__all__ = ("WaitForTimeoutError",)

try:
    _TimeoutError = TimeoutError
except NameError:
    _TimeoutError = OSError


class WaitForTimeoutError(_TimeoutError):
    # TODO docstring for class
    def __init__(self, host, port):
        super(_TimeoutError, self).__init__("Timeout reached while waiting for {host}:{port} to be reachable".format(
            host=host,
            port=port
        ))
        self.host = host
        self.port = port
