"""simplest tcp client"""

from socket import socket
from socket import AF_INET, SOCK_STREAM

class SimpleClient:
    """Class for creating simplest tcp client and sanding data for server."""
    def __init__(self, ip = '127.0.0.1', port = 8080):
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


if __name__ == '__main__':
    client = SimpleClient()
    client.data_provider = "I'm new client!"
    print(client.data_provider)
