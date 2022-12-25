"""Module contains custom event handlers for input to server-creator."""

from selectors import EVENT_READ

def get_setup() -> tuple:
    """Retruns template for creating base server."""
    return (
        "DefaultServer",
        {
            '_on_accept_ready':_on_accept_ready,
            '_on_read_ready': _on_read_ready,
            '_on_disconnect': None,
            '_on_connect':_on_connect,
            '_on_disconnect': _on_disconnect,
        }
    )


def _on_accept_ready(self, sock, mask) -> int:
    """Handling accept connection event on the host socket.
        Parameters:
            sock:socket.socket - host socket
        Return:
            None
        Algorithm:
            1. Accept connection
            2. Register read event
            3. Call logging function
    """
    ptp_connection, _ = sock.accept()
    ptp_connection.setblocking(False)
    self.selector.register(ptp_connection, EVENT_READ, self._on_read_ready)
    if self._on_connect:
        self._on_connect(ptp_connection)


def _on_read_ready(self, _conn, mask):
    """Handling ready for reading ptp sockets.

        Alghorithm:
            1. Take message from connection.
            2. Create task and uppend to queue.
    """
    value = self.recv(_conn)
    if not value is None:
        if value != 0:
            self._tasks.append(
                {
                    'name': "default",
                    'args': int(value),
                    'connection': _conn,
                }
            )
        else:
            self._on_disconnect(_conn)
            self.selector.unregister(_conn)

# LOGGERS

def _on_connect(self, _conn):
    """Console log for 'accept new connection' event."""
    print(f"User from {_conn.getpeername()} connected!")


def _on_disconnect(self, _conn):
    """Console log for 'close current ptp connection' event."""
    print(f"User from {_conn.getpeername()} disconnected!")
