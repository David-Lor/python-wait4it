"""wait4it
"""

import socket
from time import time, sleep
from contextlib import closing, contextmanager

__all__ = ("wait_for", "wait_for_pass", "WaitForTimeoutError", "get_free_port")

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


def wait_for_pass(exceptions=None, retries=3):
    """Decorator that catches exceptions raised by the decorated function, and retries running it
    if the exception is one of the provided, until retries limit is reached.
    :param exceptions: single or list of exceptions expected. If not set, catch all
    :type exceptions: list | tuple | Exception
    :param retries: retries limit. If 0, retry forever
    :type retries: int
    """
    # TODO Add timeout
    try:
        len(exceptions)
    except TypeError:
        if exceptions:
            exceptions = [exceptions]

    def _real_decorator(func):
        def wrapper(*args, **kwargs):
            last_ex = None

            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    if exceptions and type(ex) not in exceptions:
                        raise ex
                    last_ex = ex

            raise last_ex

        return wrapper

    return _real_decorator


def wait_for(port, host="127.0.0.1", polling_freq=0.25, timeout=15, raise_error=True):
    """Wait for a given TCP port to be reachable.
    :param host: target host to wait its port for (default=127.0.0.1)
    :type host: str
    :param port: target port to wait for
    :type port: int
    :param polling_freq: how much time to wait between checks on target port
    :type polling_freq: float
    :param timeout: if the port is not available after this time is elapsed, a TimeoutError is raised or False returned.
                    If 0, wait infinitely until the port is available (
    :type timeout: float
    :param raise_error: if True, raise TimeoutError if port is not available on "timeout" time.
                        If False, just return True/False (default=True)
    :returns: True/False
    :rtype: bool
    :raises: WaitForTimeoutError | ValueError
    """
    # TODO Add retries_limit param
    have_timeout = timeout and timeout > 0
    try:
        socket_exceptions = (ConnectionError, socket.timeout, socket.error)
    except NameError:
        socket_exceptions = (OSError, socket.error)

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sck:
        if have_timeout:
            sck.settimeout(timeout)
            start_time = time()

        while True:
            try:
                sck.connect((host, port))
                return True

            except socket_exceptions:
                if have_timeout and time() - start_time >= timeout:
                    if raise_error:
                        raise WaitForTimeoutError(host=host, port=port)
                    else:
                        return False
                else:
                    sleep(polling_freq)


def get_free_port():
    """Get a random free port on localhost. Notice that the port is not reserved, and could be used by any other
    application until your target service binds to it.
    :returns: free port available
    :rtype: int
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sck:
        sck.bind(("", 0))
        sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sck.getsockname()[1]
