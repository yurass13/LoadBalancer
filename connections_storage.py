"""Module with client storage."""

from socket import socket
from uuid import uuid1

class ConnectionStorage:
    """Storage for processing with active connections. 
        client_storage.add((socket, address)) -> self.connections; self._address

        client_storage() -> [id,]
        client_storage[id] -> socket() (with connection)

        client_storage.get_address(id)
    """
    def __init__(self) -> None:
        self._connections = {}
        self._address= {}


    def __getitem__(self, __id: int) -> socket:
        return self._connections[__id]


    def __delitem__(self, __id: str) -> None:
        self._connections[__id].close()
        del self._connections[__id]
        del self._address[__id]


    def __len__(self):
        return len(self._connections)


    def __call__(self) -> list:
        return self._connections.keys()


    def keys(self):
        return self._connections.keys()


    def add(self, __value: tuple) -> int:
        conn_id = uuid1()
        self._connections[conn_id] = __value[0]
        self._address[conn_id] = __value[1]
        return conn_id


    def get_addres(self, __id: int):
        return self._address[__id]
