"""Module with simplest server that read data from socket do some task and send answer."""

from base_srv import BaseLocalServer


class NoBlockingServer(BaseLocalServer):
    """Server for processing with several clients."""

    def __init__(self, queue_limit = 4, connections_limit = 2):
        super().__init__(queue_limit, connections_limit)

        # Делаем сокет не блокируемым
        self._host_socket.setblocking(0)
        # Переопределяем поле
        self._clients = {}


    def recv(self, client_id):
        try:
            new_id =  super().recv(client_id)
        except BlockingIOError:
            return None
        return new_id

    def main_process_loop(self):
        while(True):
            # Если есть таски выполняем 
            for _ in self._tasks:
                self._do_tasks()

            # Обрабатываем подключения
            if len(self._clients)>0:
                # Храним клиентов для удаления
                disconnected = []
                for c_id in self._clients:
                    value = self._handle_connection(c_id)

                    # Если обработчик вернул None клиент помечается на удаление
                    if value == 0:
                        disconnected.append(c_id)

                for c_id in disconnected:
                    print("Disconnect user:",c_id)
                    del self._clients[c_id]

            self.accept_connection()

    def accept_connection(self) -> int:
        try:
            new_id = BaseLocalServer.accept_connection(self)
            self._clients[new_id]['conn']
            return new_id
        except BlockingIOError:
            return None


            