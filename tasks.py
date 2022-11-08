"""Module with tasks for server."""

def get_task_by_name(name):
    match name:
        case 'default':
            return _task_send_decrement

def _task_send_decrement(sender, target: int, value):
    sender.send(target, int(value) - 1)