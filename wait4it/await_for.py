"""WAIT FOR
Async wait_for (not compatible with Python 2)
"""

import socket
import asyncio
from time import time
from contextlib import closing

from .exceptions import WaitForTimeoutError

__all__ = ("await_for",)


async def _await_for_single(host, port, polling_freq, timeout, raise_error):
    have_timeout = bool(timeout)

    if have_timeout:
        start_time = time()

    while True:
        writer = None
        try:
            # TODO Failing if closed (not closing errored conns?)
            coro = asyncio.open_connection(host=host, port=port)
            if have_timeout:
                _, writer = await asyncio.wait_for(coro, timeout=timeout)
            else:
                _, writer = await coro
            return True

        except ConnectionError:
            # noinspection PyUnboundLocalVariable
            if have_timeout and time() - start_time >= timeout:
                if raise_error:
                    raise WaitForTimeoutError(host=host, port=port)
                else:
                    return False
            else:
                await asyncio.sleep(polling_freq)

        finally:
            if writer:
                writer.close()


async def await_for(*ports, polling_freq=0.25, timeout=15, raise_error=True):
    """Wait asynchronously for one or multiple given TCP ports to be reachable.
    :param ports: target port to wait for
    :type ports: str | int
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
    hosts_ports = list()  # [("127.0.0.1", "80"), ("127.0.0.1", "22")]
    for input_port in ports:
        if type(input_port) is int or ":" not in input_port:
            hosts_ports.append(("127.0.0.1", str(input_port)))
        else:
            chunks = input_port.split(":")
            hosts_ports.append((chunks[0], chunks[1]))

    results_bool = await asyncio.gather(*[
        _await_for_single(host=host, port=port, polling_freq=polling_freq, timeout=timeout, raise_error=raise_error)
        for host, port in hosts_ports
    ])

    results_dict = dict()
    for i, host_port in enumerate(hosts_ports):
        results_dict[":".join(host_port)] = results_bool[i]

    return results_dict
