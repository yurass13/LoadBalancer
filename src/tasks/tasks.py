"""Module with tasks and task_handlers for server."""
# TODO клиент должен иметь возможность получить список задач и
# алгоритм его действий при работе с сервером.(Порядок отправки и получения сообщений с
# кодом задачи и кодом действия.)
def get_task_list():
    ""
    return [
        "default",
        "another_task"
    ]

def get_task_by_name(name: str="default"):
    """Default task getter method.
        Return worker-function by name.
    """
    try:
        return {
            "default" : _task_send_decrement,
            "another_task": _another_task,
        }[name]
    except KeyError:
        raise ValueError(
            "Unknown value! Can't find task with name {}!".format(
                name
            )
        )

# Tasks
def _task_send_decrement(sender, _conn, **kwargs):
    """Send to current connection value - 1."""
    sender.send(_conn, int(kwargs["value"]) - 1)

def _another_task(sender, _conn, **kwargs):
    """Task template."""
    sender.send(
        _conn,
        "{}".format(
            kwargs
        )
    )

    print("Send some data for client")
    pass
