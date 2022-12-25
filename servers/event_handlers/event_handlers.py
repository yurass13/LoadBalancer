"""
"""
from . import default_event_handlers
from . import data_storage_event_handlers
from . import balancer_event_handlers

def get_handlers_strategy(server_assignment: str) -> tuple:
    """Strategy of server creation."""
    return {
        "default": default_event_handlers,
        "data_storage": data_storage_event_handlers,
        "balancer": balancer_event_handlers,
    }[server_assignment].get_setup()