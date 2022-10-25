"""Module with simplest server that read data from socket do some task and send answer."""

from time import sleep
from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)

class SimpleServer:
    """Server for processing with only one client."""
    def __init__(self, ip= '', port=9090, connections_limit = 1):
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        # Освобождаем порт
        self.host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        
        self.host_socket.bind((ip, port))
        self.host_socket.listen(connections_limit)
        self._connection = None
        self.client_address = None

    def wait_client(self):
        print('Waiting for new connection...')
        connection, client_address = self.host_socket.accept()
        self._connection = connection
        self.client_address = client_address
        print('[{client[0]}] connected!\n'.format(client = client_address))


    def read_data(self):
        recv_data = self._connection.recv(1024)
        return recv_data.decode('utf-8')

    def send_data(self, send_data):
        self._connection.send(send_data.encode('utf-8'))
        sleep(1)

    def close_connection(self):
        print("[{client[0]}] disconnected!".format(client = self.client_address))
        self._connection.close()

    data_provider = property(read_data, send_data, close_connection)
