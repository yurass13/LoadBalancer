
from time import sleep


class SocketDataProvider:
    """Data provider for simple work with IO on current socket."""
    def __init__(self, __data):
        self._connection = __data[0]
        self._address = __data[1]


    def read_data(self):
        try:
            recv_data = self._connection.recv(1024)
            recv_data = recv_data.decode('utf-8')
            return recv_data
        except ConnectionError:
            print("Connection suddenly closed while receiving!")
            return None

    def send_data(self, send_data):
        try:
            self._connection.send(send_data.encode('utf-8'))
        except ConnectionError:
            print("Client suddenly closed, cannot send!")
            sleep(1)

    def close_connection(self):
        print("[{client[0]}] disconnected!".format(
                client = self._address
            )
        )
        self._connection.close()

    data_provider = property(read_data, send_data, close_connection)


    def get_address(self):
        return self._address
