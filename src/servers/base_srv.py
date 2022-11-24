"""Module contains base class for the call-back server."""

import selectors

from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)

import src.tasks.tasks as tasks


class BaseCBServer:
    """Base class for the callback server."""

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
        # TODO проверка количества подключений.
        self._queue_limit = queue_limit
        self._host_socket.listen(self._queue_limit)
        self._connections_limit = connections_limit
        
        self.selector = selectors.DefaultSelector()
        self.selector.register(self._host_socket, selectors.EVENT_READ, self._on_accept_ready)

        self._tasks = []


    def run(self):
        """Main loop.
            Algorithm:
                1. Select all events
                2. Call handlers for all events
                3. Do tasks
        """
        while True:
            # Обрабатываем события
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
            # TODO Перенести выполнение тасок на отдельный поток
            # Выполняем таски
            while len(self._tasks):
                self.do_task()


    def do_task(server):
        """Default task handler."""
        # Забираем первую таску из списка и отдаем на обработку
        task = server._tasks.pop(0)

        # Получаем функцию для исполнения таски по ее имени
        target = tasks.get_task_by_name(task['name'])
        
        if target is None:
            print(
                "Task {name} is not avaliable".format(
                    name = task['name']
                )
            )
        try:
            target(
                sender = server,
                value = task['args'],
                _conn = task['connection']
            )
        except Exception as ex:
            print("Task processing was unsuccesfull!")
            print(ex)


    def send(self, _conn, message):
        """Decorator for default socket.send with using .
            Encode message before sending for current connection."""
        _conn.send(str(message).encode('utf-8'))


    def recv(self, _conn):
        """Decorator for default socket.recv.
            Decode message from current connection before return and
            handling ConnectionError exception.
        """
        try:
            data = _conn.recv(1024).decode('utf-8')
            return 0 if (data is None) or (not data.isdigit()) else data
        except ConnectionError:
            # TODO hadling Connection error
            print("ConnectionError")
            return 0
