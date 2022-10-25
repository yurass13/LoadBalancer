"""Sample of simple_server processing."""
from simple_server import SimpleServer

if __name__ == "__main__":
    # Create server object
    srv = SimpleServer()

    srv.wait_client()
    print('Processing ...')

    # Обмениваемся бредом
    data = srv.data_provider
    for num in range(int(data)):
        srv.data_provider = str(num)
    print('Complete!')
    print(srv.data_provider)
    del srv.data_provider
    print("Server is shutdown.")