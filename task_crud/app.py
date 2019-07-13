# import requests
import json

from controller import Controller
from handler import Handler
from repository import DynamoDBTaskRepository


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    if event.get("path") != "/task":
         return {"statusCode": 404}

    repository = DynamoDBTaskRepository()
    controller = Controller(repository)
    fixtures = Handler(controller)

    handler_funcs = {
        'POST': fixtures.create_task,
        'GET': fixtures.get_task,
        'PUT': fixtures.update_task,
        'DELETE': fixtures.delete_task,
    }

    method = event.get("httpMethod")
    if method in handler_funcs:
        return handler_funcs[method](context, event)

    return {"statusCode": 405}
