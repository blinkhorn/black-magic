import os
import json

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from boto3.dynamodb.conditions import Key

import constants

CODES_TABLE_NAME = os.environ["CODES_TABLE_NAME"]

logger = Logger(child=True)
router = Router()
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(CODES_TABLE_NAME)

@router.get("/<code_id>")
def get_bandcamp_code(code_id: str) -> dict:
    logger.info(f"Fetching code with id [ {code_id} ]")
    response = table.query(
        KeyConditionExpression=Key('code').eq(code_id)
    )
    logger.info(f"Response is: [ {json.dumps(response)} ]")
    if constants.ITEMS not in response or not response[constants.ITEMS]:
        raise NotFoundError(f"[ {code_id} ] code not found. Please try again with a valid code from a Bandcamp release PDF.")
    return response.get('Items')