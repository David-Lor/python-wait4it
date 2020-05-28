"""TEST - WAIT FOR
Test the wait_for function
"""

# # Installed # #
import pytest

# # Project # #
from wait4it import wait_for, WaitForTimeoutError

# # Package # #
from .helpers import expect_time


def test_wait_for_port_in_use(port_in_use):
    """Wait for a port that is currently in use.
    Should run ASAP and return True
    """
    r = wait_for(port_in_use)
    assert r is True


def test_wait_for_port_not_in_use(free_port, random_timeout):
    """Wait for a port that is currently free.
    Should raise WaitForTimeoutError with host:port attributes, after the given timeout
    """
    with expect_time(random_timeout + 0.5):
        with pytest.raises(WaitForTimeoutError):
            try:
                wait_for(free_port, timeout=random_timeout)
            except WaitForTimeoutError as error:
                assert error.host == "127.0.0.1"
                assert error.port == free_port
                raise error


def test_wait_for_port_not_in_use_not_raise(free_port, random_timeout):
    """Wait for a port that is currently free, without raising exception.
    Should return False after the given timeout
    """
    with expect_time(random_timeout + 0.5):
        r = wait_for(free_port, timeout=random_timeout, raise_error=False)
        assert r is False


# TODO Pending tests:
#  - parametrize polling_freq
#  - set timeout to 0
