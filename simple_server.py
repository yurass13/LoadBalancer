"""Module with simplest server that read data from socket do some task and send answer."""
from base_srv import BaseLocalServer

class SimpleServer(BaseLocalServer):
    """
        Server for processing with only one client.
        Using connections for connectios.
    """
    def __init__(self, queue_limit = 4, connections_limit = 2):
        super().__init__(queue_limit, connections_limit)
        self._clients = {}

    def main_process_loop(self):
        current_id = None
        while(True):
            # Если есть таски выполняем 
            for _ in self._tasks:
                self._do_tasks()

            if current_id is None:
                current_id = self.accept_connection()
            else:
                value = self._handle_connection(current_id)

                # Если обработчик вернул 0 клиент помечается на удаление
                if value == 0:
                    print("Disconnect user:", current_id)
                    del self._clients[current_id]
                    current_id = None