"""Module with simplest server that read data from socket do some task and send answer."""
from base_srv import BaseLocalServer

class SimpleServer(BaseLocalServer):
    """
        Server for processing with only one client.
        Using connections for connectios.
    """
    def __init__(self, queue_limit = 4, connections_limit = 2):
        super().__init__(queue_limit, connections_limit)
        self._clients = None
