from abc import ABC
from typing import Optional, Tuple
from uuid import uuid5, NAMESPACE_URL

import boto3
from botocore import exceptions

from entity import Task, TaskMutationRequest

CONTENT_FIELD = "content"
TASK_UUID_FIELD = "taskUUID"


class TaskRepository(ABC):
    def create_task(self, ctx, req: TaskMutationRequest) -> Tuple[Optional[str], bool]:
        pass

    def get_task_by_uuid(self, ctx, task_uuid: str) -> Tuple[Optional[Task], bool]:
        pass

    def update_task(self, ctx, task_uuid: str, req: TaskMutationRequest) -> bool:
        pass

    def delete_task(self, ctx, task_uuid: str) -> bool:
        pass


TASK_UUID_SEED = uuid5(NAMESPACE_URL, "task_uuid/miD7yYiWZq")


class DynamoDBTaskRepository(TaskRepository):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Tasks')

    def create_task(self, ctx, req: TaskMutationRequest) -> Tuple[Optional[str], bool]:
        """
        Create a task in the DB

        Returns
        -------
        The UUID of the newly created task. Bool is set to true if task was created successfuly, false if a task with
        the same ID already exists.
        """
        task_uuid = str(uuid5(TASK_UUID_SEED, ctx.aws_request_id))
        try:
            self.table.put_item(
                Item={
                    TASK_UUID_FIELD: str(task_uuid),
                    CONTENT_FIELD: str(req.content),
                },
                ConditionExpression='attribute_not_exists(taskUUID)',
            )

        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
            return task_uuid, False

        return task_uuid, True

    def get_task_by_uuid(self, ctx, uuid: str) -> Tuple[Optional[Task], bool]:
        """
        Get a task by its UUID.

        Returns
        -------
        The task and a boolean. Boolean is true if the task exists, false otherwise.

        """
        response = self.table.get_item(
            Key={
                TASK_UUID_FIELD: str(uuid),
            }
        )

        item = response.get("Item")
        if item is None:
            return None, False

        return Task(
            id=item.get(TASK_UUID_FIELD),
            content=item.get(CONTENT_FIELD),
        ), True

    def update_task(self, ctx, task_uuid: str, req: TaskMutationRequest) -> bool:
        """
        Update a task.

        Returns
        -------
        Return false if the task does not exist, true otherwise.

        """
        try:
            self.table.put_item(
                Item={
                    TASK_UUID_FIELD: str(task_uuid),
                    CONTENT_FIELD: str(req.content),
                },
                ConditionExpression='attribute_exists(taskUUID)',
            )

        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
            return False

        return True

    def delete_task(self, ctx, task_uuid: str) -> bool:
        pass
        try:
            self.table.delete_item(
                Key={
                    TASK_UUID_FIELD: str(task_uuid),
                },
            )

        except exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise
            return False

        return True
