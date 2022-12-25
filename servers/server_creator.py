"""Module contains base class for the call-back server and function server creator."""
from .base_cb_server import BaseCBServer
from .event_handlers import get_handlers_strategy


def server_factory(server_assignment: str = "default") -> BaseCBServer:
    """ Using server_type as create instance of call-back serever.

        Parameters:
        server_name: str,
            "default" | "data_storage" | "balancer" | ...

        Returns:
            Instance of callback server based on BaseCBServer by server_type. 
    """
    try:
        class_name, class_atributes = get_handlers_strategy(server_assignment)
        # print(f"Handlers choosed {class_name}")
    except KeyError:
        raise ValueError("Unknown assigment!")

    return type(class_name, (BaseCBServer, ), class_atributes)()
