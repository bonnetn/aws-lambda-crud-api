import json

from controller import Controller
from entity import GetTaskRequest, CreateTaskRequest, TaskMutationRequest, DeleteTaskRequest, UpdateTaskRequest

CONTENT_FIELD = "content"
ID_FIELD = "id"


class Handler:
    def __init__(self, controller: Controller):
        self.controller = controller

    def create_task(self, ctx, event) -> dict:
        body_json = event.get("body", "{}")
        body = json.loads(body_json)

        content = body.get(CONTENT_FIELD)
        if not content:
            return {"statusCode": 400, "body": f"'{CONTENT_FIELD}' is required in the body."}

        id, ok = self.controller.create_task(ctx, CreateTaskRequest(
            mutation=TaskMutationRequest(
                content=content,
            ),
        ))
        if not ok:
            return {"statusCode": 409}

        return {
            "statusCode": 200,
            "body": json.dumps({
                ID_FIELD: id,
            }),
        }

    def get_task(self, ctx, event) -> dict:
        query = event.get("queryStringParameters", {})
        task_id = query.get(ID_FIELD)
        if task_id is None:
            return {"statusCode": 400, "body": f"'{ID_FIELD}' query param is required."}

        task, ok = self.controller.get_task(ctx, GetTaskRequest(
            id=task_id
        ))
        if not ok:
            return {"statusCode": 404, "body": "Task not found."}

        return {
            "statusCode": 200,
            "body": json.dumps({
                ID_FIELD: task.id,
                CONTENT_FIELD: task.content,
            }),
        }

    def update_task(self, ctx, event) -> dict:
        body_json = event.get("body", "{}")
        body = json.loads(body_json)

        task_id = body.get(ID_FIELD)
        if not task_id:
            return {"statusCode": 400, "body": f"'{ID_FIELD}' is required in the body."}

        content = body.get(CONTENT_FIELD)
        if not content:
            return {"statusCode": 400, "body": f"'{CONTENT_FIELD}' is required in the body."}

        ok = self.controller.update_task(ctx, UpdateTaskRequest(
            id=task_id,
            mutation=TaskMutationRequest(
                content=content,
            ),
        ))
        if not ok:
            return {"statusCode": 404, "body": "Task not found."}

        return {"statusCode": 204}

    def delete_task(self, ctx, event) -> dict:
        body_json = event.get("body", "{}")
        body = json.loads(body_json)

        task_id = body.get(ID_FIELD)
        if not task_id:
            return {"statusCode": 400, "body": f"'{ID_FIELD}' is required in the body."}

        ok = self.controller.delete_task(ctx, DeleteTaskRequest(
            id=task_id,
        ))
        if not ok:
            return {"statusCode": 404, "body": "Task not found."}

        return {"statusCode": 204}
