"""Module with simplest server that read data from socket do some task and send answer."""

from base_srv import BaseCBServer
import tasks


def serverCreator(accept_handler, read_handler, disconnect_handler = None, **kwargs):
    """Create emplementation of call-back serever with using 
        accept_handler - for handling incoming connactions,
        read_handler  - for handling read-write process with current client,
        disconnect_handler - for handling process of disconnecting clients or it self.
    """
    new_class_name = "CallBackServer"
    new_class_atributes = kwargs
    new_class_atributes["_on_accept_ready"]  = accept_handler
    new_class_atributes["_on_read_ready"]  = read_handler
    new_class_atributes["do_tasks"] = tasks.do_tasks

    return type(new_class_name, (BaseCBServer,), new_class_atributes)
