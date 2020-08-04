"""TEST - HELPERS
Util functions and fixtures
"""

# # Native # #
import socket
from random import uniform
from time import time
from contextlib import closing, contextmanager

# # Installed # #
import pytest

# # Project # #
from wait4it import get_free_port

__all__ = ("free_port", "port_in_use", "lazy_port_in_use", "random_timeout", "expect_time")


@pytest.fixture
def free_port():
    """Returns a free port on this host
    """
    return get_free_port()


@pytest.fixture
def port_in_use(free_port):
    """Returns a free port on this host that is now in use by a fake service started by this fixture
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sck:
        sck.bind(("localhost", free_port))
        sck.listen(1)
        yield free_port


@pytest.fixture
def lazy_port_in_use(free_port):
    """Returns a free port on this host that is now in use by a fake service started by this fixture
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sck:
        sck.bind(("localhost", free_port))
        yield free_port


@pytest.fixture
def random_timeout():
    """Returns a random timeout value (a float between 0.1 and 2)
    """
    return uniform(0.1, 2)


@contextmanager
def expect_time(expected, more=False):
    """Context manager that expects to run the inner code in less or more than the given time
    :param expected: expected limit/minimum time to run code in
    :type expected: float
    :param more: if True, verify that runs in more time than the expected.
                 If False, verify that it runs in less time than the expected
    :type more: bool
    """
    start_time = time()
    yield
    elapsed_time = time() - start_time
    assert elapsed_time < expected if not more else elapsed_time >= expected
