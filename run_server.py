import server_creator as sc
import event_handlers as eh

if __name__== "__main__":
    srv =  sc.serverCreator(
        accept_handler = eh.on_accept_ready,
        read_handler = eh.handle_connection,
        disconnect_handler = eh.on_disconnect,
        on_connect  = eh.on_connect,
    )()

    srv.run()