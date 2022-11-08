"""Module with tasks for server."""

def get_task_by_name(name):
    match name:
        case 'default':
            return _task_send_decrement

def _task_send_decrement(sender, target_id: int, value):
    sender.send(target_id, int(value) - 1)