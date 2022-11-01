"""Module with simplest server that read data from socket do some task and send answer."""

from time import sleep
from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)

from connections_storage import ConnectionStorage

class SimpleServer:
    """
        Server for processing with only one client.
        Using storage for connectios.
    """
    def __init__(self, ip= '', port=9090, queue_limit = 1, connections_limit = 1):
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        # Освобождаем порт
        self.host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        
        self.host_socket.bind((ip, port))
        self.queue_limit = queue_limit
        self.connections_limit =connections_limit
        self.host_socket.listen(queue_limit)
        self.storage = ConnectionStorage()

    def wait_client(self):
        print('Waiting for new connection...')
        current_id = self.storage.add(self.host_socket.accept())
        print('[{client[0]}] connected!\n'.format(
                client = self.storage.get_addres(current_id)
            )
        )


    def read_data(self):
        # Cotyl' dlya proverki
        current_id = list(self.storage.keys())
        print(current_id[0])
        recv_data = self.storage[current_id[0]].recv(1024)
        return recv_data.decode('utf-8')

    def send_data(self, send_data):
        # Cotyl' dlya proverki
        current_id = list(self.storage.keys())
        self.storage[current_id[0]].send(send_data.encode('utf-8'))
        sleep(1)

    def close_connection(self):
        # Cotyl' dlya proverki
        current_id = list(self.storage.keys())
        print("[{client[0]}] disconnected!".format(
                client = self.storage.get_addres(current_id[0])
            )
        )
        self.storage[current_id[0]].close()

    data_provider = property(read_data, send_data, close_connection)

    def _check_limit(self) -> bool:
        """Return True if server have able for connect new user."""