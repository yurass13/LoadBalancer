"""Test for default server with connect of several clients."""

from multiprocessing import Process

from random import random
from time import sleep

from clients import SimpleClient

from servers import (
    create_server,
    event_handlers,
)

def run_server() -> None:
    """Target function for running default server.
    """
    srv =  create_server(
        accept_handler = event_handlers.on_accept_ready,
        read_handler = event_handlers.handle_connection,
        disconnect_handler = event_handlers.on_disconnect,
        on_connect  = event_handlers.on_connect,
    )
    srv.run()

def run_client(client: SimpleClient) -> None:
    """Target function for running current client.

    Args:
        client (SimpleClient): target client for processing.
    """
    value = int(random() * 20)
    print(client.tcp_socket.getsockname(), "Generated value:{}".format(value))
    while value >= 0:
        sleep(1)
        # print("Try send {} to server.".format(value))
        client.data_provider = str(value)
        value = int(client.data_provider)
        # print("Recived data:", value)

def get_clients(count) -> list:
    """Init list of clients.

    Args:
        count (int): total count of clients

    Returns:
        list: contains SimpleClient objects
    """
    return [SimpleClient() for _ in range(count)]


if __name__ == "__main__":
    server_p = Process(
        target=run_server,
        name="server_process",
    )
    try:
        server_p.start()
    except Exception:
        print("Some troubles with server!")
        assert False
    try:
        clients_ps = [
            Process(
                target= run_client,
                name = str(client),
                args=(client,),
                
            ) for client in get_clients(4)
        ]
        for process in clients_ps:
            process.start()
        
        while any(
            [
                client.is_alive() 
                for client in clients_ps
            ]
        ):
            pass
        print("All client requests handled succesfull!")
        server_p.kill()
        print("server is stoped!")
    except Exception:
        print("Some client is break.")
        assert False
