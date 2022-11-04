"""Module with client storage."""

from uuid import uuid1
from socket_data_provider import SocketDataProvider


class ConnectionStorage:
    """Storage for processing with active connections. 
        client_storage.add((socket, address)) -> self.connections; self._address

        client_storage() -> [id,]
        client_storage[id] -> DataProvider - property 

        client_storage.get_address(id)
    """
    def __init__(self) -> None:
        self._connections = {}


    def __getitem__(self, __id: int) -> str:
        return self._connections[__id].data_provider


    def __setitem__(self, __id: int, __value: str):
        self._connections[__id].data_provider = __value


    def __delitem__(self, __id: int) -> None:
        self._connections[__id].close_connection()
        del self._connections[__id]


    def __len__(self):
        return len(self._connections)


    def __iter__(self):
        return self._connections.__iter__()


    def keys(self):
        return list(self._connections.keys())


    def add(self, __value: tuple) -> int:
        conn_id = uuid1()
        self._connections[conn_id] = SocketDataProvider(__value)
        return conn_id


    def get_addres(self, __id: int):
        return self._connections[__id].get_address()


    def read_data(self, __id):
        return self._connections[__id]


    def send_data(self,__id, send_data):
        self._connections[__id] = send_data


    def close_connection(self):
        # Cotyl' dlya proverki
        current_id = list(self.connections.keys())
        print("[{client[0]}] disconnected!".format(
                client = self.connections.get_addres(current_id[0])
            )
        )
        self.connections[current_id[0]].close()
