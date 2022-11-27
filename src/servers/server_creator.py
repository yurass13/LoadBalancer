"""Module contains base class for the call-back server and function server creator."""
from .base_cb_server import BaseCBServer


def create_server(accept_handler, read_handler, disconnect_handler = None, **kwargs):
    """Create instance of call-back serever.
        Parameters: 
            accept_handler: function - for handling incoming connections,
            read_handler: function - for handling read-write process with current connection,
            disconnect_handler: function - for handling process of disconnecting.
            **kwargs - another dependencies needed for working process.

        Return:
            Instance of callback server based on BaseCBServer and Parameters. 
    """
    new_class_name = "CallBackServer"
    new_class_atributes = kwargs
    new_class_atributes["_on_accept_ready"]  = accept_handler
    new_class_atributes["_on_read_ready"]  = read_handler
    new_class_atributes["_on_disconnect"] = disconnect_handler

    return type(new_class_name, (BaseCBServer,), new_class_atributes)()

