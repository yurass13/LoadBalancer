"""Module with base class for server."""

from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)
from uuid import uuid1

import tasks


class BaseLocalServer:
    """Base class for the server."""

    def __init__(self, queue_limit = 4, connections_limit = 2) -> None:
        self._host_socket = socket(AF_INET, SOCK_STREAM)
        # AF_INET - протокол IPv4 (аналоги AF_INET6 - IPv6; AF_IPX - IPX; AF_UNIX - Unix сокеты.)
        # SOCK_STREAM - TCP протокол (аналог SOCK_DGRAM)

        # SO_REUSEADDR - освобождаем порт не дожидаясь таймаута
        self._host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

        self._host_socket.bind(('localhost',9090))

        # Ограничения для очереди на подключение 
        # по-умолчанию делаем ее немного больше, чем количество доступных подключений.
        # Ограничение количества подключений
        self._queue_limit = queue_limit
        self._host_socket.listen(self._queue_limit)
        self._connections_limit = connections_limit

        # Сюда складываем наших ptp соединения
        # Обязательно переопределить при наследовании
        self._clients = None

        self._tasks = []


    def send(self, client_id, message):
        self._clients[client_id]['conn'].send(str(message).encode('utf-8'))

    def recv(self, client_id):
        try:
            client_conn = self._clients[client_id]['conn']
            data = client_conn.recv(1024).decode('utf-8')
            return 0 if (data is None) or (not data.isdigit()) else data
        except ConnectionError:
            print("ConnectionError")
            return 0

    def accept_connection(self) -> int:
        """Client connection logic."""
        if self._check_connections_limit():
            new_id = uuid1()
            ptp_connection, address = self._host_socket.accept()
            if ptp_connection is None:
                return None 

            self._clients[new_id] = {
                'conn':ptp_connection,
                'address': address,
            }
            print("Connect user:", new_id)
            print("Address:", address)
            return new_id


    def _check_connections_limit(self) -> bool:
        return len(self._clients) <= self._connections_limit

    def _handle_connection(self, client_id):
        """Take message with int from client and create task."""
        value = self.recv(client_id)
        if not value is None:
            if value != 0:
                self._tasks.append(
                    {
                        'task': "default",
                        'args': int(value),
                        'client': client_id,
                    }
                )
        return value

    def _do_tasks(self):
        # Забираем первую таску из списка и отдаем на обработку
        task = self._tasks.pop(0)

        # Получаем функцию для исполнения таски по ее имени
        target = tasks.get_task_by_name(task['task'])
        
        if target is None:
            print(
                "Task {name} is not avaliable".format(
                    name = task['task']
                )
            )
        try:
            target(
                sender = self,
                value = task['args'],
                target_id = task['client']
            )
        except Exception as ex:
            print("Task processing was unsuccesfull!")
            print(ex)
