"""simplest tcp client"""

from random import randint
from time import sleep


from socket import socket
from socket import AF_INET, SOCK_STREAM


def run_simple_client() -> None:
    """Target function for running current client.

    Args:
        client (SimpleClient): target client for processing.
    """
    client = SimpleClient()
    value = randint(0, 20)
    print(client.tcp_socket.getsockname(), "Generated value:{}".format(value))
    while value >= 0:
        sleep(1)
        client.data_provider = str(value)
        value = int(client.data_provider)



class SimpleClient:
    """Class for creating simplest tcp client and sanding data for server."""
    def __init__(self, ip = '127.0.0.1', port = 9090):
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.connect((ip, port))

    def _set_data(self, send_data):
        send_data = send_data.encode('utf-8')
        self.tcp_socket.send(send_data)

    def _get_data(self):
        recv_data = self.tcp_socket.recv(1024)
        recv_data = recv_data.decode('utf-8')
        return recv_data

    data_provider = property(_get_data, _set_data)

    def __del__(self):
        self.tcp_socket.close()
