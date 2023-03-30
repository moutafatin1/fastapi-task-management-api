from app.exceptions import NotFound


class TaskNotFound(NotFound):
    def __init__(self, id: int):
        self.id = id

    DETAIL = f"The task with the id: {id} does not exists"
