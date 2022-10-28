"""Module with simplest server that read data from socket do some task and send answer."""


from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from connections_storage import ConnectionStorage


class AsyncServer:
    """Server for processing with several clients."""
    def __init__(
        self,
        ip= '',
        port=9090,
        connections_limit = 2
    ):
        # Подготовка сокета
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        self.host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        self.host_socket.setblocking(0)
        self.connections_limit = connections_limit
        # Настройка сокета 
        self.host_socket.bind((ip, port))
        self.host_socket.listen(connections_limit)
        
        # Переменные для хранения адресов клиентов и соединений с ними
        self._clients = ConnectionStorage()


    def wait_client(self):
        while True:
            # Check count of connected clients. 
            if len(self._clients) < self.connections_limit:
                # Connect new client and delegate process
                self._clients.add(self.host_socket.accept())
                


