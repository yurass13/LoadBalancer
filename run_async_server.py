"""Sample of simple_server processing."""
from async_server import AsyncServer

if __name__ == "__main__":
    # Create server object
    srv = AsyncServer()

    while True:
        srv.wait_client()
        print('Processing ...')

        target = srv.connections.items()[0][0]
        # Обмениваемся бредом
        data = srv.data_provider[target]
        for num in range(int(data)):
            srv.data_provider[target] = str(num)
        print('Complete!')
        print(srv.data_provider[target])
        del srv.data_provider[target]
        print("Server is shutdown.")