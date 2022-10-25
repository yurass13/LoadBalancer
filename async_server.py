"""Module with simplest server that read data from socket do some task and send answer."""

from sys import addaudithook
import uuid
from time import sleep
from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)

class AsyncServer:
    """Server for processing with several clients."""
    def __init__(self, ip= '', port=9090, connections_limit = 2):
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        # Освобождаем порт
        self.host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        
        self.host_socket.bind((ip, port))
        self.host_socket.listen(connections_limit)
        self.addresses = {}
        self._connections = {}

    def wait_client(self):
        print('Waiting for new connection...')
        connection, client_address = self.host_socket.accept()
        self.addresses[uuid.uuid1()] = client_address
        self._connections[client_address] = connection

        print('[{client[0]}] connected!\n'.format(client = client_address))


    def read_data(self, id):
        recv_data = self._connections[self.addresses[id]].recv(1024)
        return recv_data.decode('utf-8')

    def send_data(self, id, send_data):
        self._connections[self.addresses[id]].send(send_data.encode('utf-8'))
        sleep(1)

    def close_connection(self, id):
        print("[{client[0]}] disconnected!".format(client = self.addresses[id]))
        del self._connections[self.addresses[id]]
        self._connections[self.addresses[id]].close()

    data_provider = property(read_data, send_data, close_connection)
