"""Module with simplest server that read data from socket do some task and send answer."""
from select import select
from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from time import sleep

from connections_storage import ConnectionStorage

class SimpleServer:
    """
        Server for processing with only one client.
        Using connections for connectios.
    """
    def __init__(self, ip= 'localhost', port=9090, queue_limit = 4, connections_limit = 2):
        # Создаем серверный сокет
        self.host_socket = socket(AF_INET, SOCK_STREAM)
        # AF_INET - протокол IPv4 (аналоги AF_INET6 - IPv6; AF_IPX - IPX; AF_UNIX - Unix сокеты.)
        # SOCK_STREAM - TCP протокол (аналог SOCK_DGRAM)

        # SO_REUSEADDR - освобождаем порт не дожидаясь таймаута
        self.host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

        # Биндим сокет на полученные в ip и port  
        self.host_socket.bind((ip, port))

        # Инициализация остальных внутренних "приколюх"
        # Ограничения для очереди на подключение 
        # по-умолчанию делаем ее немного больше, чем количество доступных подключений.
        self.queue_limit = queue_limit

        # Ограничение количества подключений
        self.connections_limit = connections_limit
        self.host_socket.listen(queue_limit)

        # Контейнер для хранения клиент сокетов с активными подключениями. 
        # (Тут нужно еще подумать над реализацией т.к. для кооперативного ПОДХОДА они НЕ ПОДХОДЯТ.
        # TODO после реализации рабочего сервера на селекторах переписать и не позориться.)
        self.connections = ConnectionStorage()


    def wait_client(self) -> int:
        print('Waiting for new connection...')
        current_id = self.connections.add(self.host_socket.accept())
        print('[{client[0]}] connected!\n'.format(
                client = self.connections.get_addres(current_id)
            )
        )
        return current_id

    def main(self):
        while True:
            if self._check_limit():
                current_id = self.wait_client()
                self._handle_connection(current_id)
                print(len(self.connections))
            else:
                break

    def _check_limit(self) -> bool:
        """Return True if server have able for connect new user."""
        if len(self.connections) < self.connections_limit:
            return True
        return False


    def _handle_connection(self, _id):
        data = self.connections[_id] 
        for num in range(int(data)):
            sleep(1)
            self.connections[_id] = str(num)

        del self.connections[_id]