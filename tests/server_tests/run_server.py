from .... import LoadBalancer as sc

if __name__== "__main__":
    srv =  sc.create_server(
        accept_handler = sc.handlers.on_accept_ready,
        read_handler = sc.handlers.handle_connection,
        disconnect_handler = sc.handlers.on_disconnect,
        on_connect  = sc.handlers.on_connect,
    )

    srv.run()
