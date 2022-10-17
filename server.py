"""Module with simplest server that read data from socket do some task and send answer."""

import enum
from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)

class ConnectionStatus(enum.Enum):

    CL_DISCONNECTED = 0
    CL_CONNECTED = 1
    CL_SENDING_DATA = 2
    CL_LISTEN_DATA =3
    CL_TIMEOUT = 8
    CL_ER_CONNECTION = 9

class SimpleServer:
    def __init__(self, ip= '127.0.0.1', port=8080):
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        # Освобождаем порт
        self.host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        self.host_socket.bind((ip, port))
        self._connection = None
        self.client_address = None

    def wait_client(self):
        self.host_socket.listen(128)
        connection, client_address = self.host_socket.accept()
        self._connection = connection
        self.client_address = client_address

    def get_from_soc(self):
        # Ждем подключения клиента и готовимся к получению данных
        self.wait_client()
        recv_data = self._connection.recv(1024)
        return recv_data.decode('utf-8')

    def send_to_soc(self, send_data):
        self._connection.send(send_data.encode('utf-8'))

    def del_soc(self):
        self._connection.close()

    data_provider = property(get_from_soc, send_to_soc, del_soc)

if __name__ == '__main__':
    # Start server
    srv = SimpleServer()
    # Read data from socket
    value = 0
    while(True):
        from_client = srv.data_provider
        print(
                '[{ip}]'.format(ip = srv.client_address),
                from_client
            )
        # Write data to socket
        srv.data_provider = "some_shit"
