from unittest.mock import MagicMock

import pytest

from controller import Controller
from entity import GetTaskRequest, UpdateTaskRequest, TaskMutationRequest, DeleteTaskRequest, CreateTaskRequest
from repository import TaskRepository


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def controller(mock_repository):
    return Controller(mock_repository)


@pytest.fixture
def ctx():
    return None


def test_create_task(ctx, controller, mock_repository: TaskRepository):
    result = ("bla", True)
    mut = TaskMutationRequest(content='content')
    mock_repository.create_task = MagicMock(return_value=result)
    assert result == controller.create_task(ctx, CreateTaskRequest(mutation=mut))
    mock_repository.create_task.assert_called_once_with(ctx, mut)


def test_get_task(ctx, controller, mock_repository: TaskRepository):
    result = ("aa", True)
    mock_repository.get_task_by_uuid = MagicMock(return_value=result)
    assert result == controller.get_task(ctx, GetTaskRequest(id='test'))
    mock_repository.get_task_by_uuid.assert_called_once_with(ctx, "test")


def test_update_task(ctx, controller, mock_repository: TaskRepository):
    mut = TaskMutationRequest(content='content')
    mock_repository.update_task = MagicMock(return_value=True)
    assert True == controller.update_task(ctx, UpdateTaskRequest(id='test',
                                                                 mutation=mut))
    mock_repository.update_task.assert_called_once_with(ctx, 'test', mut)


def test_delete_task(ctx, controller, mock_repository: TaskRepository):
    mock_repository.delete_task = MagicMock(return_value=True)
    assert True == controller.delete_task(ctx, DeleteTaskRequest(id='test'))
    mock_repository.delete_task.assert_called_once_with(ctx, 'test')
