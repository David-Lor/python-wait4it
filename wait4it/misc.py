"""MISC
Other tools provided on the wait4it library
"""

import socket
from contextlib import closing

__all__ = ("get_free_port",)


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
