import json
from unittest.mock import MagicMock

import pytest

from controller import Controller
from entity import Task, GetTaskRequest, CreateTaskRequest, TaskMutationRequest, DeleteTaskRequest, UpdateTaskRequest
from handler import Handler


@pytest.fixture
def mock_controller():
    return MagicMock()


@pytest.fixture
def handler(mock_controller):
    return Handler(mock_controller)


@pytest.fixture
def stub_task():
    return Task(
        id='id',
        content='content',
    )


class TestCreateTask:
    @pytest.fixture
    def create_task_request_fixture(self):
        """ Generates API GW Event"""
        with open("unit/fixtures/create_task.json", "r") as f:
            return json.loads(f.read())

    def test_success(self, create_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        mock_controller.create_task = MagicMock(return_value=("id", True))
        result = handler.create_task(None, create_task_request_fixture)
        assert 200 == result.get('statusCode')
        mock_controller.create_task.assert_called_once_with(None, CreateTaskRequest(
            mutation=TaskMutationRequest(content='some content')))

    def test_controller_fail(self, create_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        mock_controller.create_task = MagicMock(return_value=(None, False))
        result = handler.create_task(None, create_task_request_fixture)
        assert 409 == result.get('statusCode')

    def test_missing_body(self, create_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        create_task_request_fixture['body'] = '{}'
        mock_controller.create_task = MagicMock(return_value=(None, False))
        result = handler.create_task(None, create_task_request_fixture)
        assert 400 == result.get('statusCode')


class TestGetTask:
    @pytest.fixture
    def get_task_request_fixture(self):
        """ Generates API GW Event"""
        with open("unit/fixtures/get_task.json", "r") as f:
            return json.loads(f.read())

    def test_success(self, get_task_request_fixture: dict, handler: Handler, mock_controller: Controller,
                     stub_task: Task):
        mock_controller.get_task = MagicMock(return_value=(stub_task, True))
        result = handler.get_task(None, get_task_request_fixture)
        assert 200 == result.get('statusCode')
        mock_controller.get_task.assert_called_once_with(None, GetTaskRequest(id='myid'))

    def test_without_query_param(self, get_task_request_fixture: dict, handler: Handler, mock_controller: Controller,
                                 stub_task: Task):
        del get_task_request_fixture['queryStringParameters']['id']
        mock_controller.get_task = MagicMock(return_value=(stub_task, True))
        result = handler.get_task(None, get_task_request_fixture)
        assert 400 == result.get('statusCode')

    def test_controller_fail(self, get_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        mock_controller.get_task = MagicMock(return_value=(None, False))
        result = handler.get_task(None, get_task_request_fixture)
        assert 404 == result.get('statusCode')


class TestUpdateTask:
    @pytest.fixture
    def update_task_request_fixture(self):
        """ Generates API GW Event"""
        with open("unit/fixtures/update_task.json", "r") as f:
            return json.loads(f.read())

    def test_success(self, update_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        mock_controller.update_task = MagicMock(return_value=True)
        result = handler.update_task(None, update_task_request_fixture)
        assert 204 == result.get('statusCode')
        mock_controller.update_task.assert_called_once_with(None, UpdateTaskRequest(id='myid',
            mutation=TaskMutationRequest(content='some content')))

    def test_id_not_in_body(self, update_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        update_task_request_fixture['body'] = '{"content":"something"}'
        mock_controller.update_task = MagicMock(return_value=True)
        result = handler.update_task(None, update_task_request_fixture)
        assert 400 == result.get('statusCode')

    def test_content_not_in_body(self, update_task_request_fixture: dict, handler: Handler,
                                 mock_controller: Controller):
        update_task_request_fixture['body'] = '{"id":"something"}'
        mock_controller.update_task = MagicMock(return_value=True)
        result = handler.update_task(None, update_task_request_fixture)
        assert 400 == result.get('statusCode')

    def test_not_found(self, update_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        mock_controller.update_task = MagicMock(return_value=False)
        result = handler.update_task(None, update_task_request_fixture)
        assert 404 == result.get('statusCode')


class TestDeleteTask:
    @pytest.fixture
    def delete_task_request_fixture(self):
        """ Generates API GW Event"""
        with open("unit/fixtures/delete_task.json", "r") as f:
            return json.loads(f.read())

    def test_success(self, delete_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        mock_controller.delete_task = MagicMock(return_value=True)
        result = handler.delete_task(None, delete_task_request_fixture)
        assert 204 == result.get('statusCode')
        mock_controller.delete_task.assert_called_once_with(None, DeleteTaskRequest(id='myid'))

    def test_fail(self, delete_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        mock_controller.delete_task = MagicMock(return_value=False)
        result = handler.delete_task(None, delete_task_request_fixture)
        assert 404 == result.get('statusCode')

    def test_id_not_in_body(self, delete_task_request_fixture: dict, handler: Handler, mock_controller: Controller):
        delete_task_request_fixture['body'] = '{}'
        mock_controller.delete_task = MagicMock(return_value=False)
        result = handler.delete_task(None, delete_task_request_fixture)
        assert 400 == result.get('statusCode')
