"""Module with run simple callback server logic."""
from src.servers import (
    create_server,
    event_handlers,
)

if __name__== "__main__":
    srv =  create_server(
        accept_handler = event_handlers.on_accept_ready,
        read_handler = event_handlers.handle_connection,
        disconnect_handler = event_handlers.on_disconnect,
        on_connect  = event_handlers.on_connect,
    )
    srv.run()
