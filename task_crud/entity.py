from dataclasses import dataclass


@dataclass
class Task:
    id: str
    content: str


@dataclass
class TaskMutationRequest:
    content: str


@dataclass
class CreateTaskRequest:
    mutation: TaskMutationRequest


@dataclass
class GetTaskRequest:
    id: str


@dataclass
class UpdateTaskRequest:
    id: str
    mutation: TaskMutationRequest


@dataclass
class DeleteTaskRequest:
    id: str
