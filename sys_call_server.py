"""Module with simplest server that read data from socket do some task and send answer."""
from select import select
from socket import socket
from socket import (
    AF_INET,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR
)

import tasks


class SelectServer():
    """
        Server for processing with only one client.
        Using connections for connectios.
    """
    def __init__(self, queue_limit = 4, connections_limit = 2):
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

        self._tasks = []
        self._inputs = []
        self._inputs.append(self._host_socket)

    def accept_connection(self) -> None:
        ptp_connection, _ = self._host_socket.accept()
        
        self._inputs.append(ptp_connection)
        print("Connect user:", _)

    def send(self, client, message):
        client.send(str(message).encode('utf-8'))

    def recv(self, client):
        try:
            data = client.recv(1024).decode('utf-8')
            return 0 if (data is None) or (not data.isdigit()) else data
        except ConnectionError:
            print("ConnectionError")
            return 0

    def main_process_loop(self):
        while(True):
            readeble, writteble, exceptional = select(
                self._inputs,
                [],
                self._inputs
            )
            for sock in readeble:
                if sock == self._host_socket:
                    self.accept_connection()
                else:
                    value = self._handle_connection(sock)
                    if value == 0:
                        print("Disconnect user:", sock.getpeername())
                        self._inputs.remove(sock)

            for _ in self._tasks:
                self._do_tasks()

    def _handle_connection(self, client):
        """Take message with int from client and create task."""
        value = self.recv(client)
        if not value is None:
            if value != 0:
                self._tasks.append(
                    {
                        'task': "default",
                        'args': int(value),
                        'client': client,
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
                target = task['client']
            )
        except Exception as ex:
            print("Task processing was unsuccesfull!")
            print(ex)

    def _check_connections_limit(self) -> bool:
        return len(self._clients) <= self._connections_limit
