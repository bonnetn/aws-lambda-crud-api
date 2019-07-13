import logging
from typing import Optional, Tuple

from entity import Task, GetTaskRequest, CreateTaskRequest, UpdateTaskRequest, DeleteTaskRequest
from repository import TaskRepository


class Controller:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, ctx, req: CreateTaskRequest) -> Tuple[Optional[str], bool]:
        logging.debug("create_task controller called")
        return self.repository.create_task(ctx, req.mutation)

    def get_task(self, ctx, req: GetTaskRequest) -> Tuple[Optional[Task], bool]:
        logging.debug("get_task controller called")
        return self.repository.get_task_by_uuid(ctx, req.id)

    def update_task(self, ctx, req: UpdateTaskRequest) -> bool:
        logging.debug("update_task controller called")
        return self.repository.update_task(ctx, req.id, req.mutation)

    def delete_task(self, ctx, req: DeleteTaskRequest) -> bool:
        logging.debug("delete_task controller called")
        return self.repository.delete_task(ctx, req.id)
