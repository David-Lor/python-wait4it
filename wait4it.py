"""wait4it
"""

import socket
from time import time, sleep
from contextlib import closing

__all__ = ("wait_for", "WaitForTimeoutError", "get_free_port")


class WaitForTimeoutError(TimeoutError):
    # TODO docstring for class
    def __init__(self, host, port):
        super().__init__(f"Timeout reached while waiting for {host}:{port} to be reachable")
        self.host = host
        self.port = port


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
    have_timeout = bool(timeout)

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sck:
        if have_timeout:
            sck.settimeout(timeout)
            start_time = time()

        while True:
            try:
                sck.connect((host, port))
                return True

            except (ConnectionError, socket.timeout):
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
