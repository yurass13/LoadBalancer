"""Base class for the call-back server."""
from abc import abstractclassmethod

import selectors

from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)


class BaseCBServer:
    def __init__(self, queue_limit = 4, connections_limit = 2):
        self._host_socket = socket(AF_INET, SOCK_STREAM)
        # AF_INET - протокол IPv4 (аналоги AF_INET6 - IPv6; AF_IPX - IPX; AF_UNIX - Unix сокеты.)
        # SOCK_STREAM - TCP протокол (аналог SOCK_DGRAM)

        # SO_REUSEADDR - освобождаем порт не дожидаясь таймаута
        self._host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

        self._host_socket.bind(('localhost', 9090))

        # Ограничения для очереди на подключение 
        # по-умолчанию делаем ее немного больше, чем количество доступных подключений.
        # Ограничение количества подключений
        self._queue_limit = queue_limit
        self._host_socket.listen(self._queue_limit)
        self._connections_limit = connections_limit
        
        self.selector = selectors.DefaultSelector()
        self.selector.register(self._host_socket, selectors.EVENT_READ, self._on_accept_ready)

        self._tasks = []
        # Хранилище для ptp подключений
        self._connections = {}

    def run(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
            for _ in self._tasks:
                self.do_tasks()

    @abstractclassmethod
    def do_tasks(self):

        pass 