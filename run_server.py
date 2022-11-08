from nb_server import NoBlockingServer

if __name__== "__main__":
    srv = NoBlockingServer()

    srv.main_process_loop()
    print('Конец.')