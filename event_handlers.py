"""Module contains custom event handlers for input to server-creator."""

from selectors import EVENT_READ
from uuid import uuid1


def on_accept_ready(self, sock, mask) -> int:
    """

    """
    ptp_connection, _ = self._host_socket.accept()
    uid = uuid1()
    self._connections[uid] = ptp_connection
    self.selector.register(ptp_connection, EVENT_READ, self._on_read_ready)
    if self.on_connect:
        self.on_connect(uid)
    return uid

def on_read_ready():
    """

    """
    print("on_ready_read handler.")


def on_connect(self, uid):
    """Console log for 'accept new connection' event."""
    print(f"User[{uid}] from {self._connections[uid].getpeername()} connected!")

def on_disconnect(self, uid, address):
    """Console log for 'close current ptp connection' event."""
    print(f"User[{uid}] from {address} disconnected!")


def send(self, client, message):
    """Decorator. Encode message before sending for current client."""
    client.send(str(message).encode('utf-8'))

def recv(self, client):
    """
        Decorator.
        Decode message from current client before return and
        handling ConnectionError exception.
    """
    try:
        data = client.recv(1024).decode('utf-8')
        return 0 if (data is None) or (not data.isdigit()) else data
    except ConnectionError:
        # TODO hadling Connection error
        print("ConnectionError")
        return 0

def handle_connection(self, sock, mask):
    """Handling ready for reading ptp sockets.

        Alghorithm:
            1. Take message from client.
            2. Create task and uppend to queue.
    """
    value = self.recv(sock)
    if not value is None:
        if value != 0:
            self._tasks.append(
                {
                    'name': "default",
                    'args': int(value),
                    'client': sock,
                }
            )
    return value
