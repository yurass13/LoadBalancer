"""Test for default server with connect of several clients."""

from multiprocessing import Process

from clients import run_simple_client
from servers import server_factory


def run_server() -> None:
    """Target function for running default server.
    """

    srv = server_factory()
    srv.run()


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
                target= run_simple_client,
                name = str(_)
                
            ) for _ in range(4)

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
