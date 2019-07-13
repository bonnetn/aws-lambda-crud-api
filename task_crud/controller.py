from typing import Optional, Tuple

from entity import Task, GetTaskRequest, CreateTaskRequest, UpdateTaskRequest, DeleteTaskRequest
from repository import TaskRepository


class Controller:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, ctx, req: CreateTaskRequest) -> Tuple[Optional[str], bool]:
        return self.repository.create_task(ctx, req.mutation)

    def get_task(self, ctx, req: GetTaskRequest) -> Tuple[Optional[Task], bool]:
        return self.repository.get_task_by_uuid(ctx, req.id)

    def update_task(self, ctx, req: UpdateTaskRequest) -> bool:
        return self.repository.update_task(ctx, req.id, req.mutation)

    def delete_task(self, ctx, req: DeleteTaskRequest) -> bool:
        return self.repository.delete_task(ctx, req.id)
