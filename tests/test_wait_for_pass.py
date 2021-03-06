"""TEST - WAIT FOR PASS
Test the wait_for_pass decorator
"""

# # Installed # #
import pytest

# # Project # #
from wait4it import wait_for_pass

# # Package # #
from .helpers import expect_time


def test_wait_for_pass_successful(random_timeout):
    """Wait for a function that raises no exceptions.
    Should return the function return value with no problem
    """
    @wait_for_pass(Exception)
    def func():
        return random_timeout

    result = func()
    assert result == random_timeout


def test_wait_for_pass_fail_once(random_timeout):
    """Wait for a function that raises an exception only once, with 2 retries limit.
    Should run twice and return the function return value with no problem
    """
    run_data = {
        "times_ran": 0,
        "ran": False
    }

    @wait_for_pass(ZeroDivisionError, retries=2)
    def func():
        run_data["times_ran"] += 1
        if run_data["ran"] is False:
            run_data["ran"] = True
            raise ZeroDivisionError
        return random_timeout

    result = func()
    assert result == random_timeout
    assert run_data["ran"] is True
    assert run_data["times_ran"] == 2


def test_wait_for_pass_always_fail():
    """Wait for a function that always raises an exception, with 3 retries limit.
    The function raises a different exception each time.
    Should run thrice and raise the last defined exception (from array of 3)
    """
    run_data = {
        "times_ran": 0
    }
    exceptions = [ZeroDivisionError, OSError, TypeError]

    @wait_for_pass(exceptions, retries=3)
    def func():
        exception_to_raise = exceptions[run_data["times_ran"]]
        run_data["times_ran"] += 1
        raise exception_to_raise

    with pytest.raises(exceptions[-1]):
        func()

    assert run_data["times_ran"] == 3


def test_wait_for_pass_not_defined_exception():
    """Wait for a function that raises an exception that is not set as filter on wait_for_pass decorator.
    Should run once and raise the exception
    """
    run_data = {
        "times_ran": 0
    }

    @wait_for_pass(ZeroDivisionError)
    def func():
        run_data["times_ran"] += 1
        raise TypeError

    with pytest.raises(TypeError):
        func()

    assert run_data["times_ran"] == 1


def test_wait_for_pass_none_exception_defined():
    """Wait for a function that raises an exception, when any exception is defined on the decorator.
    Should run thrice and raise the exception
    """
    run_data = {
        "times_ran": 0
    }

    @wait_for_pass()
    def func():
        run_data["times_ran"] += 1
        raise ZeroDivisionError

    with pytest.raises(ZeroDivisionError):
        func()

    assert run_data["times_ran"] == 3


def test_wait_for_pass_indefinitely():
    """Wait for a function that raises an exception when it runs 15 times, while setting wait_for_pass retries=0.
    Should run 15 times and raise no exceptions
    """
    run_times = 15
    run_data = {
        "times_ran": 0
    }

    @wait_for_pass(retries=0)
    def func():
        run_data["times_ran"] += 1
        if run_data["times_ran"] < run_times:
            raise ZeroDivisionError

    func()

    assert run_data["times_ran"] == run_times


def test_wait_for_pass_delay():
    """Wait for a function that raises an exception, setting wait_for_pass retries=5 and retries_delay_1.
    Should end in at least 5 seconds
    """
    @wait_for_pass(retries=5, retries_delay=1)
    def func():
        raise ZeroDivisionError

    with expect_time(expected=5, more=True):
        with pytest.raises(ZeroDivisionError):
            func()
