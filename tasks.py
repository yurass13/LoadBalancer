"""Module with tasks and task_handlers for server."""

# Handlers

def do_tasks(server):
    """Simple task handler.
        Just owerride server abstract method and it'll done.
    """
    # Забираем первую таску из списка и отдаем на обработку
    task = server._tasks.pop(0)

    # Получаем функцию для исполнения таски по ее имени
    target = get_task_by_name(task['name'])
    
    if target is None:
        print(
            "Task {name} is not avaliable".format(
                name = task['name']
            )
        )
    try:
        target(
            sender = server,
            value = task['args'],
            target = task['client']
        )
    except Exception as ex:
        print("Task processing was unsuccesfull!")
        print(ex)

# Servise

def get_task_by_name(name):

    if name == "default":
        return _task_send_decrement
    else:
        return None

# Tasks

def _task_send_decrement(sender, target: int, value):
    sender.send(target, int(value) - 1)
